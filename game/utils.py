import pygame

from file_utils import resource_path
from game.options import Options


def playMusic(options: Options, filename, loop=-1):
    # only one music can be loaded at the time
    # when play is run on already playing music it restarts
    pygame.mixer.music.load(resource_path(filename))
    pygame.mixer.music.set_volume(options.sound.getVolumeMusic() / 100)
    pygame.mixer.music.play(loop)
