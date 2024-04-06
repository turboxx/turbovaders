import pygame

from config import Config
from constants import Color
from game.options import Options
from game.screens.screen import AScreen
from game.ui.utils import renderText, create_text


class ScreenMenu(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, Config.screens.menu['music']['basic'])
        self.size_increase = True
        self.size = 0.7

    def render(self):
        ui_width = self.win.get_rect().width
        ui_height = self.win.get_rect().height
        ui_surface = pygame.Surface((ui_width, ui_height))
        ui_surface_rect = ui_surface.get_rect()
        ui_surface.fill(Color.WHITE.value)
        font_size = 40
        color_primary = Color.BLACK.value

        text_title = 'Turbovaders'

        renderText(ui_surface,
                   text_title, color_primary, font_size * 2,
                   (ui_surface_rect.width / 2, ui_surface_rect.height / 2 - 100))

        text_start = 'Press Space to Start'
        # renderText(ui_surface,
        #            text_start, color_primary, int(font_size * self.get_font_multiplier()),
        #            (ui_surface_rect.width / 2, ui_surface_rect.height / 2 + 100))

        scale = self.get_font_multiplier()
        surface_text = pygame.transform.scale_by(create_text(text_start, color_primary, font_size), scale)
        surface_text_rect = surface_text.get_rect()
        surface_text_rect.topleft = (ui_surface_rect.width / 2 - surface_text_rect.width / 2,
                                     ui_surface_rect.height / 2 + 100 - surface_text_rect.height / 2)

        ui_surface.blit(surface_text, surface_text_rect)

        self.win.blit(ui_surface, (0, 0))

    def get_font_multiplier(self):
        minimum = 0.7
        maximum = 0.8

        multiplier = self.size
        increment = 0.0005
        bounce_delay = 0.02

        self.size = self.size + (increment * (1 if self.size_increase else -1))

        if multiplier >= maximum + bounce_delay:
            self.size_increase = False

        elif multiplier <= minimum - bounce_delay / 2:
            self.size_increase = True

        return min(max(self.size, minimum), maximum)
