from .engine.game_object import GameObject
from .engine.colors import Colors

from .settings import Settings


class SnakeRenderer(GameObject):
    def __init__(self, snake, color):
        GameObject.__init__(self)
        self.snake = snake
        self.color = color
        self.border_color = Colors.lighter(color, 0.20)

        self.prerender()

    def prerender(self):
        self.prerender_segments()
        self.prerender_eyes()

    def prerender_segments(self):
        width = Settings.snake_size * 2
        self.offset = int(width / 2)

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


    def prerender_eyes(self):
        width = int(Settings.snake_size)
        self.eye = self.Surface(
            (width, width),
            flags=self.pygame.SRCALPHA
        )

        self.draw.circle(
            self.eye,
            (255,255,255),
            (int(width / 2), int(width / 2)),
            int(width / 2)
        )
        self.draw.circle(
            self.eye,
            (0,0,0),
            (int(width / 2), int(width / 2)),
            int(width / 4)
        )

        self.eye_vector = self.Vector2()


    def render(self, surface):
        self.render_segments(surface)
        self.render_eyes(surface)

        #self.draw.rect(surface, (255,0,0), self.snake.rect, 2)


    def render_segments(self, surface):
        for segment in self.snake.segments():
            surface.blit(
                self.segment,
                (segment.x - self.offset,
                 segment.y - self.offset)
            )


    def render_eyes(self, surface):
        self.eye_vector.from_polar((Settings.snake_size/3, self.snake.get_heading()))
        self.eye_vector.rotate_ip(90)
        surface.blit(
            self.eye,
            (self.snake.head_pt.x - self.offset + int(self.eye_vector.x),
             self.snake.head_pt.y - self.offset + int(self.eye_vector.y))
        )
        surface.blit(
            self.eye,
            (self.snake.head_pt.x - self.offset - int(self.eye_vector.x),
             self.snake.head_pt.y - self.offset - int(self.eye_vector.y))
        )


class SquareSnakeRenderer(SnakeRenderer):
    def prerender_segments(self):
        width = Settings.snake_size
        self.offset = int(width / 2)

        self.segment = self.Surface(
            (width, width)
        )

        self.draw.rect(
            self.segment,
            self.color,
            self.Rect(0, 0, width, width)
        )

        self.draw.rect(
            self.segment,
            self.border_color,
            self.Rect(0, 0, width, width),
            2
        )

    def render_eyes(self, surface):
        pass