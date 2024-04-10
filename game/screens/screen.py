from typing import Optional

import pygame

from game.game import Game
from game.options import Options
from game.utils import play_music


class AScreen:
    def __init__(self, win: pygame.Surface, clock: pygame.time.Clock, options: Options, music_file):
        self.win = win
        self.clock = clock
        self.options = options
        self.music_file = music_file
        self.music_loaded = False
        self.game: Optional[Game] = None

    def __str__(self):
        return f'{self.__class__.__name__}: music_loaded: {self.music_loaded}'

    def setGame(self, game: Game):
        self.game = game
        return self

    def load(self):
        self.loadMusic()
        return self

    def unload(self):
        self.unloadMusic()
        return self

    def loadMusic(self):
        if not self.music_loaded:
            play_music(self.options, self.music_file)
            self.music_loaded = True

    def unloadMusic(self):
        if self.music_loaded:
            self.music_loaded = False

    def handleEvent(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.options.sound.toggle_mute()
                pygame.mixer.music.set_volume(self.options.sound.get_volume_music() / 100)
            if event.key == pygame.K_n:
                self.options.ui.toggle_dark_mode()

    def render(self):
        pass
