import pygame

from constants import Color
from config import Config
from game.options import Options
from game.screens.screen import AScreen
from game.ui.utils import renderText

MUSIC_GAME_FILE = Config.screens.game['music']['basic']
MUSIC_PAUSE_FILE = Config.screens.game['music']['pause']


class ScreenGame(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, MUSIC_GAME_FILE)

    def render(self):
        self.win.fill(self.options.ui.get_primary_bg_color())
        self.__render_ui()

        if self.options.dev_mode:
            self.__render_arena()

        self.game.render_game()

        if not self.game.active_level.loaded:
            self.__render_count_down_overlay()

        if not self.game.running:
            self.__render_pause_overlay()

    def __render_arena(self):
        pygame.draw.rect(self.win, Color.GREY, self.game.arena.rect, 2)
        pygame.draw.rect(self.win, (255, 0, 0), self.game.active_level.kill_zone)

    def __render_ui(self):
        self.__render_ui_top()
        self.__render_ui_bottom()

    def __render_ui_top(self):
        ui_width = self.win.get_rect().width
        ui_height = self.game.arena.y
        ui_surface = pygame.Surface((ui_width, ui_height))
        ui_surface.fill(self.options.ui.get_primary_bg_color())
        ui_surface_rect = ui_surface.get_rect()
        padding = 30
        font_size = 36
        color_primary = self.options.ui.get_primary_text_color()

        time_spend = self.game.calculate_time()

        text_score = f'Score: {self.game.score}'
        renderText(
            ui_surface, text_score, color_primary, font_size, (padding * 2, padding)
        )

        text_time = f'{time_spend}'
        renderText(
            ui_surface, text_time, color_primary, font_size, (ui_surface_rect.width / 2, padding)
        )

        text_lives = f'Lives: {self.game.active_level.player.health}'
        renderText(
            ui_surface, text_lives, color_primary, font_size, (ui_surface_rect.width - (padding * 2), padding)
        )

        self.win.blit(ui_surface, (0, 0))

    def __render_ui_bottom(self):
        ui_width = self.win.get_rect().width
        ui_height = self.win.get_rect().height - self.game.arena.y - self.game.arena.height
        ui_surface = pygame.Surface((ui_width, ui_height))
        ui_surface.fill(self.options.ui.get_primary_bg_color())
        ui_surface_rect = ui_surface.get_rect()
        ui_dest = (0, self.game.arena.y + self.game.arena.height)
        padding = 30
        font_size = 18
        color_primary = self.options.ui.get_primary_text_color()

        text_time = f'A - "Left", D - "Right", Space - Fire, M - Mute'
        renderText(
            ui_surface, text_time, color_primary, font_size, (ui_surface_rect.width / 2, padding)
        )

        self.win.blit(ui_surface, ui_dest)

    def __render_pause_overlay(self):
        win_rect = self.win.get_rect()
        color_background = Color.BLACK.value
        color_primary = Color.WHITE.value
        font_size = 36

        pause_screen_fade = pygame.Surface(win_rect.size)
        pause_screen_fade.fill(color_background)
        pause_screen_fade.set_alpha(160)
        self.win.blit(pause_screen_fade, (0, 0))

        pause_screen_ui = pygame.Surface(win_rect.size, pygame.SRCALPHA, 32)
        pause_screen_ui.convert_alpha()
        pause_screen_ui_rect = pause_screen_ui.get_rect()

        renderText(pause_screen_ui,
                   'Press Space To Continue', color_primary, font_size,
                   (pause_screen_ui_rect.width / 2, pause_screen_ui_rect.height / 2 - 20))
        renderText(pause_screen_ui,
                   'Press Esc To Resign', color_primary, font_size,
                   (pause_screen_ui_rect.width / 2, pause_screen_ui_rect.height / 2 + 20))

        self.win.blit(pause_screen_ui, (0, 0))

    def __render_count_down_overlay(self):
        win_rect = self.win.get_rect()
        color_background = Color.BLACK.value
        color_primary = Color.WHITE.value
        font_size = 48

        pause_screen_fade = pygame.Surface(win_rect.size)
        pause_screen_fade.fill(color_background)
        pause_screen_fade.set_alpha(160)
        self.win.blit(pause_screen_fade, (0, 0))

        pause_screen_ui = pygame.Surface(win_rect.size, pygame.SRCALPHA, 32)
        pause_screen_ui.convert_alpha()
        pause_screen_ui_rect = pause_screen_ui.get_rect()

        time = self.game.active_level.get_loading_time_remaining()

        renderText(pause_screen_ui,
                   f'{time}', color_primary, font_size,
                   (pause_screen_ui_rect.width / 2, pause_screen_ui_rect.height / 2))

        self.win.blit(pause_screen_ui, (0, 0))

    def pause(self):
        self.game.stop()
        self.unloadMusic()
        self.music_file = MUSIC_PAUSE_FILE

    def unpause(self):
        self.game.start()
        self.unloadMusic()
        self.music_file = MUSIC_GAME_FILE

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game.running:
                    self.pause()
                elif not self.game.running:
                    self.game.resign()
                return

            if event.key == pygame.K_SPACE:
                if not self.game.running:
                    self.unpause()
                    return

        if self.game:
            self.game.handle_event(event)
