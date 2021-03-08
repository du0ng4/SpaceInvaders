# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 1: Space Invaders
# This File: projectile.py handles all projectiles in game

import pygame as pg
from ship import Ship
from alien import Alien
from pygame.sprite import Sprite
from settings import Settings

settings = Settings()


class Projectiles:
    def __init__(self, ship_projectile_group, alien_projectile_group, alien_group,
                 ship_group, barrier_group, ufo_group, scoreboard, screen):
        self.ship_projectiles = ship_projectile_group
        self.alien_projectiles = alien_projectile_group
        self.alien_group = alien_group
        self.ship_group = ship_group
        self.barrier_group = barrier_group
        self.ufo_group = ufo_group
        self.scoreboard = scoreboard
        self.screen = screen
        self.sound = pg.mixer.Sound("assets/sounds/bang.wav")

    def add(self, screen, shooter):
        if type(shooter) is Ship:
            self.sound.play()
            self.ship_projectiles.add(Projectile(screen=screen, shooter=shooter))
        if type(shooter) is Alien:
            self.alien_projectiles.add(Projectile(screen=screen, shooter=shooter))

    def update(self):
        # handles projectiles fired by the ship
        self.ship_projectiles.update()
        for projectile in self.ship_projectiles.copy():
            if projectile.rect.bottom <= 0 or projectile.rect.top >= settings.screen_height:
                self.ship_projectiles.remove(projectile)
        collide_with_aliens = pg.sprite.groupcollide(self.alien_group, self.ship_projectiles, False, True)
        if collide_with_aliens:
            for alien in collide_with_aliens:
                alien.use_death_animation()
                self.scoreboard.add_alien_points(alien.type)
        collide_with_ufo = pg.sprite.groupcollide(self.ufo_group, self.ship_projectiles, False, True)
        if collide_with_ufo:
            for ufo in collide_with_ufo:
                ufo.show_points()
                ufo.dead = True
                self.scoreboard.add_ufo_points(ufo.value)

        # handles projectiles fired by aliens
        self.alien_projectiles.update()
        for projectile in self.alien_projectiles.copy():
            if projectile.rect.top >= settings.screen_height:
                self.alien_projectiles.remove(projectile)
        collide_with_ship = pg.sprite.groupcollide(self.ship_group, self.alien_projectiles, False, True)
        if collide_with_ship:
            for ship in collide_with_ship:
                ship.dead = True

        # handles projectiles from both ship and aliens that hit barriers
        alien_collides = pg.sprite.groupcollide(self.barrier_group, self.alien_group, False, False)
        collide_with_barriers_aliens = pg.sprite.groupcollide(self.barrier_group, self.alien_projectiles, False, True)
        collide_with_barriers_ship = pg.sprite.groupcollide(self.barrier_group, self.ship_projectiles, False, True)
        collide_with_barrier = {**collide_with_barriers_aliens, **collide_with_barriers_ship, **alien_collides}
        if collide_with_barrier:
            for barrier in collide_with_barrier:
                barrier.take_damage()

        # projectile on projectile collisions
        pg.sprite.groupcollide(self.ship_projectiles, self.alien_projectiles, True, True)

    def draw(self):
        for projectile in self.ship_projectiles.sprites():
            projectile.draw()
        for projectile in self.alien_projectiles.sprites():
            projectile.draw()


class Projectile(Sprite):
    def __init__(self, screen, shooter):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, 5, 30)
        self.shooter = shooter
        self.rect.centerx = self.shooter.rect.centerx
        self.rect.bottom = self.shooter.rect.top
        self.y = float(self.rect.y)
        if type(shooter) is Ship:
            self.color = settings.player_bullet_color
        else:
            self.color = settings.enemy_bullet_color

    def update(self):
        if type(self.shooter) is Ship:
            self.y -= settings.ship_projectile_speed
        if type(self.shooter) is Alien:
            self.y += settings.alien_projectile_speed
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)
