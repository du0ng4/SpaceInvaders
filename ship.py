import pygame
from pygame.sprite import Sprite
import SpriteSheet
from timer import Timer
from settings import Settings

settings = Settings()


class Ship(Sprite):
    def __init__(self, screen, group, projectiles=None):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.group = group

        self.image = pygame.image.load('assets/images/ship.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10

        self.ss = SpriteSheet.Spritesheet('assets/images/ship_explosion.png')
        self.images_explosions = []
        for i in range(8):
            self.images_explosions.append(self.ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
        self.timer_explosion = Timer(frames=self.images_explosions, wait=100, looponce=True)

        self.move_speed = 10
        self.dead = False
        self.projectiles = projectiles
        self.last_shot_time = 0

    def update(self, keys):
        self.movement(keys)
        self.remove_if_dead()
        if pygame.time.get_ticks() > (self.last_shot_time + settings.ship_fire_rate):
            self.shooting(keys)
        if self.dead is True:
            self.image = self.timer_explosion.imagerect()

    def movement(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.centerx > 32:
            self.rect.centerx -= self.move_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.centerx < settings.screen_width - 32:
            self.rect.centerx += self.move_speed

    def shooting(self, keys):
        if keys[pygame.K_SPACE] and self.dead is False:
            self.projectiles.add(screen=self.screen, shooter=self)
            self.last_shot_time = pygame.time.get_ticks()

    def remove_if_dead(self):
        if self.timer_explosion.finished is True:
            self.group.remove(self)
