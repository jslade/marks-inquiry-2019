#!/usr/bin/env python3

import sys

from snake.game_loop import GameLoop
from snake.game_object import GameObject
from snake.game_state import GameState
from snake.screen import Screen

class SnakeGame(GameObject):
    def __init__(self):
        self.width = 600
        self.height = 600
        self.scale = 10

    def main(self, args):
        self.parse_args(args)
        loop = self.init_game()
        loop.run()

    def parse_args(self, args):
        pass

    def init_game(self):
        state = GameState(self.width, self.height, self.scale)
        screen = Screen(state)
        return GameLoop(state, screen)

if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

