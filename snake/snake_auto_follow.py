from .engine.game_object import GameObject

from .settings import Settings


class SnakeAutoFollow(GameObject):
    def __init__(self, snake, target_location=None):
        GameObject.__init__(self)
        self.snake = snake
        self.target_location = target_location
        self.turning_to = 0

        self.active = True
        self.ticks = 0


    def set_active(self, active):
        self.active = active


    def tick(self, millis):
        if not self.active: return

        self.ticks += millis
        if self.ticks >= 250:
            self.ticks -= 250
            self.update_target_angle()

        self.turn(millis)

    def update_target_angle(self):
        if self.target_location is not None:
            vector_to_mouse = self.Vector2(
                self.target_location[0] - self.snake.head_pt.x,
                self.target_location[1] - self.snake.head_pt.y
            )
            dist, self.turning_to = vector_to_mouse.as_polar()
        #self.log("target turning_to = %.1f" % (self.turning_to))

    def turn(self, millis):
        dist, angle = self.snake.velocity.as_polar()
        turn_angle = self.turning_to - angle

        if turn_angle > 180:
            turn_angle -= 360
        elif turn_angle < -180:
            turn_angle += 360

        max_turn = Settings.snake_turn_rate * millis
        if turn_angle > 0:
            if turn_angle > max_turn: turn_angle = max_turn
        elif turn_angle < 0:
            max_turn *= -1.0
            if turn_angle < max_turn: turn_angle = max_turn

        #self.log("turning_to %.1f by %.1f" % (self.turning_to, turn_angle))
        self.snake.turn(turn_angle)


class SnakeFollowMouse(SnakeAutoFollow):
    def __init__(self, snake):
        SnakeAutoFollow.__init__(self, snake, self.mouse.get_pos())
        self.on_event(self.pygame.MOUSEMOTION, self.process_mouse_motion)

    def process_mouse_motion(self, event):
        self.target_location = event.pos


class SnakeFollowObject(SnakeAutoFollow):
    def __init__(self, snake, obj=None):
        SnakeAutoFollow.__init__(self, snake)
        self.obj = obj

    def get_target(self):
        return self.obj

    def set_target(self, obj):
        self.obj = obj
        self.active = (self.obj is not None)

    def tick(self, millis):
        if self.obj is not None:
            self.target_location = self.obj.rect.center
        SnakeAutoFollow.tick(self, millis)


class SnakeFollowController(SnakeAutoFollow):
    def __init__(self, snake):
        SnakeAutoFollow.__init__(self, snake)
        self.controller_angle = 0

    def set_controller_angle(self, angle):
        #self.log("set_controller_angle %.1f" % (angle))
        self.turning_to = angle

    def tick(self, millis):
        if not self.active: return

        self.turn(millis)


