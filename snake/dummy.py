from snake.scene.game_scene import GameScene

class Dummy(GameScene):
    def on_activated(self):
        self.width = float(self.screen.width)
        self.height = float(self.screen.height)

        self.x = self.width / 2.0
        self.y = self.height / 2.0

        self.dx = self.random_float(-1.0, 1.0)
        self.dy = self.random_float(-1.0, 1.0)

    def tick(self, millis):
        self.x += self.dx
        if self.x >= self.width or self.x <= 0.0:
            self.dx *= -1.0

        self.y += self.dy
        if self.y >= self.height or self.y <= 0.0:
            self.dy *= -1.0

    def render(self, surface):
      self.draw.circle(surface, (128, 0, 128), (int(self.x), int(self.y)), 50)

