from snake.snake_head import SnakeHead

class Snake(object):
    def __init__(self, board):
        self.head = SnakeHead()
        self.tail = self.head
        self.length = 1
        self.dead = False

        board.set_at(board.center_x(), board.center_y(), self.head)

    def can_move_right(self, board):
        piece = board.get_at(self.head.x + 1, self.head.y)
        if piece is None:
            return True
        else:
            return False

    def move_right(self, board):
        head_x = self.head.x
        head_y = self.head.y
        board.set_at(head_x, head_y, None)
        board.set_at(head_x + 1, head_y, self.head)


    def die(self):
        self.dead = True

    def is_dead(self):
        return self.dead == True


