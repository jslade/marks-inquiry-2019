from snake.board import Board
from snake.snake import Snake

class GameState(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = Board(width, height)
        self.snake = Snake(self.board)

