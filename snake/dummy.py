from snake.scene.game_scene import GameScene

class Dummy(GameScene):
    def on_activated(self, screen):
        self.width = screen.width
        self.height = screen.height

        self.x = self.width / 2.0
        self.y = self.height / 2.0

        self.dx = self.random_float(-1.0, 1.0)
        self.dy = self.random_float(-1.0, 1.0)
        self.speed = self.random_float(30.0, 50.0)

        self.log("activated with speed = %s" % (self.speed))

    def tick(self, millis):
        delta = self.speed * (millis / 60.0)

        self.x += self.dx * delta
        if self.x >= self.width or self.x <= 0.0:
            self.dx *= -1.0

        self.y += self.dy * delta
        if self.y >= self.height or self.y <= 0.0:
            self.dy *= -1.0

    def render(self, surface):
        surface.fill( (0,0,0))

        color = (0, 0, 128)
        self.draw.circle(surface, color, (int(self.x), int(self.y)), 50)

