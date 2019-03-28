from .engine.game_object import GameObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

from .food import Food
from .settings import Settings
from .snake import Snake
from .snake_auto_follow import SnakeFollowObject, SnakeFollowMouse
from .snake_collider import SnakeCollider


class Playground(GameScene):
    def on_activated(self, screen):
        snake_layer = Layer()
        snake_layer.set_background((0,0,0))
        self.add_layer(snake_layer)

        self.food = Food()
        self.food.rect.center = (int(Settings.screen_width/2), int(Settings.screen_height/2))
        snake_layer.add_object(self.food)

        self.snake = Snake(color=Settings.snake_colors[0], length=10)
        snake_layer.add_object(self.snake)
        self.snake.move_to(int(Settings.screen_width/2) + 100, int(Settings.screen_height/2) + 100)
        self.snake.set_velocity(Settings.snake_speed, 0)

        self.follow = SnakeFollowObject(self.snake, self.food)
        self.add_offscreen_object(self.follow)

        self.collider = SnakeCollider(self.snake, self.food)
        self.collider.on_touch = self.touched_food
        self.add_offscreen_object(self.collider)


    def touched_food(self, snake, food):
        self.food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
        self.food.rect.centery = self.random_int(100, Settings.screen_height - 100)
        snake.queue_growth(10)

