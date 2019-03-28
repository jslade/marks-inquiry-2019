
class Settings(object):
    screen_width = 800
    screen_height = 600
    target_fps = 60

    snake_size = 10
    snake_speed = snake_size * 10 / 1000.0
    snake_turn_rate = 180 / 1000.0

    snake_colors = [
      (0, 200, 100), # green
      (0, 100, 200), # blue
      (150, 0, 0), # red
      (200, 200, 100), # yellow
      (200, 0, 200) # fuscia
    ]
