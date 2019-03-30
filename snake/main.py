#!/usr/bin/env python3

import optparse
import sys

from .engine.game_loop import GameLoop
from .engine.game_object import GameObject
from .engine.game_screen import GameScreen

from .args import ArgParser
from .playground import Playground
from .settings import Settings
from .start_scene import StartScene


class SnakeGame(GameObject):
    def main(self, args):
        self.parse_args(args)
        loop = self.init_game()
        loop.run()


    def parse_args(self, args):
        self.opts, self.args = ArgParser().parse(args)


    def init_game(self):
        screen = GameScreen(Settings.screen_width, Settings.screen_height)
        loop = GameLoop(screen, Settings.target_fps)

        if self.opts.playground:
            loop.set_scene(Playground())
        else:
            loop.set_scene(StartScene())

        return loop


if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

