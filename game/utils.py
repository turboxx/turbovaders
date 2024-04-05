import pygame

import constants
import file_utils
from file_utils import resource_path
from game.options import Options


def get_reverse_direction(direction: str):
    if direction is constants.DIRECTION_UP:
        return constants.DIRECTION_DOWN
    if direction is constants.DIRECTION_DOWN:
        return constants.DIRECTION_UP
    if direction is constants.DIRECTION_RIGHT:
        return constants.DIRECTION_LEFT
    if direction is constants.DIRECTION_LEFT:
        return constants.DIRECTION_RIGHT


# relative left, relative right
def get_side_directions(direction: str):
    if direction is constants.DIRECTION_UP:
        return constants.DIRECTION_RIGHT, constants.DIRECTION_LEFT
    if direction is constants.DIRECTION_DOWN:
        return constants.DIRECTION_LEFT, constants.DIRECTION_RIGHT
    if direction is constants.DIRECTION_RIGHT:
        return constants.DIRECTION_UP, constants.DIRECTION_DOWN
    if direction is constants.DIRECTION_LEFT:
        return constants.DIRECTION_DOWN, constants.DIRECTION_UP


def get_relative_left(direction: str):
    if direction is constants.DIRECTION_UP:
        return constants.DIRECTION_RIGHT
    if direction is constants.DIRECTION_DOWN:
        return constants.DIRECTION_LEFT
    if direction is constants.DIRECTION_RIGHT:
        return constants.DIRECTION_UP
    if direction is constants.DIRECTION_LEFT:
        return constants.DIRECTION_DOWN


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
