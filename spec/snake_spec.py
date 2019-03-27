from snake.snake import Snake
from snake.settings import Settings

from snake.spec_helper import *


with description('Snake') as self:
    with it('has a default length'):
        snake = Snake()
        expect(snake.length).to(equal(3))

    with context('no velocity'):
        with it('does not grow'):
            snake = Snake()
            snake.tick(1000)
            expect(snake.length).to(equal(3))

    with context('positive velocity'):
        with it('grows at the expected rate'):
            snake = Snake()
            snake.post = Dummy()

            snake.queue_growth(2)
            snake.set_velocity(Settings.snake_size / 100.0, 0 )

            # Moving right, growing
            snake.tick(100)
            expect(snake.length).to(equal(4))
            expect(snake.growing).to(equal(1))
            expect(snake.head_pt.x).to(equal(Settings.snake_size * 3))
            expect(snake.head_pt.y).to(equal(0))

            # Moving up, growing
            snake.turn(90)
            snake.tick(100)
            expect(snake.length).to(equal(5))
            expect(snake.growing).to(equal(0))
            expect(snake.head_pt.x).to(equal(Settings.snake_size * 3))
            expect(snake.head_pt.y).to(equal(Settings.snake_size))

            # Moving up, not growing
            snake.tick(100)
            expect(snake.length).to(equal(5))
            expect(snake.growing).to(equal(0))
            expect(snake.head_pt.x).to(equal(Settings.snake_size * 3))
            expect(snake.head_pt.y).to(equal(Settings.snake_size * 2))
