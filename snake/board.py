from snake.obstacle import Obstacle

class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init_grid()

    def init_grid(self):
        self.grid = [None] * self.width * self.height

        # Fill top and bottom edge
        for x in range(0, self.max_x()+1):
            self.set_at(x, 0, Obstacle())
            self.set_at(x, self.max_y(), Obstacle())

        # Fill left and right edge
        for y in range(1, self.max_y()):
            self.set_at(0, y, Obstacle())
            self.set_at(self.max_x(), y, Obstacle())

    def max_x(self):
        return self.width - 1

    def max_y(self):
        return self.height - 1

    def center_x(self):
        return int(self.max_x() / 2)

    def center_y(self):
        return int(self.max_y() / 2)

    def set_at(self, x, y, what):
        index = int((self.width * y) + x)

        existing = self.grid[index]
        self.grid[index] = what

        if existing is not None:
            existing.removed()
        if what is not None:
            what.placed(x, y)

    def get_at(self, x, y):
        index = int((self.width * y) + x)
        return self.grid[index]


