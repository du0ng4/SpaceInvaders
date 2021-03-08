# Author: Andy Duong
# Email: aqduong@csu.fullerton.edu
# Class: CPSC 386-02
# Project 1: Space Invaders
# This File: other_functions.py contains useful functions used

from settings import Settings

settings = Settings()


def read_high_score():
    high_scores = []
    with open('scores.txt', 'r') as file:
        for line in file:
            current = line[:-1]
            high_scores.append(int(current))
    return high_scores


def write_high_score(high_scores, current):
    if len(high_scores) < 5:
        high_scores.append(current)
        high_scores.sort(reverse=True)
    else:
        is_a_high_score = False
        for score in high_scores:
            if current > score:
                is_a_high_score = True
        if is_a_high_score:
            high_scores.sort(reverse=True)
            high_scores.pop()
            high_scores.append(current)
            high_scores.sort(reverse=True)
    with open('scores.txt', 'w') as file:
        for score in high_scores:
            file.write('%s\n' % str(score))


def check_for_game_over(game):
    if len(game.ship_group.sprites()) == 0 or len(game.alien_group.sprites()) == 0:
        game.game_over_screen()
