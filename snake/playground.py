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

        snakes = []
        for i in range(5):
            food = Food()
            food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
            food.rect.centery = self.random_int(100, Settings.screen_height - 100)
            snake_layer.add_object(food)

            snake = Snake(color=Settings.snake_colors[i], length=10)
            snake_layer.add_object(snake)
            snake.set_velocity(Settings.snake_speed, 0)
            snakes.append(snake)
            self.reset_snake(snake)

            follow = SnakeFollowObject(snake, food)
            self.add_offscreen_object(follow)

            collider = SnakeCollider(snake, food, on_touch=self.touched_food)
            self.add_offscreen_object(collider)

        for snake in snakes:
            collider = SnakeCollider(snake, on_touch=self.touched_snake)
            for other_snake in snakes:
                if other_snake != snake: collider.add_object(other_snake)
            #self.add_offscreen_object(collider)


    def touched_food(self, snake, food):
        food.rect.centerx = self.random_int(100, Settings.screen_width - 100)
        food.rect.centery = self.random_int(100, Settings.screen_height - 100)
        snake.queue_growth(10)

    def touched_snake(self, snake, other_snake):
        self.reset_snake(snake)


    def reset_snake(self, snake):
        snake.move_to(
            self.random_int(200, Settings.screen_width - 200),
            self.random_int(200, Settings.screen_height - 200)
        )
        snake.set_length(10)

