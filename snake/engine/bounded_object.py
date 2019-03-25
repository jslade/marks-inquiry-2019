from .game_object import GameObject

class BoundedObject(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.rect = self.Rect(0,0,0,0)
        self.mouse_in = False


    def is_touching(self, what):
        what_type = type(what)

        if what_type == tuple:
            return self.rect.collidepoint(what)

        elif what_type == self.Rect:
            return self.rect.colliderect(what)

        elif isinstance(what, BoundedObject):
            return self.rect.colliderect(what.rect)

        return False


    def tick(self, millis):
        pass


    def render(self):
        pass


    def on_mouse_enter(self, event):
        self.mouse_in = True

    def on_mouse_exit(self, event):
        self.mouse_in = False

    def on_mouse_down(self, event):
        pass

    def on_mouse_up(self, event):
        pass

    def on_mouse_click(self, event):
        pass
