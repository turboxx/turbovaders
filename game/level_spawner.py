import pygame

from constants import Direction
from config import Config
from game.hive import Hive

invaderConfig = Config.invader


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

    def spawn_initial_invaders(self, hive: "Hive"):
        # we care about "width" only as height is to determine the "row"
        i_width = invaderConfig.width
        i_height = invaderConfig.width
        space_between = 10

        spawn_count = hive.config.init_count
        (offset_x, offset_y, arena_offset_x, arena_offset_y) = self.__get_invaders_offset()

        arena_width = self.level.game.arena.width - arena_offset_x * 2
        if self.level.config.direction in [Direction.LEFT, Direction.RIGHT]:
            arena_width = self.level.game.arena.height - arena_offset_y * 2

        row_size = arena_width // (i_width + space_between)
        row_count = spawn_count // row_size
        remaining = spawn_count % row_size

        last_row_offset = (arena_width - remaining * (i_width + space_between)) / 2

        for row_number in range(row_count + 1):
            i_last_row_offset = 0
            row_vertical_offset = row_number * (i_height + space_between)
            if row_number >= row_count:
                i_last_row_offset = last_row_offset

            for row_item_number in range(row_size):
                # in the last row we count only to the remainder
                if row_number >= row_count and row_item_number >= remaining:
                    break

                i_width_with_space_between = row_item_number * (i_width + space_between)
                item_horizontal_offset = i_last_row_offset + i_width_with_space_between

                i_x = offset_x
                i_y = offset_y

                if self.level.config.direction is Direction.DOWN:
                    i_x = offset_x + item_horizontal_offset
                    i_y = offset_y + row_vertical_offset
                if self.level.config.direction is Direction.UP:
                    i_x = offset_x + item_horizontal_offset
                    i_y = offset_y - row_vertical_offset
                if self.level.config.direction is Direction.RIGHT:
                    i_x = offset_x + row_vertical_offset
                    i_y = offset_y - item_horizontal_offset
                if self.level.config.direction is Direction.LEFT:
                    i_x = offset_x - row_vertical_offset
                    i_y = offset_y + item_horizontal_offset

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

        return offset_x, offset_y, arena_offset_x, arena_offset_y

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
