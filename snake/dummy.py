from .button import Button
from .engine.bounded_object import BoundedObject
from .engine.game_scene import GameScene
from .engine.layer import Layer

class Dummy(GameScene):
    def on_activated(self, screen):
        circle_layer = Layer()
        circle_layer.set_background((0,0,0))
        circle_layer.add_object(BouncyCircle(screen))
        self.add_layer(circle_layer)

        button_layer = Layer(mousable=True)
        button = Button(
            text='Click me!',
            action=self.button_clicked,
            color=(0,128,0),
            hover_color=(0,200,0),
            text_color=(255,255,255)
        )
        button.rect = self.Rect(100,100,100,40)
        button_layer.add_object(button)
        self.add_layer(button_layer)

    def button_clicked(self, event):
        self.log("Yay!")


class BouncyCircle(BoundedObject):
    def __init__(self, screen):
        BoundedObject.__init__(self)

        self.screen_width = screen.width
        self.screen_height = screen.height

        x = self.screen_width / 2.0
        y = self.screen_height / 2.0
        self.rect.center = (x,y)
        self.rect.width = 50
        self.rect.height = 50

        self.v = self.Vector2(
            self.random_float(-1.0, 1.0),
            self.random_float(-1.0, 1.0)
        ).normalize()
        self.v *= self.random_float(30.0, 50.0)

        self.log("activated with v = %s (%s)" % (self.v, self.v.length()))

    def tick(self, millis):
        delta = self.v * (millis / 60.0)

        self.rect.x += delta.x
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.v.x *= -1.0

        self.rect.y += delta.y
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.v.y *= -1.0

    def render(self, surface):
        color = (0, 0, 128)
        self.draw.circle(surface, color, self.rect.center, 50)

