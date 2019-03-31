from .engine.bounded_object import BoundedObject

class Obstacle(BoundedObject):
    def __init__(self, color=None, rect=None):
        BoundedObject.__init__(self)

        self.color = color
        if rect is not None:
            self.rect = rect

    def render(self, surface):
        self.draw.rect(surface, self.color, self.rect)
