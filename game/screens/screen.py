from typing import Optional

import pygame

from game.game import Game
from game.options import Options
from game.utils import playMusic


class AScreen:
    def __init__(self, win, clock, options: Options, music_file):
        self.win = win
        self.clock = clock
        self.options = options
        self.music_file = music_file
        self.music_loaded = False
        self.game: Optional[Game] = None

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
            playMusic(self.options, self.music_file)
            self.music_loaded = True

    def unloadMusic(self):
        if self.music_loaded:
            self.music_loaded = False

    def handleEvent(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.options.sound.toggleMute()
                pygame.mixer.music.set_volume(self.options.sound.getVolumeMusic() / 100)
