from .game_object import GameObject

class Layer(GameObject):
    def __init__(self, mousable=False):
        GameObject.__init__(self)
        self.objects = []

        self.mousable = mousable
        self.mouse_in_obj = None
        self.mouse_down_in_obj = None
        self.mouse_up_in_obj = None


    def add_object(self, obj):
        self.objects.append(obj)
        obj.update_bounds()


    def remove_object(self, obj):
        self.objects.remove(obj)


    def tick(self, millis):
        for obj in self.objects:
            obj.tick(millis)

    def render(self, surface):
        for obj in self.objects:
            obj.render(surface)


    def set_mousable(self, flag):
        self.mousable = flag


    def on_mouse_down(self, event):
        if not self.mousable:
            return False

        location = event.pos

        for obj in self.objects:
            if obj.is_touching(location):
                obj.on_mouse_down(event)
                self.mouse_down_in_obj = obj
                return True

    def on_mouse_up(self, event):
        if not self.mousable:
            return False

        location = event.pos

        for obj in self.objects:
            if obj.is_touching(location):
                obj.on_mouse_up(event)
                self.mouse_up_in_obj = obj

                if self.mouse_up_in_obj == self.mouse_down_in_obj:
                    obj.on_mouse_click(event)

                return True

    def on_mouse_moved(self, event):
        if not self.mousable:
            return False

        location = event.pos

        old_in_obj = self.mouse_in_obj
        new_in_obj = None
        for obj in self.objects:
            if obj.is_touching(location):
                new_in_obj = obj

        if old_in_obj != new_in_obj:
            if old_in_obj:
                old_in_obj.on_mouse_exit(event)
            if new_in_obj:
                new_in_obj.on_mouse_enter(event)
            self.mouse_in_obj = new_in_obj
            return True

