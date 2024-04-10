import pygame

from constants import Direction
import file_utils
from file_utils import resource_path
from game.options import Options


def get_reverse_direction(direction: str):
    if direction is Direction.UP:
        return Direction.DOWN
    if direction is Direction.DOWN:
        return Direction.UP
    if direction is Direction.RIGHT:
        return Direction.LEFT
    if direction is Direction.LEFT:
        return Direction.RIGHT


# relative left, relative right
def get_side_directions(direction: Direction):
    if direction is Direction.UP:
        return Direction.RIGHT, Direction.LEFT
    if direction is Direction.DOWN:
        return Direction.LEFT, Direction.RIGHT
    if direction is Direction.RIGHT:
        return Direction.UP, Direction.DOWN
    if direction is Direction.LEFT:
        return Direction.DOWN, Direction.UP


def get_relative_left(direction: Direction):
    if direction is Direction.UP:
        return Direction.RIGHT
    if direction is Direction.DOWN:
        return Direction.LEFT
    if direction is Direction.RIGHT:
        return Direction.UP
    if direction is Direction.LEFT:
        return Direction.DOWN


def get_rotation_angle(direction: Direction):
    angle = 0
    if direction == Direction.UP:
        angle = 180
    if direction == Direction.LEFT:
        angle = 270
    if direction == Direction.RIGHT:
        angle = 90

    return angle


def get_directional_vector(direction: Direction):
    vector = (0, 0)
    if direction == Direction.DOWN:
        vector = (0, 1)
    if direction == Direction.UP:
        vector = (0, -1)
    if direction == Direction.LEFT:
        vector = (-1, 0)
    if direction == Direction.RIGHT:
        vector = (1, 0)

    return pygame.Vector2(vector)


def play_music(options: Options, filename, loop=-1):
    # only one music can be loaded at the time
    # when play is run on already playing music it restarts
    pygame.mixer.music.load(resource_path(filename))
    pygame.mixer.music.set_volume(options.sound.get_volume_music() / 100)
    pygame.mixer.music.play(loop)


def load_img(source):
    return pygame.image.load(file_utils.resource_path(source))


def load_and_transform_img(source, size):
    img = load_img(source)
    return pygame.transform.scale(img, size)


def loadSound(source):
    return pygame.mixer.Sound(file_utils.resource_path(source))
