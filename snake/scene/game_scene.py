from .game_object import GameObject

class GameScene(GameObject):
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
        pass

    def render(self, surface):
        pass
