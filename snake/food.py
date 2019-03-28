from .engine.bounded_object import BoundedObject
from .engine.colors import Colors

from .settings import Settings
from .snake import Snake


class Food(BoundedObject):
    def __init__(self, ):
        BoundedObject.__init__(self)

        self.color = (180, 20, 40)
        self.color2 = Colors.darker(self.color, .50)

        self.rect.width = Settings.snake_size
        self.rect.height = Settings.snake_size

        self.prerender()

    def prerender(self):
        visual_size = int(Settings.snake_size * 1.2)
        self.surface = self.Surface(
            (visual_size, visual_size),
            flags=self.pygame.SRCALPHA
        )

        self.draw.circle(
            self.surface,
            self.color2,
            (int(visual_size / 2), int(visual_size / 2)),
            int(visual_size / 2)
        )
        self.draw.circle(
            self.surface,
            self.color,
            (int(visual_size / 2), int(visual_size / 2)),
            int(visual_size / 2.5)
        )


    def render(self, surface):
        surface.blit(self.surface, self.rect.topleft)
