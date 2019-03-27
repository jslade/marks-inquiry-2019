import pygame as _pygame
import random
import sys
import weakref

class GameObject(object):
    @staticmethod
    def init():
        _pygame.init()
        GameObject.seed()

    named_instances = {}

    @staticmethod
    def find_by_name(name):
        ref = GameObject.named_instances.get(name, None)
        if ref is None:
            return None

        obj = ref()
        if obj is None:
            del GameObject.named_instances[name]
            return None

        return obj


    def __init__(self, name = None):
        if name:
            GameObject.named_instances[name] = weakref.ref(self)

    # Pygame helpers
    # This allows e.g. 'self.draw' to be used in
    # place of 'pygame.draw' in all of the subclasses,
    # also obviating the need for 'import pygame'
    # ------------------------------------------------------

    pygame = _pygame
    display = _pygame.display
    draw = _pygame.draw
    event = _pygame.event
    font = _pygame.font
    image = _pygame.image
    key = _pygame.key
    math = _pygame.math
    mixer = _pygame.mixer
    mouse = _pygame.mouse
    time = _pygame.time

    Rect = _pygame.Rect
    Surface = _pygame.Surface
    Vector2 = _pygame.math.Vector2


    # Events
    # ------------------------------------------------------

    next_event_id = _pygame.USEREVENT + 1
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
            event = self.pygame.event.Event(event_id, dict)
        else:
            event = self.pygame.event.Event(event_id, **attrs)

        self.pygame.event.post(event)


    # Logging to the console for debugging:
    # ------------------------------------------------------

    def log(self, msg):
        print(msg)
        sys.stdout.flush()

    # Random numbers:
    # ------------------------------------------------------

    @staticmethod
    def seed(v=None):
        random.seed(v)

    def random_int(self, min, max):
        return random.randint(min, max)

    def random_float(self, min, max):
        return min + random.random() * (max - min)
