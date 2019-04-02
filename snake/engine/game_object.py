import pygame as _pygame
import random
import sys
import weakref

class GameObject(object):
    @staticmethod
    def init():
        _pygame.init()
        _pygame.mixer.init()
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
        if not event_id in klass.event_listeners:
            klass.event_listeners[event_id] = []
        klass.event_listeners[event_id].append(sub)

    @classmethod
    def process_event(klass, event):
        sub = None
        try:
            subs = klass.event_listeners[event.type]
        except KeyError:
            return

        for sub in subs:
            sub(event)

    def post(self, event_id, data=None, **attrs):
        if data is None: data = attrs
        event = self.pygame.event.Event(event_id, data)
        self.pygame.event.post(event)

    def now(self):
        return _pygame.time.get_ticks()

    def elapsed_since(self, when):
        return self.now() - when

    def do_after(self, millis, callback, data=None, **attrs):
        if data is None: data = attrs

        target = self.pygame.time.get_ticks() + millis
        timer = {
            'target': target,
            'action': callback,
            'data': data
        }

        # timer queue is expected to be short, and most insertions likely to happen
        # at the front of the list, so just do linear search...
        queued = False
        for i in range(len(GameObject.timer_queue)):
            existing = GameObject.timer_queue[i]
            if target < existing['target']:
                GameObject.timer_queue[i:i] = [timer]
                queued = True
                break

        if not queued:
            GameObject.timer_queue.append(timer)


    def do_every(self, millis, callback, data=None, **attrs):
        if data is None: data = attrs
        self.do_after(millis, self.on_every, { 'action': callback, 'data': data, 'interval': millis})

    def on_every(self, data):
        data['action'](data['data'])
        self.do_after(data['interval'], self.on_every, data)


    timer_queue = []
    @classmethod
    def process_timers(klass):
        now = _pygame.time.get_ticks()
        while len(klass.timer_queue) > 0:
            next_timer = klass.timer_queue[0]
            if now <= next_timer['target']:
                break

            next_timer['action'](next_timer['data'])
            klass.timer_queue.pop(0)


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
