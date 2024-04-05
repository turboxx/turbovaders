import pygame

import file_utils
from file_utils import resource_path
from game.options import Options


def playMusic(options: Options, filename, loop=-1):
    # only one music can be loaded at the time
    # when play is run on already playing music it restarts
    pygame.mixer.music.load(resource_path(filename))
    pygame.mixer.music.set_volume(options.sound.getVolumeMusic() / 100)
    pygame.mixer.music.play(loop)


def loadAndTransformImg(source, size):
    img = pygame.image.load(file_utils.resource_path(source))
    return pygame.transform.scale(img, size)


def loadSound(source):
    return pygame.mixer.Sound(file_utils.resource_path(source))
