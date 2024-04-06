import pygame

from constants import Direction
from config import Config
from game.actors.hive import invaderConfig


class LevelSpawner:
    def __init__(self, level):
        self.level = level
        self.game = level.game
        self.config = level.config

    def get_player_starting_location(self):
        pWidth = Config.player.width
        pHeight = Config.player.height
        offset = 10

        # centers to be overridden
        x = self.game.arena.x + self.game.arena.width / 2 - pWidth / 2
        y = self.game.arena.y + self.game.arena.height / 2 - pWidth / 2

        if self.config.direction is Direction.UP:
            y = self.game.arena.y + offset
        if self.config.direction is Direction.DOWN:
            y = self.game.arena.y + self.game.arena.height - offset - pHeight
        if self.config.direction is Direction.RIGHT:
            x = self.game.arena.x + self.game.arena.width - offset - pHeight
        if self.config.direction is Direction.LEFT:
            x = self.game.arena.x + offset

        # print(self.game.arena, f'x: {int(x)} y: {int(y)}')

        return x, y

    def spawn_initial_invaders(self, hive):
        # we care about "width" only as height is to determine the "row"
        i_width = invaderConfig.width
        space_between = 10

        spawn_count = hive.config.init_count
        (offset_x, offset_y) = self.__get_invaders_offset()

        for i in range(spawn_count):
            i_x = offset_x
            i_y = offset_y
            i_width_with_space_between = i * (i_width + space_between)
            if self.level.config.direction is Direction.DOWN:
                i_x = offset_x + i_width_with_space_between
            if self.level.config.direction is Direction.UP:
                i_x = offset_x + i_width_with_space_between
            if self.level.config.direction is Direction.RIGHT:
                i_y = offset_y - i_width_with_space_between
            if self.level.config.direction is Direction.LEFT:
                i_y = offset_y + i_width_with_space_between

            hive.spawn_invader(i_x, i_y)

        return hive.invaders

    def __get_invaders_offset(self):
        i_width = invaderConfig.width
        i_height = invaderConfig.height

        arena_offset_x = 10
        arena_offset_y = 10

        offset_x = 0
        offset_y = 0
        if self.level.config.direction is Direction.UP:
            offset_y = self.level.game.arena.y + self.level.game.arena.height - i_height - arena_offset_y
            offset_x = self.level.game.arena.x + arena_offset_x
        if self.level.config.direction is Direction.DOWN:
            offset_y = self.level.game.arena.y + arena_offset_y
            offset_x = self.level.game.arena.x + arena_offset_x
        if self.level.config.direction is Direction.LEFT:
            offset_y = self.level.game.arena.y + arena_offset_y
            offset_x = self.level.game.arena.x + self.level.game.arena.width - i_width - arena_offset_x
        if self.level.config.direction is Direction.RIGHT:
            offset_y = self.level.game.arena.height - arena_offset_y
            offset_x = self.level.game.arena.x + arena_offset_x

        return offset_x, offset_y

    def create_kill_zone(self):
        offset = 70
        height = 5
        if self.config.direction is Direction.UP:
            return pygame.Rect(self.game.arena.x, self.game.arena.y + offset, self.game.arena.width, height)
        if self.config.direction is Direction.RIGHT:
            return pygame.Rect(self.game.arena.x + self.game.arena.width - offset, self.game.arena.y, height,
                               self.game.arena.height)
        if self.config.direction is Direction.LEFT:
            return pygame.Rect(self.game.arena.x + offset, self.game.arena.y, height,
                               self.game.arena.height)
            # return pygame.Rect(self.game.arena.x, self.game.arena.y + offset, self.game.arena.width, height)

        return pygame.Rect(self.game.arena.x, self.game.arena.y + self.game.arena.height - offset,
                           self.game.arena.width, height)
