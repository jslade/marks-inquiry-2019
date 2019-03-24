#!/usr/bin/env python3

import sys

from snake.board_renderer import BoardRenderer
from snake.game_state import GameState
from snake.stepper import Stepper

class SnakeGame(object):
    def main(self, args):
        state = GameState(60, 20)
        renderer = BoardRenderer(state)
        stepper = Stepper(state)

        while True:
            renderer.draw()
            stepper.step()
            if stepper.is_finished():
                break

if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

