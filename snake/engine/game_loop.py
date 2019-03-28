from .game_object import GameObject

import pygame

class GameLoop(GameObject):
    def __init__(self, screen, fps):
        GameObject.__init__(self, 'GameLoop')

        self.screen = screen
        self.fps = fps
        self.scene = None

        self.on_event(pygame.QUIT, self.process_quit)
        self.on_event(pygame.KEYDOWN, self.process_key_down)
        self.on_event(pygame.MOUSEBUTTONDOWN, self.process_mouse_down)
        self.on_event(pygame.MOUSEBUTTONUP, self.process_mouse_up)
        self.on_event(pygame.MOUSEMOTION, self.process_mouse_motion)

        # Special periodic FPS event / timer:
        self.fps_event_id = self.define_event()
        self.time.set_timer(self.fps_event_id, 5000)
        self.on_event(self.fps_event_id, self.print_fps)


    def print_fps(self, event):
        self.log("FPS = %s" % (int(self.clock.get_fps())))

    def set_scene(self, new_scene):
        if self.scene:
            self.scene.deactivate()

        self.scene = new_scene
        if self.scene:
            self.scene.activate(self.screen)

    def run(self):
        self.clock = self.time.Clock()

        self.running = True

        while self.running:
            try:
                self.clock.tick(self.fps)
            except KeyboardInterrupt:
                self.post(pygame.QUIT)

            millis = self.clock.get_time()

            GameObject.process_timers()
            self.process_events()
            if self.scene:
                self.scene.tick(millis)
            self.screen.render(self.scene)


    def process_events(self):
        for event in self.event.get():
            self.process_one_event(event)

    def process_one_event(self, event):
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

    def process_quit(self, event):
        self.running = False

    def process_mouse_down(self, event):
        if self.scene:
            self.scene.on_mouse_down(event)

    def process_mouse_up(self, event):
        if self.scene:
            self.scene.on_mouse_up(event)

    def process_mouse_motion(self, event):
        if self.scene:
            self.scene.on_mouse_moved(event)

