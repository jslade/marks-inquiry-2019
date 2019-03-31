from .engine.bounded_object import BoundedObject
from .engine.game_object import GameObject

from .settings import Settings
from .snake_renderer import SnakeRenderer, SquareSnakeRenderer


class Snake(BoundedObject):
    growth_event_id = GameObject.define_event()
    death_event_id = GameObject.define_event()

    def __init__(self, color=None, length=3, square=False):
        BoundedObject.__init__(self)

        self.velocity = self.Vector2(0, 0)
        self.head_vector = self.Vector2()
        self.head_rect = self.Rect(0, 0, Settings.snake_size, Settings.snake_size)

        self.head_pt = None
        self.tail_pt = None
        self.length = 0
        self.dead = False
        self.growing = 0

        self.snake_size_squared = Settings.snake_size * Settings.snake_size

        if color:
            self.color = color
            if square:
                self.renderer = SquareSnakeRenderer(self, color)
            else:
                self.renderer = SnakeRenderer(self, color)

        self.set_length(length)


    def set_length(self, length):
        while self.length < length:
            self.add_point(self.length*Settings.snake_size, 0)
        while self.length > length:
            self.remove_point_at_tail()


    def tick(self, millis):
        if not self.dead:
            self.slither(millis)

    def render(self, surface):
        self.renderer.render(surface)

    def die(self):
        self.log("Snake is dead!")
        self.dead = True
        self.post(self.death_event_id, snake=self)

    def is_dead(self):
        return self.dead == True

    def set_velocity(self, speed, angle):
        self.velocity.from_polar( (speed, angle) )
        self.head_vector.x = self.head_vector.y = 0

    def get_heading(self):
        mag, dir = self.velocity.as_polar()
        return dir

    def turn(self, degrees):
        self.velocity.rotate_ip(degrees)
        self.head_vector.rotate_ip(degrees)

    def queue_growth(self, units):
        self.growing += units


    def slither(self, millis):
        # Movement is done by growing the head vector at a fixed velocity
        # Once the head vector is long enough, then move the body points
        self.head_vector += self.velocity * millis
        self.extend_head()
        self.update_bounds()

    def extend_head(self):
        # How far has the head moved from the last point?
        len2 = self.head_vector.length_squared()

        # If the head has moved at least the distance of a new segment,
        # then add a segment
        if len2 >= self.snake_size_squared:
            # The vec_to_head is a vector that is pointed in the direction
            # of movement (the velocity vector), but the segment length long
            vec_to_head = self.Vector2(self.velocity)
            vec_to_head.scale_to_length(Settings.snake_size)

            # So now we'll add a new point that distance away from the last point
            # and remove the tail piece (unless it's growing)
            self.add_point_at_head(vec_to_head)
            if self.remove_point_at_tail() is False:
                self.post(self.growth_event_id, snake=self)

            # Now lop off the segment length from the head vector,
            # and repeat, in case the head vector is more than one
            # segment long
            self.head_vector -= vec_to_head
            self.extend_head()

    def add_point_at_head(self, vec_to_head):
        self.add_point(
            int(self.head_pt.x + vec_to_head.x),
            int(self.head_pt.y + vec_to_head.y)
        )

    def add_point(self, x, y):
        pt = self.Point.get()
        pt.x = x
        pt.y = y

        if self.head_pt:
            self.head_pt.next = pt
        else:
            self.tail_pt = pt
        self.head_pt = pt
        self.length += 1

    def remove_point_at_tail(self):
        if self.growing > 0:
            self.growing -= 1
            return False

        pt = self.tail_pt
        self.tail_pt = pt.next
        self.length -= 1

        self.Point.recycle(pt)

    def segments(self):
        pt = self.tail_pt
        while pt is not None:
            yield pt
            pt = pt.next

    def move_to(self, x, y):
        dx = x - self.head_pt.x
        dy = y - self.head_pt.y
        for pt in self.segments():
            pt.x += dx
            pt.y += dy

        self.update_bounds

    def update_bounds(self):
        x1 = x2 = self.tail_pt.x
        y1 = y2 = self.tail_pt.y
        for pt in self.segments():
            x = pt.x
            y = pt.y

            if x < x1: x1 = x
            if x > x2: x2 = x
            if y < y1: y1 = y
            if y > y2: y2 = y

        x1 = x1 - Settings.snake_size
        y1 = y1 - Settings.snake_size
        x2 = x2 + Settings.snake_size
        y2 = y2 + Settings.snake_size

        self.rect.left = x1
        self.rect.top = y1
        self.rect.width = x2 - x1
        self.rect.height = y2 - y1

        self.head_rect.centerx = self.head_pt.x
        self.head_rect.centery = self.head_pt.y



    # Segments of the snake body are represented by the Point class
    # The list of segments is managed as a singly-linked list,
    # where new points are always added at the "tail" of the list
    # (the snake's head), and points are removed from the "head"
    # of the list (the snake's tail)
    #
    # Since adding/removing points on the body of the snake is
    # a frequent operation, a slight optimization is to keep a
    # pool of available point objects

    class Point(object):
        pool = None

        @classmethod
        def get(kls):
            if kls.pool is None:
                return kls()
            else:
                p = kls.pool
                kls.pool = p.next
                p.next = None
                return p

        @classmethod
        def recycle(kls, p):
            p.next = kls.pool
            kls.pool = p

        def __init__(self):
            self.x = None
            self.y = None
            self.next = None
