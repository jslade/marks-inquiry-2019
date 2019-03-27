from .engine.game_scene import GameScene
from .engine.layer import Layer

from .apple import Apple
from .settings import Settings
from .snake import Snake
from .snake_renderer import SnakeRenderer



class Playground(GameScene):
    def on_activated(self, screen):
        snake_layer = Layer()
        snake_layer.set_background((0,0,0))
        self.add_layer(snake_layer)

        self.snake = Snake(length=10)
        snake_view = SnakeRenderer(self.snake, Settings.snake_colors[0])
        snake_layer.add_object(snake_view)
        self.reset_snake()

        self.ticks = 0

        self.apple = Apple()
        self.apple.rect.center = (int(Settings.screen_width/2), int(Settings.screen_height/2))
        snake_layer.add_object(self.apple)


        self.on_event(self.pygame.KEYDOWN, self.process_key_down)


    def reset_snake(self):
        self.snake.move_to(int(Settings.screen_width/2), int(Settings.screen_height/2) + 100)
        self.snake.set_velocity(Settings.snake_speed, 0)


    def tick(self, millis):
        GameScene.tick(self, millis)


        self.ticks += millis
        if self.ticks > 500:
            self.ticks -= 500

            self.snake.turn(-45)


    def process_key_down(self, event):
        if event.key == self.pygame.K_SPACE:
            self.reset_snake()
            return
