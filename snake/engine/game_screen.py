from .game_object import GameObject

class GameScreen(GameObject):
    def __init__(self, width, height):
        GameObject.init()

        GameObject.__init__(self, 'screen')

        self.width = width
        self.height = height

        self.surface = self.display.set_mode((self.width, self.height))

    def set_title(self, title):
        self.display.set_caption(title)

    def render(self, scene):
        if scene:
            scene.render(self.surface)

        # When all rendering changes are done:
        self.display.flip()

