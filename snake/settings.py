
class Settings(object):
    screen_width = 1200
    screen_height = 800
    target_fps = 60

    snake_size = 10
    snake_turn_rate = 180 / 1000.0
    snake_speed = snake_size * 10 / 1000.0

    snake_speed_boost = 0.05
    snake_speed_boost_max = 1.5
    snake_speed_boost_duration = 3000

    snake_speed_decay = 0.7 / 300 # Decays to 70% speed by length 300

    snake_colors = [
      (0, 200, 100), # green
      (0, 100, 200), # blue
      (150, 0, 0), # red
      (200, 200, 100), # yellow
      (200, 0, 200) # fuscia
    ]

    max_players = 5
    food_per_player = 4

    obstacle_color = (20,20,20)

    maximum_player_idle = 2000
    maximum_snake_idle = 10000
    maximum_food_idle = 30000

    player_disconnect_inactive_time = 60000
