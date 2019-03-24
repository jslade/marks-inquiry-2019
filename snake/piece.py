class Piece(object):
    char = ' '

    def __init__(self):
        self.x = None
        self.y = None

    def placed(self, x, y):
        self.x = x
        self.y = y

    def removed(self):
        self.x = None
        self.y = None
