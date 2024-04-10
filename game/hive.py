import pygame

from constants import Direction
from game.actors.invader import Invader
from game.utils import get_reverse_direction, get_side_directions, get_relative_left


class HiveConfig:
    def __init__(self, init_count: int, can_spawn: bool = False, final_count: int = 10, can_speed_up: bool = False,
                 can_berserk: bool = False):
        self.init_count = init_count
        self.final_count = final_count
        self.can_spawn = can_spawn
        self.can_speed_up = can_speed_up
        self.can_berserk = can_berserk


class Hive:
    def __init__(self, level, config: HiveConfig):
        self.level = level
        self.config = config
        self.invaders: list[Invader] = []
        self.alive = True

        self.move_direction = self.__get_init_direction()
        self.last_move_direction = self.move_direction

    def spawn_invader(self, x, y):
        self.invaders.append(Invader(self.level, x, y))

    def is_alive(self):
        return self.alive

    def check_dead_invaders(self):
        aliveCount = len(self.get_live_invaders())
        if aliveCount <= 0:
            self.alive = False

    def check_reached_end(self, end_rect: pygame.Rect):
        for invader in self.invaders:
            if not invader.alive:
                continue

            iRect = pygame.Rect(invader.rect)
            if iRect.colliderect(end_rect):
                return True

        return False

    def get_live_invaders(self):
        return list(filter(lambda i: i.alive is True, self.invaders))

    def __speed_up(self):
        for invader in self.get_live_invaders():
            speed_increase = 2
            invader.speed_up(speed_increase)

    def __get_side_invaders(self):
        rightMost = self.invaders[0]
        leftMost = self.invaders[0]

        level_direction = self.level.config.direction

        for invader in self.invaders:
            if not invader.alive:
                continue

            if level_direction is Direction.DOWN:
                if rightMost.x < invader.x:
                    rightMost = invader
                if leftMost.x > invader.x:
                    leftMost = invader

            if level_direction is Direction.UP:
                if rightMost.x > invader.x:
                    rightMost = invader
                if leftMost.x < invader.x:
                    leftMost = invader

            if level_direction is Direction.RIGHT:
                if rightMost.y < invader.y:
                    rightMost = invader
                if leftMost.y > invader.y:
                    leftMost = invader
            if level_direction is Direction.LEFT:
                if rightMost.y > invader.y:
                    rightMost = invader
                if leftMost.y < invader.y:
                    leftMost = invader

        return rightMost, leftMost

    def determine_invader_direction(self):
        (rightMost, leftMost) = self.__get_side_invaders()
        self.__bounce_and_reverse(rightMost, leftMost)

        return self.move_direction

    def __bounce_and_reverse(self, right_most, left_most):
        if self.level.config.direction is self.move_direction:
            reverse_direction = get_reverse_direction(self.last_move_direction)
            self.move_direction = reverse_direction
            self.last_move_direction = reverse_direction
            return

        (relative_left, relative_right) = get_side_directions(self.level.config.direction)
        if (self.move_direction is relative_right and
                not self.level.game.arena.contains(right_most.calculate_new_position())):
            self.move_direction = self.level.config.direction
        if (self.move_direction is relative_left and
                not self.level.game.arena.contains(left_most.calculate_new_position())):
            self.move_direction = self.level.config.direction

        return

    def __get_init_direction(self):
        return get_relative_left(self.level.config.direction)

