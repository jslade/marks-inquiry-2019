from .engine.game_object import GameObject

from .settings import Settings


class SnakeAutoFollow(GameObject):
    def __init__(self, snake, target):
        GameObject.__init__(self)
        self.snake = snake
        self.target = target
        self.turning_to = 0

    def tick(self, millis):
        vector_to_mouse = self.Vector2(
            self.target[0] - self.snake.head_pt.x,
            self.target[1] - self.snake.head_pt.y
        )
        dist, self.turning_to = vector_to_mouse.as_polar()

        dist, angle = self.snake.velocity.as_polar()
        turn_angle = self.turning_to - angle

        max_turn = Settings.snake_turn_rate * millis
        if turn_angle > 0:
            if turn_angle > max_turn: turn_angle = max_turn
        elif turn_angle < 0:
            max_turn *= -1.0
            if turn_angle < max_turn: turn_angle = max_turn

        self.snake.turn(turn_angle)

class SnakeFollowMouse(SnakeAutoFollow):
    def __init__(self, snake):
        SnakeAutoFollow.__init__(self, snake, self.mouse.get_pos())
        self.on_event(self.pygame.MOUSEMOTION, self.process_mouse_motion)

    def process_mouse_motion(self, event):
        self.target = event.pos


class SnakeFollowObject(SnakeAutoFollow):
    def __init__(self, snake, obj):
        SnakeAutoFollow.__init__(self, snake, obj.rect.center)
        self.obj = obj

    def tick(self, millis):
        self.target = self.obj.rect.center
        SnakeAutoFollow.tick(self, millis)

