from .engine.game_object import GameObject

from .settings import Settings
from .snake import Snake
from .snake_auto_follow import SnakeFollowController


class Player(GameObject):
    def __init__(self, pubnub_id):
        GameObject.__init__(self)

        self.snake = None
        self.color = None

        self.id = pubnub_id
        self.player_channel = 'player.%s' % (self.id)
        self.player_back_channel = self.player_channel + '.back'
        self.pubnub = GameObject.find_by_name('PubNub')

        self.pubnub.subscribe(self.player_channel, self.on_message)

        self.on_event(Snake.growth_event_id, self.on_growth)
        self.on_event(Snake.death_event_id, self.on_death)
        self.growth_pending = False

        self.follow = None
        self.v = self.Vector2()


    def set_snake(self, snake):
        self.snake = snake
        self.color = self.snake.color

        self.publish({
            'action': 'set_snake',
            'color': {
                'r': self.color[0],
                'g': self.color[1],
                'b': self.color[2]
            },
            'length': self.snake.length
        })

        self.follow = SnakeFollowController(self.snake)
        self.snake.set_velocity(Settings.snake_speed, 0)


    def set_waiting(self, cooldown):
        self.cooldown = cooldown
        if cooldown:
            self.do_after(cooldown, self.reset_cooldown)

        self.publish({
            'action': 'waiting'
        })

    def reset_cooldown(self, _):
        self.cooldown = None

    def is_in_cooldown(self):
        return self.cooldown is not None


    def tick(self, millis):
        if self.follow:
            self.follow.tick(millis)


    def publish(self, msg):
        self.pubnub.publish(
            channel=self.player_back_channel,
            message=msg
        )


    def on_message(self, msg):
        #self.log("player msg=%s" % (msg))
        knob = msg.get('knob', None)
        if knob is not None:
            self.update_knob(knob)


    def update_knob(self, knob):
        self.v.x = knob['x']
        self.v.y = knob['y']
        mag, angle = self.v.as_polar()
        #self.log('knob angle=%s' % (angle))
        if self.follow:
            self.follow.set_controller_angle(angle)


    def on_death(self, event):
        if event.snake != self.snake:
            return

        self.publish({
            'action': 'death',
            'length': self.snake.length
        })

    def on_growth(self, event):
        if event.snake != self.snake:
            return

        if not self.growth_pending:
            self.growth_pending = True
            self.do_after(500, self.update_score)

    def update_score(self, data):
        self.growth_pending = False

        self.publish({
            'action': 'growth',
            'length': self.snake.length
        })


    def still_connected(self):
        return True # todo....
