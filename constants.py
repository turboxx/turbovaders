from enum import Enum

WIDTH = 500
HEIGHT = 500
FPS = 60

STATE_MENU = 'state_menu'
STATE_GAME = 'state_game'
STATE_RESULT = 'state_result'


# inheriting from str to avoid calling .value everywhere
class Direction(str, Enum):
    LEFT = 'direction_left'
    RIGHT = 'direction_right'
    DOWN = 'direction_down'
    UP = 'direction_up'


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Factions(str, Enum):
    PLAYER = 'faction_player'
    ENEMY = 'faction_enemy'
