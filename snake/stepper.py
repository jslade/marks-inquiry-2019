class Stepper(object):
    def __init__(self, state):
        self.state = state
        self.board = state.board
        self.snake = state.snake

    def step(self):
        self.move_snake()

    def move_snake(self):
        if self.snake.can_move_right(self.board):
            self.snake.move_right(self.board)
        else:
            self.snake.die()

    def is_finished(self):
        return self.snake.is_dead()
