from .engine.bounded_object import BoundedObject
from .engine.game_object import GameObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

from .button import Button
from .help_scene import HelpScene
from .multiplayer_scene import MultiplayerScene
from .play_scene import PlayScene


class StartScene(GameScene):
    def on_activated(self, screen):
        button_layer = Layer(mousable=True)
        button_layer.set_background((0, 0, 0))
        self.add_layer(button_layer)

        button = Button(text='Single player', action=self.play_button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(255,00,00))
        button.rect = self.Rect(100,100,100,40)
        button_layer.add_object(button)

        button = Button(text='Multi player', action=self.multiplay_button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(255,00,00))
        button.rect = self.Rect(400,100,100,40)
        button_layer.add_object(button)

        button = Button(text='Help', action=self.help_button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(00,255,00))
        button.rect = self.Rect(100,200,110,40)
        button_layer.add_object(button)

        button = Button(text='Exit', action=self.exit_button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(00,00,255))
        button.rect = self.Rect(100,300,100,40)
        button_layer.add_object(button)

    def play_button_clicked(self, event):
        self.log("You want to play?")
        game_loop = GameObject.find_by_name('GameLoop')
        game_loop.set_scene(PlayScene())

    def multiplay_button_clicked(self, event):
        self.log("Let's play a game!")
        game_loop = GameObject.find_by_name('GameLoop')
        game_loop.set_scene(MultiplayerScene())

    def help_button_clicked(self, event):
        self.log("No help for you!")
        game_loop = GameObject.find_by_name('GameLoop')
        game_loop.set_scene(HelpScene())

    def exit_button_clicked(self, event):
        self.log("Why you leave me?")
        self.post(self.pygame.QUIT)
