import pygame
from PIL import Image
from pygame.sprite import Sprite
from settings import Settings

settings = Settings()


class Barriers:
    def __init__(self, screen, group):
        self.screen = screen
        self.group = group
        self.spawn_barriers()

    def spawn_barriers(self):
        for i in range(3):
            spawn_y = 575
            spawn_x = i * 256 + 300
            barrier = Barrier(self.screen, spawn_x, spawn_y, self.group)
            self.group.add(barrier)

    def update(self):
        self.group.update()

    def draw(self):
        for barrier in self.group.sprites():
            barrier.draw()


class Barrier(Sprite):
    def __init__(self, screen, x, y, group):
        super().__init__()
        self.screen = screen
        self.group = group
        self.image = pygame.image.load('assets/images/barrier.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)

    def update(self):
        self.remove_if_destroyed()

    def draw(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(self.image, rect)

    def take_damage(self):
        raw_str = pygame.image.tostring(self.image, 'RGBA', False)
        pil_img = Image.frombytes('RGBA', self.image.get_size(), raw_str)
        pixels = pil_img.load()
        for z in range(settings.barrier_durability):
            for i in range(pil_img.size[0]):
                for j in range(pil_img.size[1]):
                    if pixels[i, j] == (0, 255, 26, 255):
                        pixels[i, j] = (0, 0, 0, 0)
                        break
        self.image = pygame.image.fromstring(pil_img.tobytes(), pil_img.size, pil_img.mode)

    def remove_if_destroyed(self):
        raw_str = pygame.image.tostring(self.image, 'RGBA', False)
        pil_img = Image.frombytes('RGBA', self.image.get_size(), raw_str)
        pixels = pil_img.load()
        all_destroyed = True
        for i in range(pil_img.size[0]):
            for j in range(pil_img.size[1]):
                if pixels[i, j] == (0, 255, 26, 255):
                    all_destroyed = False
        if all_destroyed is True:
            self.group.remove(self)
