from snake.game_object import GameObject
from snake.board import Board
from snake.snake import Snake

class GameState(GameObject):
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale

        self.board = Board(width, height)
        self.snake = Snake(self.board)

    def tick(self, millis):
        pass
