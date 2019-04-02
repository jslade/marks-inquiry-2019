from .button import Button
from .engine.bounded_object import BoundedObject
from .engine.game_scene import GameScene
from .engine.layer import Layer
from .engine.game_object import GameObject
from .text_box import TextBox


class HelpScene(GameScene):
    def on_activated(self, screen):
        button_layer = Layer(mousable=True)
        self.add_layer(button_layer)
        button_layer.set_background((0, 0, 0))
        

        button = Button(text='Go Back', action=self.back_button_clicked, color=(1,128,1), hover_color=(0,200,0), text_color=(255,00,00))
        button.rect = self.Rect(100,100,100,40)
        button_layer.add_object(button)


        text_box = TextBox(
            text= ['This is a snake game.', 'The goal is to eat apples to grow,', 'and not touch yorself or the walls.'],
            color=(1,128,1),
            text_color=(255,255,255)
            
        )
        text_box.rect.topleft = (100, 200 )
        button_layer.add_object(text_box)


    def back_button_clicked(self, event):
        from .start_scene import StartScene
        self.log("It work!")
        game_loop = GameObject.find_by_name('GameLoop')
        game_loop.set_scene(StartScene())
        
    
    
        

    
    
