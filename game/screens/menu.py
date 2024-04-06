import pygame

from config import Config
from constants import Color
from game.options import Options
from game.screens.screen import AScreen
from game.ui.utils import renderText


class ScreenMenu(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, Config.screens.menu['music']['basic'])

    def render(self):
        ui_width = self.win.get_rect().width
        ui_height = self.win.get_rect().height
        ui_surface = pygame.Surface((ui_width, ui_height))
        ui_surface_rect = ui_surface.get_rect()
        ui_surface.fill(Color.WHITE.value)
        font_size = 36
        color_primary = Color.BLACK.value

        text = 'Press Space To Start'
        renderText(ui_surface, text, color_primary, font_size,
                   (ui_surface_rect.width / 2, ui_surface_rect.height / 2))

        self.win.blit(ui_surface, (0, 0))
