import pygame

import constants
from game.options import Options
from game.screens.screen import AScreen
from game.ui.utils import renderText

MUSIC_GAME_FILE = 'assets/sfx/music_game.wav'
MUSIC_PAUSE_FILE = 'assets/sfx/music_pause.wav'


class ScreenGame(AScreen):
    def __init__(self, win, clock, options: Options):
        super().__init__(win, clock, options, MUSIC_GAME_FILE)

    def render(self):
        self.win.fill(constants.WHITE)
        self.game.render_game()

        if not self.game.running:
            self.renderPauseOverlay()

    def renderPauseOverlay(self):
        pause_screen_fade = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        pause_screen_fade.fill(constants.BLACK)
        pause_screen_fade.set_alpha(160)
        self.win.blit(pause_screen_fade, (0, 0))

        renderText(self.win, 'Press Space To Continue', constants.WHITE, 36,
                   (constants.WIDTH / 2, constants.HEIGHT / 2 - 20))
        renderText(self.win, 'Press Esc To Resign', constants.WHITE, 36,
                   (constants.WIDTH / 2, constants.HEIGHT / 2 + 20))

    def pause(self):
        self.game.stop()
        self.unloadMusic()
        self.music_file = MUSIC_PAUSE_FILE

        pass

    def unpause(self):
        self.game.start()
        self.unloadMusic()
        self.music_file = MUSIC_GAME_FILE

        pass

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

