from .engine.game_object import GameObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

from .button import Button
from .food import Food
from .obstacle import Obstacle
from .player import Player
from .pubnub_manager import PubNubManager
from .settings import Settings
from .snake import Snake
from .snake_auto_follow import SnakeFollowObject
from .snake_collider import SnakeCollider


class MultiplayerScene(GameScene):
    def on_deactivated(self):
        self.pubnub.shutdown()

    def on_activated(self, screen):
        self.pubnub = PubNubManager()
        self.add_offscreen_object(self.pubnub)
        self.pubnub.subscribe('launcher', self.on_launcher_message)

        self.player_map = {}
        self.players = [None] * Settings.max_players
        self.waiting_players = []

        self.food = []
        self.food_layer = Layer()
        self.food_layer.set_background((0,0,0))
        self.add_layer(self.food_layer)

        self.score_layer = Layer()
        self.add_layer(self.score_layer)

        self.create_snakes()
        self.create_obstacles()
        self.create_score_text()

        self.create_waiting_message()
        self.do_every(1000, self.check_waiting_players)
        self.do_every(1000, self.snake_auto_follow)
        self.do_every(5000, self.update_food)

        self.on_event(Snake.growth_event_id, self.on_growth)


    def create_snakes(self):
        self.snake_layer = Layer()
        self.add_layer(self.snake_layer)

        self.snakes = []
        self.food_colliders = []
        self.snake_positions = []
        self.snake_colliders = []
        self.auto_follows = []

        for i in range(Settings.max_players):
            snake = Snake(color=Settings.snake_colors[i])
            snake.index = i
            self.snakes.append(snake)

            self.snake_positions.append((100, 200 + i*100))

            collider = SnakeCollider(snake, on_touch=self.touched_food)
            self.food_colliders.append(collider)

            follow = SnakeFollowObject(snake)
            self.auto_follows.append(follow)
            self.add_offscreen_object(follow)

        for snake in self.snakes:
            collider = SnakeCollider(snake, on_touch=self.touched_snake)
            for other_snake in self.snakes:
                if other_snake != snake: collider.add_object(other_snake)
            self.snake_colliders.append(collider)

    def create_obstacles(self):
        self.obstacles = []

        sw = Settings.screen_width
        sh = Settings.screen_height
        thick = 2

        self.obstacles.append(Obstacle(color=Settings.obstacle_color, rect=self.Rect(0,0,sw,thick)))
        self.obstacles.append(Obstacle(color=Settings.obstacle_color, rect=self.Rect(0,sh-thick,sw,thick)))
        self.obstacles.append(Obstacle(color=Settings.obstacle_color, rect=self.Rect(0,0,thick,sh)))
        self.obstacles.append(Obstacle(color=Settings.obstacle_color, rect=self.Rect(sw-thick,0,thick,sh)))

        self.obstacle_layer = Layer()
        self.add_layer(self.obstacle_layer)
        for obstacle in self.obstacles:
            self.obstacle_layer.add_object(obstacle)

        self.obstacle_colliders = []
        for snake in self.snakes:
            collider = SnakeCollider(snake, on_touch=self.touched_obstacle)
            for obstacle in self.obstacles:
                collider.add_object(obstacle)
            self.obstacle_colliders.append(collider)

    def create_score_text(self):
        self.score_text = []
        for snake in self.snakes:
            text = Button(text='XXXXX  --  XXXXX', text_color=snake.color, size=20, rect=self.Rect(10,10,200,24))
            self.score_text.append(text)

    def on_growth(self, event):
        snake = event.snake
        self.update_snake_score(snake)

    def update_snake_score(self, snake):
        text = self.score_text[snake.index]
        player = self.players[snake.index]
        if text and player:
            text.set_text("%.5s -- %-.5s" % (player.id, snake.length))

        self.update_score_text_bounds()

    def update_score_text_bounds(self):
        active_snakes = []
        for snake in self.snakes:
            player = self.players[snake.index]
            if player:
                active_snakes.append(snake)

        active_snakes.sort(reverse=True, key=lambda snake: snake.length)
        sorted_scores = [self.score_text[snake.index] for snake in active_snakes]

        i = 0
        for score_text in sorted_scores:
            score_text.rect.top = 10 + score_text.rect.height * i
            i += 1


    def create_waiting_message(self):
        self.waiting_text = Button( # todo: should be textbox
            text='Waiting for players',
            color=(40,40,60),
            hover_color=(40,40,80),
            text_color=(255,255,255),
            rect=self.Rect(
                int(Settings.screen_width/2 - Settings.screen_width/6),
                int(Settings.screen_height/2 - Settings.screen_height/6),
                int(Settings.screen_height/3),
                int(Settings.screen_height/3)
            )
        )
        self.show_waiting_message()

    def show_waiting_message(self):
        self.log("Now waiting...")
        self.score_layer.add_object(self.waiting_text)

    def hide_waiting_message(self):
        #self.log("Yay! We can play!")
        self.score_layer.remove_object(self.waiting_text)


    def add_food(self, _=None, where=None):
        food = Food()
        self.food.append(food)
        self.food_layer.add_object(food)
        if where is None:
            self.place_food_randomly(food)
        else:
            food.set_placed(where)
        for collider in self.food_colliders:
            collider.add_object(food)

    def remove_food(self, food):
        self.food.remove(food)
        self.food_layer.remove_object(food)
        for collider in self.food_colliders:
            collider.remove_object(food)

    def place_food_randomly(self, food):
        food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
        food.rect.centery = self.random_int(100, Settings.screen_height - 100)
        food.placed = False

    def update_food(self, _):
        self.add_enough_food()

        for i in range(self.active_player_count()):
            self.move_one_piece_of_food()

    def add_enough_food(self):
        count_non_placed_food = 0
        for food in self.food:
            if not food.placed: count_non_placed_food += 1

        food_to_add = self.max_food() - count_non_placed_food
        for i in range(food_to_add):
            self.do_after(500 * i, self.add_food)

    def move_one_piece_of_food(self):
        food = self.choose_random_food(placed_okay=False)
        self.place_food_randomly(food)

    def choose_random_food(self, placed_okay=True):
        for food in self.food:
            if food.placed and food.time_since_placed() < Settings.maximum_food_idle:
                food.placed = False

        while True:
            food = self.food[self.random_int(0, len(self.food)-1)]
            if food.placed and not placed_okay: continue
            return food

    def max_food(self):
        return self.active_player_count() * Settings.food_per_player


    def touched_food(self, snake, food):
        snake.queue_growth(4)

        if len(self.food) > self.max_food():
            self.remove_food(food)
        else:
            self.place_food_randomly(food)

        follow = self.auto_follows[snake.index]
        if follow.get_target() == food:
            follow.set_target(self.choose_random_food())


    def touched_obstacle(self, snake, obstacle):
        #self.log("Snake %s %s touched an obstacle (%d) at %s" % (snake.rect, snake.head_rect, snake.index, obstacle.rect))
        self.kill_snake(snake)

    def touched_snake(self, snake, other_snake):
        #self.log("Snake touched another snake (%s --> %s)" % (snake.index, other_snake.index))
        self.kill_snake(snake)

    def kill_snake(self, snake):
        snake.die()
        self.remove_snake_player(snake)
        self.deactivate_snake(snake)
        self.check_waiting_players()
        self.update_score_text_bounds()


    def activate_snake(self, snake):
        snake.dead = False
        snake.set_length(1)
        snake.set_length(5)
        snake.move_to(*self.snake_positions[snake.index])
        snake.set_velocity(Settings.snake_speed, 0)

        self.snake_layer.add_object(snake)
        self.add_offscreen_object(self.food_colliders[snake.index])
        self.add_offscreen_object(self.snake_colliders[snake.index])
        self.add_offscreen_object(self.obstacle_colliders[snake.index])

        score_text = self.score_text[snake.index]
        self.update_snake_score(snake)
        self.score_layer.add_object(score_text)

        self.add_enough_food()

        self.hide_waiting_message()

    def deactivate_snake(self, snake):
        self.snake_layer.remove_object(snake)
        self.remove_offscreen_object(self.food_colliders[snake.index])
        self.remove_offscreen_object(self.snake_colliders[snake.index])
        self.remove_offscreen_object(self.obstacle_colliders[snake.index])
        self.convert_dead_snake_to_food(snake)
        self.auto_follows[snake.index].set_active(False)

        score_text = self.score_text[snake.index]
        self.score_layer.remove_object(score_text)
        self.update_score_text_bounds()


    def convert_dead_snake_to_food(self, snake):
        n = 0
        for segment in snake.segments():
            n += 1
            if n % 4 == 0:
                self.add_food(where=((segment.x, segment.y)))


    def remove_snake_player(self, snake):
        player = self.players[snake.index]
        self.log("Removing player %s from snake %d" % (player.id, snake.index))
        player.set_snake(None)
        self.players[snake.index] = None
        self.remove_offscreen_object(player)

        if player.still_connected():
            self.add_waiting_player(player, cooldown=10000)


    def snake_auto_follow(self, _=None):
        for snake in self.snakes:
            player = self.players[snake.index]
            follow = self.auto_follows[snake.index]
            if snake.dead or not player: continue
            if player.time_since_last_moved() > Settings.maximum_player_idle:
                player.set_idle()
                if follow.get_target() is None or snake.time_since_last_growth() > Settings.maximum_snake_idle:
                    follow.set_target(self.choose_random_food())
            else:
                player.reset_snake()
                follow.set_target(None)


    def on_launcher_message(self, msg):
        self.log('launcher: %s' % (msg))

        if msg.get('player', None):
            id = msg['player']
            player = self.player_map.get(id, None)
            if player is None:
                player = self.player_map[id] = Player(id)
            self.add_player(player)


    def add_player(self, player):
        if self.active_player_count() < len(self.players):
            self.add_active_player(player)
        else:
            self.add_waiting_player(player)

    def active_player_count(self):
        active = []
        for p in self.players:
            if p is not None: active.append(p)
        return len(active)

    def add_active_player(self, player):
        if player.snake is not None:
            self.log("Huh? player %s already connected to snake %d" % (player.id, player.snake.index))
            player.reset_snake()
            return True

        # Find the first open slot
        for i in range(len(self.snakes)):
            if self.players[i] is None:
                self.log("Adding active player %s in slot %d" % (player.id, i))
                self.players[i] = player
                player.set_snake(self.snakes[i])
                self.add_offscreen_object(player)
                self.activate_snake(self.snakes[i])
                return True

        # No available slot
        return False

    def add_waiting_player(self, player, cooldown=None):
        if player in self.waiting_players:
            return

        self.waiting_players.append(player)
        player.set_waiting(cooldown)
        self.log("Added waiting player %s with cooldown %s" % (player.id, cooldown))

    def check_waiting_players(self, _=None):
        if self.active_player_count() < Settings.max_players:
            self.activate_waiting_player()
        elif self.active_player_count() == 0 and len(self.waiting_players) == 0:
            self.show_waiting_message()

    def activate_waiting_player(self):
        for i in range(len(self.waiting_players)):
            player = self.waiting_players[i]
            if player.is_in_cooldown():
                continue
            if self.add_active_player(player):
                self.waiting_players.pop(i)
                return
