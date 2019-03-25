from .game_object import GameObject

class GameScene(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def remove_layer(self, layer):
        self.layers.remove(layer)

    def activate(self, screen):
        self.screen = screen
        self.on_activated(screen)

    def deactivate(self):
        self.on_deactivated()
        self.screen = None

    def on_activated(self, screen):
        pass

    def on_deactivated(self):
        pass

    def tick(self, millis):
        for layer in self.layers:
            layer.tick(millis)

    def render(self, surface):
        for layer in self.layers:
            layer.render(surface)

    def on_mouse_down(self, event):
        for layer in self.layers:
            handled = layer.on_mouse_down(event)
            if handled:
                break

    def on_mouse_up(self, event):
        for layer in self.layers:
            handled = layer.on_mouse_up(event)
            if handled:
                break

    def on_mouse_moved(self, event):
        for layer in self.layers:
            layer.on_mouse_moved(event)

