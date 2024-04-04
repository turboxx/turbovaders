import pygame

import constants
from game.options import Options
from game.screens.screen import AScreen

MUSIC_FILE = 'assets/sfx/music_menu.wav'


class ScreenMenu(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, MUSIC_FILE)

    def render(self):
        self.win.fill(constants.WHITE)
        text = 'Press Space To Start'

        font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
        img = font.render(text, True, (0, 0, 0))
        rect = img.get_rect()
        rect.topleft = (constants.WIDTH / 2 - rect.width / 2, constants.HEIGHT / 2)

        self.win.blit(img, rect)
