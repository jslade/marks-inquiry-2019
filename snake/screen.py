import pygame

class Screen(object):
    def __init__(self, state, scale):
        self.state = state
        self.scale = scale

        self.pyg_screen = pygame.display.set_mode((self.screen_width(), self.screen_height()))

        self.set_title('Snake')

    def screen_width(self):
        return self.scale * self.state.width

    def screen_height(self):
        return self.scale * self.state.height

    def set_title(self, title):
        pygame.display.set_caption(title)

    def render(self):
        # TODO: Draw something...

        # When all rendering changes are done:
        pygame.display.flip()

