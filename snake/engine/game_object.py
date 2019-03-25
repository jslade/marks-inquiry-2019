import pygame
import random

class GameObject(object):
    @staticmethod
    def init():
        pygame.init()
        GameObject.seed()

    def __init__(self, name = None):
        self.name = name

    # Pygame helpers
    # This allows e.g. 'self.draw' to be used in
    # place of 'pygame.draw' in all of the subclasses,
    # also obviating the need for 'import pygame'
    # ------------------------------------------------------

    display = pygame.display
    draw = pygame.draw
    event = pygame.event
    font = pygame.font
    image = pygame.image
    key = pygame.key
    math = pygame.math
    mixer = pygame.mixer
    mouse = pygame.mouse
    time = pygame.time

    Rect = pygame.Rect
    Vector2 = pygame.math.Vector2


    # Events
    # ------------------------------------------------------

    next_event_id = pygame.USEREVENT + 1
    event_listeners = {}

    @classmethod
    def define_event(klass):
        event_id = klass.next_event_id
        klass.next_event_id += 1
        return event_id

    @classmethod
    def on_event(klass, event_id, sub):
        klass.event_listeners[event_id] = sub

    @classmethod
    def process_event(klass, event):
        sub = None
        try:
            sub = klass.event_listeners[event.type]
        except KeyError:
            return

        if sub:
            sub(event)

    def post(self, event_id, dict=None, **attrs):
        if dict:
            event = pygame.event.Event(event_id, dict)
        else:
            event = pygame.event.Event(event_id, **attrs)

        pygame.event.post(event)


    # Logging to the console for debugging:
    # ------------------------------------------------------

    def log(self, msg):
        print(msg)

    # Random numbers:
    # ------------------------------------------------------

    @staticmethod
    def seed(v=None):
        random.seed(v)

    def random_int(self, min, max):
        return random.randint(min, max)

    def random_float(self, min, max):
        return min + random.random() * (max - min)
