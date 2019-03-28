from .engine.game_object import GameObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

from .apple import Apple
from .settings import Settings
from .snake import Snake
from .snake_auto_follow import SnakeFollowObject, SnakeFollowMouse
from .snake_collider import SnakeCollider


class Playground(GameScene):
    def on_activated(self, screen):
        snake_layer = Layer()
        snake_layer.set_background((0,0,0))
        self.add_layer(snake_layer)

        self.apple = Apple()
        self.apple.rect.center = (int(Settings.screen_width/2), int(Settings.screen_height/2))
        snake_layer.add_object(self.apple)

        self.snake = Snake(color=Settings.snake_colors[0], length=10)
        snake_layer.add_object(self.snake)
        self.snake.move_to(int(Settings.screen_width/2) + 100, int(Settings.screen_height/2))
        self.snake.set_velocity(Settings.snake_speed, 0)

        self.follow = SnakeFollowObject(self.snake, self.apple)
        self.add_offscreen_object(self.follow)

        self.collider = SnakeCollider(self.snake, self.apple)
        self.collider.on_touch = self.touched_apple
        self.add_offscreen_object(self.collider)


    def touched_apple(self, snake, apple):
        self.apple.rect.centerx = self.random_int(100, Settings.screen_width - 100)
        self.apple.rect.centery = self.random_int(100, Settings.screen_height - 100)
        snake.queue_growth(10)

