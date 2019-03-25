from .engine.game_scene import GameScene

class Dummy(GameScene):
    def on_activated(self, screen):
        self.width = screen.width
        self.height = screen.height

        self.x = self.width / 2.0
        self.y = self.height / 2.0

        self.v = self.Vector2(
            self.random_float(-1.0, 1.0),
            self.random_float(-1.0, 1.0)
        ).normalize()
        self.v *= self.random_float(30.0, 50.0)

        self.log("activated with v = %s (%s)" % (self.v, self.v.length()))

    def tick(self, millis):
        delta = self.v * (millis / 60.0)

        self.x += delta.x
        if self.x >= self.width or self.x <= 0.0:
            self.v.x *= -1.0

        self.y += delta.y
        if self.y >= self.height or self.y <= 0.0:
            self.v.y *= -1.0

    def render(self, surface):
        surface.fill( (0,0,0))

        color = (0, 0, 128)
        self.draw.circle(surface, color, (int(self.x), int(self.y)), 50)

