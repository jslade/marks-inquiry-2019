from .engine.bounded_object import BoundedObject

class TextBox(BoundedObject):
    
    def __init__(self, color=None, text_color=None, text=''):
        BoundedObject.__init__(self)

        self.color = color
        self.text_color = text_color

        self.font = self.pygame.font.Font(self.font.get_default_font(), 16)

        self.set_text(text)


    def set_text(self, text):
        self.text = text
        
        self.rendered_text = []
        for text in self.text:
            rendered_text = self.font.render(
                text,
                True,
                self.text_color,
                None
            )
            self.rendered_text.append(rendered_text)    
        self.update_bounds()

    def update_bounds(self):
        max_text_width = max([rt.get_width() for rt in self.rendered_text])
        max_text_height = max([rt.get_height() for rt in self.rendered_text])

        self.rect.width = max_text_width + 30
        self.rect.height = (max_text_height * 2) * len(self.text) + 30

        self.text_loc = []
        n = 0
        for rendered_text in self.rendered_text: 
            x = self.rect.left + 20
            y = self.rect.top + 20 + n * (max_text_height * 2) 
            self.text_loc.append((x,y))
            n = n + 1    

    


    def render(self, surface):
        self.draw.rect(surface, self.color, self.rect)

        for i in range(len(self.rendered_text)):
            surface.blit(self.rendered_text[i], self.text_loc[i])
