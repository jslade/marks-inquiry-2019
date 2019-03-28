from .engine.game_object import GameObject

from .snake import Snake
from .settings import Settings


class SnakeCollider(GameObject):
    def __init__(self, snake, obj, on_touch=None):
        GameObject.__init__(self)
        self.snake = snake
        self.objects = [obj]
        self.v = self.Vector2()

        self.on_touch = on_touch

        self.segment_size_squared = Settings.snake_size * Settings.snake_size


    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)


    def tick(self, millis):
        for obj in self.objects:
            collides = self.check_collision(obj)
            if collides:
                self.on_touch(self.snake, obj)


    def check_collision(self, obj):
        if not obj.is_touching((self.snake.head_pt.x, self.snake.head_pt.y)):
            return False

        if isinstance(obj, Snake):
            return self.check_collision_with_snake(obj)
        else:
            return True

    def check_collision_with_snake(self, other_snake):
        head_x = self.snake.head_pt.x
        head_y = self.snake.head_pt.y

        i = 0
        for segment in other_snake.segments():
            i += 1

            self.v.x = head_x - segment.x
            self.v.y = head_y - segment.y
            dist_squared = self.v.length_squared()

            if dist_squared <= self.segment_size_squared:
                if other_snake == self.snake:
                    # Ignore snake touching its own head
                    # (first 3 segments)
                    if i > self.snake.length-3:
                        continue

                return True

