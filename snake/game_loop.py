from snake.game_object import GameObject

import pygame

class GameLoop(GameObject):
    def __init__(self, state, screen):
        self.state = state
        self.screen = screen

    def run(self):
        fps = 60
        clock = pygame.time.Clock()

        self.running = True

        while self.running:
            clock.tick(fps)
            millis = clock.get_time()

            self.process_events()
            self.state.tick(millis)
            self.screen.render()

    def process_events(self):
        for event in pygame.event.get():
            self.process_one_event(event)

    def process_one_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return True

        if event.type == pygame.KEYDOWN:
            self.process_key_down(event)

    def process_key_down(self, event):
        self.log("process_key_down: %s" % event)

        if event.key == pygame.K_ESCAPE:
            self.post_quit()
            return

        if event.key == pygame.K_F4 and self.is_alt_pressed():
            self.post_quit()
            return

    def is_alt_pressed(self):
        pressed_keys = pygame.key.get_pressed()
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        return alt_pressed

    def post_quit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
