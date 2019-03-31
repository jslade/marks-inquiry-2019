from .engine.bounded_object import BoundedObject
from .engine.colors import Colors

from .settings import Settings
from .snake import Snake


class Food(BoundedObject):
    def __init__(self, scale=2.0, visual_scale=1.2):
        BoundedObject.__init__(self)

        self.placed = False
        self.placed_at = self.now()


        self.scale = scale
        self.visual_scale = visual_scale

        self.color = (180, 20, 40)
        self.color2 = Colors.darker(self.color, .50)

        self.rect.width = int(Settings.snake_size * scale)
        self.rect.height = int(Settings.snake_size * scale)

        self.prerender()

    def prerender(self):
        visual_size = int(Settings.snake_size * self.scale * self.visual_scale)
        dv = int((visual_size - self.rect.width) / 2)

        self.surface = self.Surface(
            (visual_size, visual_size),
            flags=self.pygame.SRCALPHA
        )

        self.draw.circle(
            self.surface,
            self.color2,
            (int(visual_size / 2) - dv, int(visual_size / 2) - dv),
            int(visual_size / 2)
        )
        self.draw.circle(
            self.surface,
            self.color,
            (int(visual_size / 2) - dv, int(visual_size / 2) - dv),
            int(visual_size / 2.5)
        )

    def render(self, surface):
        surface.blit(self.surface, self.rect.topleft)
        #self.draw.rect(surface, (0,255,0), self.rect, 2)

    def set_placed(self, where):
        self.rect.center = where
        self.placed = True
        self.placed_at = self.now()

    def time_since_placed(self):
        return self.elapsed_since(self.placed_at)