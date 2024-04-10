import pygame

from constants import Color

from config import Config
from game.options import Options
from game.screens.screen import AScreen
from game.ui.utils import renderText


class ScreenResult(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, Config.screens.result['music']['basic'])

    def render(self):
        if not self.game:
            print('rendering result without game')
            return

        ui_width = self.win.get_rect().width
        ui_height = self.win.get_rect().height
        ui_surface = pygame.Surface((ui_width, ui_height))
        ui_surface_rect = ui_surface.get_rect()
        ui_surface.fill(self.options.ui.get_primary_bg_color())
        font_size = 36
        color_primary = self.options.ui.get_primary_text_color()

        text_status = 'You have lost' if self.game.has_lost else 'Victory'
        text_middle = '' if self.game.has_lost else f'Score: {self.game.score}'
        text_start_game = 'Press Space To Start'

        center_horizontal = ui_surface_rect.width / 2
        center_vertical = ui_surface_rect.height / 2

        renderText(ui_surface, text_status, color_primary, font_size, (center_horizontal, center_vertical - 40))
        renderText(ui_surface, text_middle, color_primary, font_size, (center_horizontal, center_vertical))
        renderText(ui_surface, text_start_game, color_primary, font_size, (center_horizontal, center_vertical + 40))

        self.win.blit(ui_surface, (0, 0))
