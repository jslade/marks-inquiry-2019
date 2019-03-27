from .engine.bounded_object import BoundedObject

from .snake import Snake

class Apple(BoundedObject):
    def __init__(self, ):
        BoundedObject.__init__(self)

        self.color = (180, 20, 40)
        self.rect.width = Snake.segment_size
        self.rect.height = Snake.segment_size

        self.prerender()

    def prerender(self):
        visual_size = int(Snake.segment_size * 2)
        self.surface = self.Surface((visual_size, visual_size))

        self.draw.circle(
            self.surface,
            self.color,
            (int(visual_size / 2), int(visual_size / 2)),
            int(Snake.segment_size / 1.2)
        )

    def render(self, surface):
        surface.blit(self.surface, self.rect.topleft)
