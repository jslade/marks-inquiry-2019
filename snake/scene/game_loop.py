from .game_object import GameObject

import pygame

class GameLoop(GameObject):
    def __init__(self, screen):
        self.screen = screen
        self.fps = 60
        self.scene = None

    def set_scene(self, new_scene):
        if self.scene:
            self.scene.deactivate()

        self.scene = new_scene
        if self.scene:
            self.scene.activate(self.screen)

    def run(self):
        clock = self.time.Clock()

        self.running = True

        while self.running:
            clock.tick(self.fps)
            millis = clock.get_time()

            self.process_events()
            if self.scene:
                self.scene.tick(millis)
            self.screen.render(self.scene)

    def process_events(self):
        for event in self.event.get():
            self.process_one_event(event)

    def process_one_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return True

        if event.type == pygame.KEYDOWN:
            self.process_key_down(event)

        GameLoop.process_event(event)

    def process_key_down(self, event):
        self.log("process_key_down: %s" % event)

        if event.key == pygame.K_ESCAPE:
            self.post(pygame.QUIT)
            return

        if event.key == pygame.K_F4 and self.is_alt_pressed():
            self.post(pygame.QUIT)
            return

    def is_alt_pressed(self):
        pressed_keys = pygame.key.get_pressed()
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        return alt_pressed
