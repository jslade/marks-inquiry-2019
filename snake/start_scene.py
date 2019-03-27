from .button import Button
from .engine.bounded_object import BoundedObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

class StartScene(GameScene):
    def on_activated(self, screen):
        button_layer = Layer(mousable=True)
        self.add_layer(button_layer)

        button = Button(text='Click me!', action=self.button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(255,00,00))
        button.rect = self.Rect(100,100,100,40)
        button_layer.add_object(button)

        button = Button(text='Help', action=self.button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(00,255,00))
        button.rect = self.Rect(100,200,110,40)
        button_layer.add_object(button)

        button = Button(text='Exit', action=self.button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(00,00,255))
        button.rect = self.Rect(100,300,100,40)
        button_layer.add_object(button)

    def button_clicked(self, event):
        self.log("Yay!")