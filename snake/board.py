from .engine.game_object import GameObject

class Board(GameObject):
    def __init__(self, width, height, size):
        GameObject.__init__(self, 'board')

        self.width = width
        self.height = height
        self.size = size


