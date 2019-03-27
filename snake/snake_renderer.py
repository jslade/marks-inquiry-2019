from .settings import Settings
from .snake import Snake

from .engine.bounded_object import BoundedObject
from .engine.colors import Colors


class SnakeRenderer(BoundedObject):
    def __init__(self, snake, color):
        BoundedObject.__init__(self)
        self.snake = snake
        self.color = color
        self.border_color = Colors.lighter(color, 0.20)

        self.prerender_segments()


    def tick(self, millis):
        self.snake.tick(millis)


    def prerender_segments(self):
        width = Settings.snake_size * 2
        self.segment = self.Surface(
            (width, width),
            flags=self.pygame.SRCALPHA
        )

        self.draw.circle(
            self.segment,
            self.color,
            (int(width / 2), int(width / 2)),
            int(width / 2)
        )

        self.draw.circle(
            self.segment,
            self.border_color,
            (int(width / 2), int(width / 2)),
            int(width / 2),
            2
        )

        self.offset = int(width / 2)


    def render(self, surface):
        for segment in self.snake.segments():
            surface.blit(
                self.segment,
                (segment.x - self.offset,
                 segment.y - self.offset)
            )
