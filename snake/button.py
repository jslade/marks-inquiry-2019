from .engine.bounded_object import BoundedObject

class Button(BoundedObject):
    def __init__(self, color=None, hover_color=None, text_color=None, text='', action=None):
        BoundedObject.__init__(self)

        self.color = color
        self.hover_color = hover_color or self.color
        self.text_color = text_color

        self._font = self.font.Font(self.font.get_default_font(), 12)

        self.set_text(text)
        self.action = action


    def set_text(self, text):
        self.text = text
        self.rendered_text = self._font.render(
            self.text,
            True,
            self.text_color,
            None
        )
        self.update_bounds()


    def update_bounds(self):
        self.text_loc = (
            self.rect.centerx - self.rendered_text.get_width() / 2,
            self.rect.centery - self.rendered_text.get_height() / 2
        )

    def render(self, surface):
        draw_color = self.hover_color if self.mouse_in else self.color

        self.draw.rect(surface, draw_color, self.rect)
        surface.blit(self.rendered_text, self.text_loc)

    def on_mouse_click(self, event):
        if self.action:
            self.action(event)
