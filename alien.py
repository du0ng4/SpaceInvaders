import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from random import randint
import SpriteSheet
from settings import Settings

settings = Settings()


class Aliens:
    def __init__(self, screen, group, projectiles=None):
        self.screen = screen
        self.group = group
        self.projectiles = projectiles
        self.spawn_aliens()
        self.last_shot_time = 0
        self.direction = 0  # 0 is left, anything else is right

    def spawn_aliens(self):
        for y in range(6):
            for x in range(12):
                spawn_y = 64 * y + 32
                spawn_x = 64 * x + 64
                alien = Alien(screen=self.screen, alien_type=y % 3, x=spawn_x, y=spawn_y, group=self.group)
                self.group.add(alien)

    def update(self):
        self.group.update()
        self.movement()
        if pg.time.get_ticks() > (self.last_shot_time + settings.alien_fire_rate):
            self.shooting()

    def draw(self):
        for alien in self.group.sprites():
            alien.draw()

    def shooting(self):
        if len(self.group.sprites()) >= 1:
            shooter = self.group.sprites()[randint(0, len(self.group.sprites())-1)]
            self.projectiles.add(screen=self.screen, shooter=shooter)
            self.last_shot_time = pg.time.get_ticks()

    def movement(self):
        for alien in self.group.sprites():
            if alien.rect.centerx < 32:
                self.move_down()
                self.direction = 1
            if alien.rect.centerx > 1248:
                self.move_down()
                self.direction = 0
            if self.direction == 0:
                alien.rect.centerx -= alien.move_speed
            else:
                alien.rect.centerx += alien.move_speed

    def move_down(self):
        for alien in self.group.sprites():
            alien.rect.centery += 2
            alien.move_speed += 0.1


class Alien(Sprite):
    # load sprite sheets and images
    ss = [SpriteSheet.Spritesheet('assets/images/alien' + str(number) + '.png') for number in range(1, 4)]
    images = []
    for i in range(3):
        temp = []
        for j in range(2):
            temp.append(ss[i].image_at(rectangle=(0, j * 64, 64, 64), colorkey=(0, 0, 0)))
        images.append(temp)

    ss = SpriteSheet.Spritesheet('assets/images/alien_explosion.png')
    images_explosions = []
    for i in range(4):
        images_explosions.append(ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))

    timers = []
    for i in range(3):
        timers.append(Timer(frames=images[i], wait=700))

    def __init__(self, screen, alien_type, x, y, group):
        super().__init__()
        self.screen = screen
        self.type = alien_type
        self.timer = Alien.timers[self.type]
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)
        self.group = group
        self.move_speed = 2

    def update(self):
        self.remove_if_dead()

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)

    def use_death_animation(self):
        self.timer = Timer(frames=Alien.images_explosions, wait=100, looponce=True)

    def remove_if_dead(self):
        if self.timer.finished is True:
            self.group.remove(self)
