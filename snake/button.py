from .engine.bounded_object import BoundedObject

class Button(BoundedObject):
    def __init__(self, size=12, color=None, hover_color=None, text_color=None, text='', action=None, rect=None, pad=None):
        BoundedObject.__init__(self)

        self.color = color
        self.hover_color = hover_color or self.color
        self.text_color = text_color

        self.action = action

        self.font = self.pygame.font.Font(self.font.get_default_font(), size)
        self.pad = size if pad is None else pad

        if rect is not None:
            self.rect = rect

        self.set_text(text)


    def set_text(self, text):
        self.text = text
        self.rendered_text = self.font.render(
            self.text,
            True,
            self.text_color,
            None
        )
        self.update_bounds()


    def update_bounds(self):
        if self.rect.width == 0:
            self.rect.width = self.rendered_text.get_width() + 2*self.pad
        if self.rect.height == 0:
            self.rect_height = self.rendered_text.get_height() + 2*self.pad

        self.text_loc = (
            self.rect.centerx - self.rendered_text.get_width() / 2,
            self.rect.centery - self.rendered_text.get_height() / 2
        )

    def render(self, surface):
        draw_color = self.hover_color if self.mouse_in else self.color
        if draw_color is not None:
            self.draw.rect(surface, draw_color, self.rect)

        surface.blit(self.rendered_text, self.text_loc)

    def on_mouse_click(self, event):
        if self.action:
            self.action(event)
