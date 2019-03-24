#!/usr/bin/env python3

import sys

from .scene.game_loop import GameLoop
from .scene.game_object import GameObject
from .scene.game_screen import GameScreen

#from .start_scene import StartScene
from .dummy import Dummy

class SnakeGame(GameObject):
    def __init__(self):
        self.width = 600
        self.height = 600

    def main(self, args):
        self.parse_args(args)
        loop = self.init_game()
        loop.run()

    def parse_args(self, args):
        pass

    def init_game(self):
        screen = GameScreen(self.width, self.height)
        loop = GameLoop(screen)
        #loop.set_sceene(StartScene())
        loop.set_scene(Dummy())

        return loop


if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

