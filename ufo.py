import pygame as pg
from pygame.sprite import Sprite
import SpriteSheet
from timer import Timer
from random import randint
from settings import Settings

settings = Settings()


class Ufos:
    def __init__(self, screen, group):
        self.screen = screen
        self.group = group

    def spawn_ufo(self):
        spawn = randint(0, 500)
        if spawn == 0 and len(self.group.sprites()) == 0:
            self.group.add(Ufo(screen=self.screen, group=self.group))

    def update(self):
        self.group.update()
        self.spawn_ufo()

    def draw(self):
        for ufo in self.group.sprites():
            ufo.draw()


class Ufo(Sprite):
    def __init__(self, screen, group):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.group = group

        self.ss = SpriteSheet.Spritesheet('assets/images/ufo.png')
        self.images = []
        for i in range(3):
            self.images.append(self.ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
        self.timer = Timer(frames=self.images, wait=100, looponce=False)
        self.image = self.timer.imagerect()
        self.rect = self.image.get_rect()

        self.dead = False
        self.value = randint(100, 200)
        self.move_speed = 5
        self.direction = randint(0, 1)  # 0 is left, anything else is right
        if self.direction == 0:
            self.rect.centerx = settings.screen_width
        else:
            self.rect.centerx = 0
        self.rect.centery = 32

    def update(self):
        self.movement()
        self.remove_if_gone()

    def draw(self):
        if self.dead is False:
            self.image = self.timer.imagerect()
        rect = self.image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        if self.dead is True:
            rect.y += 15
        self.screen.blit(self.image, rect)

    def movement(self):
        if self.direction == 0:
            self.rect.centerx -= self.move_speed
        else:
            self.rect.centerx += self.move_speed

    def remove_if_gone(self):
        if self.rect.centerx > settings.screen_width or self.rect.centerx < 0:
            self.group.remove(self)

    def show_points(self):
        self.image = pg.font.SysFont('monospace', 24, True).render(str(self.value), True, (255, 0, 0))
