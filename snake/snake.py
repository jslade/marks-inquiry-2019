from .engine.game_object import GameObject

from .settings import Settings


class Snake(GameObject):
    growth_event_id = GameObject.define_event()
    death_event_id = GameObject.define_event()

    def __init__(self, length=3):
        GameObject.__init__(self)

        self.velocity = self.Vector2(0, 0)
        self.head_vector = self.Vector2()

        self.head_pt = None
        self.tail_pt = None
        self.length = 0

        for i in range(length):
            self.add_point(i*Settings.snake_size, 0)

        self.dead = False
        self.growing = 0

    def tick(self, millis):
        self.slither(millis)
        #self.check_collisions()

    def die(self):
        self.dead = True
        self.post(self.death_event_id, snake=self)

    def is_dead(self):
        return self.dead == True

    def set_velocity(self, speed, angle):
        self.velocity.from_polar( (speed, angle) )
        self.head_vector.x = self.head_vector.y = 0

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

    def extend_head(self):
        # How far has the head moved from the last point?
        len = self.head_vector.length()

        # If the head has moved at least the distance of a new segment,
        # then add a segment
        if len >= Settings.snake_size:
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
