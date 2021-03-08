import pygame as pg
from pygame.locals import *
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
        game_over_screen(game)


def game_over_screen(game):
    sound = pg.mixer.Sound("assets/sounds/oh_yeah.wav")
    if len(game.ship_group.sprites()) == 0:
        sound = pg.mixer.Sound("assets/sounds/im_a_clown.wav")
    sound.play()
    game_over = True
    game.screen.fill(settings.bg_color)
    result = 'Score: ' + str(game.scoreboard.score)
    pg.mixer.music.stop()
    font = pg.font.SysFont('Ariel', 100, True)
    text = font.render(result, True, (255, 0, 0))
    rect = text.get_rect()
    rect.centerx, rect.centery = settings.screen_width / 2, 250
    game.screen.blit(text, rect)

    restart = pg.image.load("assets/images/restart.png")
    re_rect = restart.get_rect()
    re_rect.x, re_rect.y = settings.screen_width / 2 - 100, settings.screen_height / 3 + 150
    game.screen.blit(restart, re_rect)

    pg.display.update()

    write_high_score(game.high_scores, game.scoreboard.score)

    while game_over:
        x, y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if re_rect.collidepoint(x, y):
                        game_over = False
                        game.reset()


def high_score_screen(game):
    on_menu = True
    game.screen.fill(settings.bg_color)
    font = pg.font.SysFont('Ariel', 100, False)
    text = font.render('HIGH SCORES', True, (255, 0, 0))
    rect = text.get_rect()
    rect.centerx, rect.centery = settings.screen_width / 2, 100
    game.screen.blit(text, rect)

    font = pg.font.SysFont('Ariel', 40, False)
    for i in game.high_scores:
        text = font.render(str(i), True, (255, 255, 255))
        rect = text.get_rect()
        rect.centerx, rect.centery = settings.screen_width / 2, game.high_scores.index(i) * 32 + 200
        game.screen.blit(text, rect)

    pg.display.update()
    while on_menu:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    on_menu = False
                    game.start_screen()
