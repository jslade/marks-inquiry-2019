#!/usr/bin/env python

import os
import sys

class SnakeGame(object):
    def main(self, args):
        self.board = Board(60, 20)
        self.snake = Snake(self.board)
        
        self.renderer = BoardRenderer()
        self.stepper = Stepper()

        while True:
            self.renderer.draw(self.board)
            self.stepper.step()
            if self.stepper.finished():
                break


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
        return self.max_x() / 2

    def center_y(self):
        return self.max_y() / 2

    def set_at(self, x, y, what):
        index = self.width * y + x

        existing = self.grid[index]
        self.grid[index] = what
        
        if existing is not None:
            existing.removed()
        if what is not None:
            what.placed(x, y)

    def get_at(self, x, y):
        index = self.width * y + x
        return self.grid[index]


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


class Obstacle(Piece):
    char = '#'
    
    
class SnakeSegment(Piece):
    char = 'O'


class SnakeHead(SnakeSegment):
    char = 'O'


class Snake(object):
    def __init__(self, board):
        self.head = SnakeHead()
        self.tail = self.head
        self.length = 1

        board.set_at(board.center_x(), board.center_y(), self.head)



class BoardRenderer(object):
    def draw(self, board):
        for y in range(0, board.max_y()+1):
            row = ''
            for x in range(0, board.max_x()+1):
                row += self.char_for(board.get_at(x, y))
            print row

    def char_for(self, piece):
        if piece is None:
            return ' '
        else:
            return piece.char


class Stepper(object):
    def step(self):
        pass

    def finished(self):
        return True


if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])
