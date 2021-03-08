import sys
from alien import *
from projectile import *
from ship import *
from barrier import *
from ufo import *
from scoreboard import *
from other_functions import *
settings = Settings()


class SpaceInvaders:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
        pg.display.set_caption("Space Invaders")
        icon = pg.image.load('assets/images/icon.png')
        pygame.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.running = False
        self.ship_group = pg.sprite.Group()
        self.alien_group = pg.sprite.Group()
        self.barrier_group = pg.sprite.Group()
        self.ship_projectile_group = pg.sprite.Group()
        self.alien_projectile_group = pg.sprite.Group()
        self.ufo_group = pg.sprite.Group()
        self.aliens = None
        self.projectiles = None
        self.barriers = None
        self.ufos = None
        self.scoreboard = None
        self.high_scores = read_high_score()

    def run_game(self):
        self.scoreboard = Scoreboard()
        self.projectiles = Projectiles(ship_projectile_group=self.ship_projectile_group,
                                       alien_projectile_group=self.alien_projectile_group,
                                       alien_group=self.alien_group, ship_group=self.ship_group,
                                       barrier_group=self.barrier_group, ufo_group=self.ufo_group,
                                       scoreboard=self.scoreboard, screen=self.screen)
        self.ship_group.add(Ship(screen=self.screen, group=self.ship_group, projectiles=self.projectiles))
        self.aliens = Aliens(screen=self.screen, group=self.alien_group, projectiles=self.projectiles)
        self.barriers = Barriers(screen=self.screen, group=self.barrier_group)
        self.ufos = Ufos(screen=self.screen, group=self.ufo_group)
        self.running = True

        pg.mixer.music.load('assets/sounds/music.mp3')
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)

        # game loop
        while self.running:
            keys = pg.key.get_pressed()  # gets key presses
            self.screen.fill(settings.bg_color)
            self.clock.tick(60)

            # ship functions
            self.ship_group.update(keys=keys)
            self.ship_group.draw(self.screen)

            # alien functions
            self.aliens.update()
            self.aliens.draw()

            # projectile functions
            self.projectiles.draw()
            self.projectiles.update()

            # barrier functions
            self.barriers.update()
            self.barriers.draw()

            # ufo functions
            self.ufos.update()
            self.ufos.draw()

            # scoreboard functions
            self.scoreboard.show_score(self.screen)

            # updates the screen
            pg.display.update()
            check_for_game_over(game=self)

            # stops the game loop when exiting
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    self.running = False
                    sys.exit()

    def reset(self):
        self.running = False
        self.ship_group.empty()
        self.alien_group.empty()
        self.barrier_group.empty()
        self.ship_projectile_group.empty()
        self.alien_projectile_group.empty()
        self.ufo_group.empty()
        self.aliens = None
        self.projectiles = None
        self.barriers = None
        self.ufos = None
        self.scoreboard = None
        self.start_screen()

    def start_screen(self):
        start = True
        self.screen.fill(settings.bg_color)

        # credits
        font = pg.font.SysFont('Ariel', 24, False)
        text = font.render('By Andy Duong for CPSC 386', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.left, text_rect.centery = 16, settings.screen_height - 16
        self.screen.blit(text, text_rect)

        # space invaders
        font = pg.font.SysFont('Ariel', 150, False)
        space = font.render('SPACE', True, (255, 255, 255))
        font = pg.font.SysFont('Ariel', 70, False)
        invaders = font.render('INVADERS', True, (0, 255, 0))
        space_rect = space.get_rect()
        invaders_rect = invaders.get_rect()
        space_rect.centerx, space_rect.centery = settings.screen_width / 2, 100
        invaders_rect.centerx, invaders_rect.centery = settings.screen_width / 2, 175
        self.screen.blit(space, space_rect)
        self.screen.blit(invaders, invaders_rect)

        # alien values
        ss = SpriteSheet.Spritesheet('assets/images/start.png')
        start_aliens = []
        for i in range(4):
            start_aliens.append(ss.image_at(rectangle=(0, i * 64, 64, 64), colorkey=(0, 0, 0)))
            alien_rect = start_aliens[i].get_rect()
            alien_rect.x, alien_rect.y = settings.screen_width / 2 - 100, settings.screen_height / 3 + 64 * i
            self.screen.blit(start_aliens[i], alien_rect)
            if i < 3:
                font = pg.font.SysFont('Ariel', 40, False)
                txt = '= ' + str((5 * i ** 2) + (5 * i) + 10) + ' PTS'
                p = font.render(txt, True, (255, 255, 255))
                p_rect = p.get_rect()
                p_rect.centerx, p_rect.centery = settings.screen_width / 2 + 64, settings.screen_height / 3 + 64 * i+32
                self.screen.blit(p, p_rect)
            else:
                font = pg.font.SysFont('Ariel', 40, False)
                p = font.render('= ???', True, (255, 255, 255))
                p_rect = p.get_rect()
                p_rect.centerx, p_rect.centery = settings.screen_width / 2 + 44, settings.screen_height / 3 + 64 * i+32
                self.screen.blit(p, p_rect)

        # play game
        font = pg.font.SysFont('Ariel', 40, False)
        play = font.render('PLAY GAME', True, (0, 255, 0))
        play_rect = play.get_rect()
        play_rect.centerx, play_rect.centery = settings.screen_width / 2, 600
        self.screen.blit(play, play_rect)

        # high scores
        font = pg.font.SysFont('Ariel', 40, False)
        high = font.render('HIGH SCORES', True, (255, 255, 255))
        high_rect = high.get_rect()
        high_rect.centerx, high_rect.centery = settings.screen_width / 2, 650
        self.screen.blit(high, high_rect)

        pg.display.update()
        while start:
            x, y = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play_rect.collidepoint(x, y):
                            start = False
                            self.run_game()
                        if high_rect.collidepoint(x, y):
                            high_score_screen(self)
                            start = False


def main():
    game = SpaceInvaders()  # creates instance of the game
    game.start_screen()  # opens the start screen


if __name__ == '__main__':
    main()
