import pygame

class GameLoop(object):
    def __init__(self, state, screen):
        self.state = state
        self.screen = screen

    def run(self):
        fps = 60
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            self.process_events()
            self.tick()
            self.screen.render()

            clock.tick(fps)

    def process_events(self):
        for event in pygame.event.get():
            self.process_one_event(event)

    def process_one_event(self, event):
        if self.is_trying_to_quit(event):
            self.running = False
            return

        #if event.type == pygame.KEYDOWN:
        #    self.process_key(event)

    def is_trying_to_quit(self, event):
        if event.type == pygame.QUIT:
            return True

        pressed_keys = pygame.key.get_pressed()
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        altF4 = alt_pressed and event.type == pygame.KEYDOWN and event.key == pygame.K_F4
        if altF4:
            return True

        escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        if escape:
            return True

    def tick(self):
        pass
