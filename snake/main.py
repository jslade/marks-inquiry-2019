#!/usr/bin/env python3

import sys
import pygame

from snake.screen import Screen
from snake.game_state import GameState
from snake.game_loop import GameLoop

class SnakeGame(object):
    def __init__(self):
        self.width = 60
        self.height = 60
        self.scale = 10

    def main(self, args):
        self.parse_args(args)
        loop = self.init_game()
        loop.run()

    def parse_args(self, args):
        pass

    def init_game(self):
        pygame.init()

        state = GameState(self.width, self.height)
        screen = Screen(state, self.scale)
        return GameLoop(state, screen)

if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

