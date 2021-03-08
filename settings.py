# any changes must be made before running
class Settings:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (0, 0, 0)
        self.enemy_bullet_color = (255, 0, 0)
        self.player_bullet_color = (0, 255, 0)
        self.alien_projectile_speed = 10
        self.ship_projectile_speed = 10
        # for fire rates, lower values = faster, higher values = slower
        self.ship_fire_rate = 100
        self.alien_fire_rate = 5000
        # min 1 max 30, lower values = more durable, higher values = less durable
        self.barrier_durability = 5
