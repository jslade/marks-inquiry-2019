#!/usr/bin/env python

import os
import sys
import time

class SnakeGame(object):
    def main(self, args):
        state = GameState(60, 20)
        renderer = BoardRenderer(state)
        stepper = Stepper(state)

        while True:
            renderer.draw()
            time.sleep(0.5)
            stepper.step()
            if stepper.is_finished():
                break


class GameState(object):
    def __init__(self, width, height):
        self.board = Board(width, height)
        self.snake = Snake(self.board)
    
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
        index = (self.width * y) + x

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
    char = '0'


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

    
class BoardRenderer(object):
    def __init__(self, state):
        self.state = state
        self.board = state.board

    def draw(self):
        print("\033[2J")
        for y in range(0, self.board.max_y()+1):
            row = ''
            for x in range(0, self.board.max_x()+1):
                row += self.char_for(self.board.get_at(x, y))
            print row

    def char_for(self, piece):
        if piece is None:
            return ' '
        else:
            return piece.char


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


if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

    
