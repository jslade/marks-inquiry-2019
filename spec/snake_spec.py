from snake.snake import Snake

from mamba import description, context, it
from expects import expect, equal


with description('Snake') as self:
    with it('has a default length'):
        snake = Snake()
        expect(snake.length).to(equal(3))

    with description('no velocity'):
        with it('does not grow'):
            snake = Snake()
            snake.tick(1000)
            expect(snake.length).to(equal(3))

