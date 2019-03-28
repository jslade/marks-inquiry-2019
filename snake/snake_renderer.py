from .engine.game_object import GameObject
from .engine.colors import Colors

from .settings import Settings


class SnakeRenderer(GameObject):
    def __init__(self, snake, color):
        GameObject.__init__(self)
        self.snake = snake
        self.color = color
        self.border_color = Colors.lighter(color, 0.20)

        self.prerender_segments()


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

        #self.draw.rect(surface, (255,0,0), self.snake.rect, 2)


