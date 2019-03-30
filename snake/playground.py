from .engine.game_object import GameObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

from .food import Food
from .settings import Settings
from .snake import Snake
from .snake_auto_follow import SnakeFollowObject, SnakeFollowMouse
from .snake_collider import SnakeCollider

from .pubnub_manager import PubNubManager
from .player import Player


class Playground(GameScene):
    def on_activated(self, screen):
        self.pubnub = PubNubManager()
        self.pubnub.subscribe('launcher', self.on_launcher_message)
        self.player = None

        snake_layer = Layer()
        snake_layer.set_background((0,0,0))
        self.add_layer(snake_layer)

        self.snakes = []
        for i in range(1):
            food = Food()
            food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
            food.rect.centery = self.random_int(100, Settings.screen_height - 100)
            snake_layer.add_object(food)

            snake = Snake(color=Settings.snake_colors[i], length=10)
            snake_layer.add_object(snake)
            #snake.set_velocity(Settings.snake_speed, 0)
            self.snakes.append(snake)
            self.reset_snake(snake)

            #follow = SnakeFollowObject(snake, food)
            #self.add_offscreen_object(follow)

            collider = SnakeCollider(snake, food, on_touch=self.touched_food)
            self.add_offscreen_object(collider)

            self.do_every(1000, self.check_snakes_out_of_bounds, snake=snake, food=food)

        for snake in self.snakes:
            collider = SnakeCollider(snake, on_touch=self.touched_snake)
            for other_snake in self.snakes:
                if other_snake != snake: collider.add_object(other_snake)
            #self.add_offscreen_object(collider)

    def on_deactivated(self):
        self.pubnub.shutdown()


    def reset_food(self, food):
        food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
        food.rect.centery = self.random_int(100, Settings.screen_height - 100)

    def touched_food(self, snake, food):
        self.reset_food(food)
        snake.queue_growth(10)

    def touched_snake(self, snake, other_snake):
        self.reset_snake(snake)


    def reset_snake(self, snake):
        snake.move_to(
            self.random_int(200, Settings.screen_width - 200),
            self.random_int(200, Settings.screen_height - 200)
        )
        snake.set_length(10)


    def check_snakes_out_of_bounds(self, data):
        snake = data['snake']
        food = data['food']
        if self.snake_out_of_bounds(snake):
            self.reset_food(food)

    def snake_out_of_bounds(self, snake):
        return (snake.head_pt.x > Settings.screen_width) or \
               (snake.head_pt.x < 0) or \
               (snake.head_pt.y > Settings.screen_height) or \
               (snake.head_pt.y < 0)


    def on_launcher_message(self, msg):
        self.log('launcher: %s' % (msg))

        if msg.get('player', None):
            self.add_player(msg['player'])


    def add_player(self, player_id):
        if self.player:
            self.remove_offscreen_object(self.player)

        self.player = Player(player_id)
        self.player.set_snake(self.snakes[0])
        self.add_offscreen_object(self.player)
