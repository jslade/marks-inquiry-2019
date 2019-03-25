class BoardRenderer(object):
    def __init__(self, state):
        self.state = state
        self.board = state.board

    def draw(self):
        for y in range(0, self.board.max_y()+1):
            row = ''
            for x in range(0, self.board.max_x()+1):
                row += self.char_for(self.board.get_at(x, y))
            print(row)

    def char_for(self, piece):
        if piece is None:
            return ' '
        else:
            return piece.char


