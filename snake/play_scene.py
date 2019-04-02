from .engine.game_scene import GameScene
from .engine.layer import Layer
from .engine.game_object import GameObject

from .food import Food
from .obstacle import Obstacle
from .snake import Snake
from .settings import Settings
from .snake_collider import SnakeCollider


class PlayScene(GameScene):
    def on_activated(self, screen):
        snake_layer = Layer(mousable=False)
        self.add_layer(snake_layer)
        snake_layer.set_background((0, 0, 0))

        self.snake = Snake(color = Settings.snake_colors [0])
        snake_layer.add_object(self.snake)
        self.snake.move_to(int(Settings.screen_width / 2), int(Settings.screen_height / 2))
        self.snake.set_velocity(Settings.snake_speed, 0)

        self.food = Food()
        snake_layer.add_object(self.food)
        self.place_food()

        collider = SnakeCollider(self.snake, self.food, on_touch=self.touched_food)
        self.add_offscreen_object(collider)

        collider = SnakeCollider(self.snake, self.snake, on_touch=self.touched_snake)
        self.add_offscreen_object(collider)

        self.on_event(self.pygame.KEYDOWN, self.key_pressed)

        with open('bite.wav', 'rb') as f:
            self.bite = self.pygame.mixer.Sound(f.read())
        with open('sad.wav', 'rb') as f:
            self.sad_trombone = self.pygame.mixer.Sound(f.read())


    def key_pressed(self, event):
        if event.key == self.pygame.K_ESCAPE:
            self.esc_pressed()
            return
        if event.key == self.pygame.K_w:
            self.turn_up()
            return
        if event.key == self.pygame.K_a:
            self.turn_left()
            return
        if event.key == self.pygame.K_s:
            self.turn_down()
            return
        if event.key == self.pygame.K_d:
            self.turn_right()
            return

    def esc_pressed(self):
        self.go_back()

    def go_back(self, _=None):
        from .start_scene import StartScene
        self.log("It work!")
        game_loop = GameObject.find_by_name('GameLoop')
        game_loop.set_scene(StartScene())

    def turn_up(self):
        self.snake.set_velocity(Settings.snake_speed, 270)

    def turn_down(self):
        self.snake.set_velocity(Settings.snake_speed, 90)

    def turn_left(self):
        self.snake.set_velocity(Settings.snake_speed, 180)

    def turn_right(self):
        self.snake.set_velocity(Settings.snake_speed, 0)

    def place_food(self):
        self.food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
        self.food.rect.centery = self.random_int(100, Settings.screen_height - 100)

    def touched_food(self, snake, food):
        self.place_food()
        self.bite.play()
        self.snake.queue_growth(10)

    def touched_snake(self, snake, _):
        self.snake.die()
        self.sad_trombone.play()
        self.do_after(2000, self.go_back)
