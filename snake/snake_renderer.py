from .snake import Snake

from .engine.bounded_object import BoundedObject


class SnakeRenderer(BoundedObject):
    def __init__(self, snake, color):
        BoundedObject.__init__(self)
        self.snake = snake
        self.color = color
        self.border_color = (255,255,255)

        self.prerender_segments()


    def tick(self, millis):
        self.snake.tick(millis)


    def prerender_segments(self):
        width = Snake.segment_size * 2
        self.segment = self.Surface(
            (width, width),
            flags=self.pygame.SRCALPHA
        )

        self.draw.circle(
            self.segment,
            self.color,
            (int(width / 2), int(width / 2)),
            int(width / 2.5)
        )

        self.draw.circle(
            self.segment,
            self.border_color,
            (int(width / 2), int(width / 2)),
            int(width / 2.5),
            2
        )


    def render(self, surface):
        for segment in self.snake.segments():
            surface.blit(self.segment, (segment.x, segment.y))
