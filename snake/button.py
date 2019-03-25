from .engine.bounded_object import BoundedObject

class Button(BoundedObject):
    def __init__(self, color=None, hover_color=None, text_color=None, text='', action=None):
        BoundedObject.__init__(self)

        self.color = color
        self.hover_color = hover_color or self.color
        self.text_color = text_color

        self.text = text
        self.action = action

    def render(self, surface):
        draw_color = self.hover_color if self.mouse_in else self.color

        self.draw.rect(surface, draw_color, self.rect)

    def on_mouse_click(self, event):
        if self.action:
            self.action(event)
