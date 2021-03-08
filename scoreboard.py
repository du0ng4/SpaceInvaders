# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 1: Space Invaders
# This File: scoreboard.py handles the score system of the current round/game

import pygame as pg
from settings import Settings

settings = Settings()


class Scoreboard:
    def __init__(self):
        self.score = 0

    def add_alien_points(self, alien_type):
        if alien_type == 0:
            self.score += 10
        if alien_type == 1:
            self.score += 20
        if alien_type == 2:
            self.score += 40

    def add_ufo_points(self, value):
        self.score += value

    def show_score(self, screen):
        font = pg.font.SysFont('Ariel', 40, False)
        score = font.render('Points: ' + str(self.score), True, (0, 255, 0))
        score_rect = score.get_rect()
        score_rect.right, score_rect.centery = settings.screen_width - 16, 32
        screen.blit(score, score_rect)
