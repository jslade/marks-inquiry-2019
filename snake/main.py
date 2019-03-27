#!/usr/bin/env python3

import sys

from .engine.game_loop import GameLoop
from .engine.game_object import GameObject
from .engine.game_screen import GameScreen

from .settings import Settings

#from .start_scene import StartScene
from .dummy import Dummy


#from .pubnub_manager import PubNubManager


class SnakeGame(GameObject):
    def main(self, args):
        self.parse_args(args)
        loop = self.init_game()
        loop.run()

        #self.pubnub.shutdown()


    def parse_args(self, args):
        pass

    def init_game(self):
        #self.pubnub = PubNubManager()

        screen = GameScreen(Settings.screen_width, Settings.screen_height)
        loop = GameLoop(screen, Settings.target_fps)
        #loop.set_sceene(StartScene())
        loop.set_scene(Dummy())

        return loop


if __name__ == '__main__':
    SnakeGame().main(sys.argv[1:])

