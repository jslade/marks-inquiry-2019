from .button import Button
from .engine.bounded_object import BoundedObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

class StartScene(GameScene):


    button_layer = Layer(mousable=True)
        button = Button(
            text='Click me!',
            action=self.button_clicked,
            color=(1,128,1),
            hover_color=(0,200,0),
            text_color=(255,255,255)
        )
        button.rect = self.Rect(100,100,100,40)
        button_layer.add_object(button)
        self.add_layer(button_layer)

    def button_clicked(self, event):
        self.log("Yay!")