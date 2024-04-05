import pygame

import constants

from game.actors.hive import HiveConfig
from game.arena import Arena
from game.level import Level, LevelConfig
from game.timer import Timer

levels = [
    LevelConfig(HiveConfig(4), direction=constants.DIRECTION_DOWN),
    LevelConfig(HiveConfig(2), direction=constants.DIRECTION_RIGHT),
    LevelConfig(HiveConfig(2), direction=constants.DIRECTION_UP),
    LevelConfig(HiveConfig(2), direction=constants.DIRECTION_LEFT),
]


class Game:
    def __init__(self, win: pygame.Surface, clock: pygame.time.Clock):
        self.win = win
        self.clock = clock

        self.score = 0
        self.level_count = 0
        self.timer = Timer()
        self.running = True
        self.hasEnded = False
        self.hasLost = False
        self.hasWon = False

        self.level_configs = levels
        marginVertical = 50
        marginHorizontal = 50
        self.arena = Arena((marginHorizontal, marginVertical),
                           (constants.WIDTH - marginHorizontal * 2, constants.HEIGHT - marginVertical * 2))

        self.active_level = self.__next_level()

    def __next_level(self):
        # print('Next level:', self.level_count, len(self.level_configs))
        if self.level_count < len(levels):
            level = Level(self, levels[self.level_count])
            self.active_level = level
            self.level_count += 1
            return level

        return self.active_level

    def start(self):
        self.running = True
        self.timer.resume()
        self.active_level.timer.resume()

    def stop(self):
        self.running = False
        self.timer.pause()
        self.active_level.timer.pause()

    def resign(self):
        self.running = False
        self.hasLost = True
        self.hasEnded = True

    def tick(self):
        if not self.running:
            return

        self.active_level.tick()
        # determine end of a level, either continue, die, or win
        if self.active_level.completed:
            self.hasLost = self.active_level.has_lost
            self.hasWon = self.active_level.has_won

            if self.active_level.has_won:
                if not self.__check_finished():
                    self.__next_level()
                    return

            self.hasEnded = True
            self.running = False

    def __check_finished(self):
        return self.level_count >= len(self.level_configs)

    # def calculateTime(self):
    #     # todo: it's weird the timer starts here in rendering and not in tick
    #     if not self.timer:
    #         self.timer = Timer()
    #         self.timer.start()
    #
    #     return self.timer.get(1)

    def __render_arena(self):
        pygame.draw.rect(self.win, (240, 240, 240), self.arena.rect)

    def __render_ui(self):
        pass

    def render_game(self):
        self.__render_ui()
        self.__render_arena()
        self.active_level.redraw_level()

    def handle_event(self, event):
        self.active_level.handle_event(event)
