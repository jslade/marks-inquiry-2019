from .engine.game_scene import GameScene
from .engine.layer import Layer

from .apple import Apple
from .settings import Settings
from .snake import Snake
from .snake_renderer import SnakeRenderer



class Dummy(GameScene):
    def on_activated(self, screen):
        snake_layer = Layer()
        snake_layer.set_background((0,0,0))
        self.add_layer(snake_layer)

        self.snake = Snake()
        self.snake.move_to(int(Settings.screen_width/2), int(Settings.screen_height/2))
        snake_view = SnakeRenderer(self.snake, Settings.snake_colors[0])
        snake_layer.add_object(snake_view)

        self.snake.set_velocity(Settings.snake_speed, 0)

        self.ticks = 0


        self.apple = Apple()
        self.apple.rect.topleft = (200,200)
        snake_layer.add_object(self.apple)

    def tick(self, millis):
        GameScene.tick(self, millis)


        self.ticks += millis
        if self.ticks > 200:
            self.ticks -= 200

            self.snake.turn(self.random_int(-90, 90))
            self.snake.queue_growth(self.random_int(0, 1))
