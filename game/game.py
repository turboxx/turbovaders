import pygame

from constants import Direction

from game.actors.hive import HiveConfig
from game.arena import Arena
from game.level import Level, LevelConfig
from game.timer import Timer

levels = [
    LevelConfig(HiveConfig(4), direction=Direction.DOWN),
    LevelConfig(HiveConfig(2), direction=Direction.RIGHT),
    LevelConfig(HiveConfig(2), direction=Direction.UP),
    LevelConfig(HiveConfig(2), direction=Direction.LEFT),
]


class Game:
    def __init__(self, win: pygame.Surface, clock: pygame.time.Clock):
        self.win = win
        self.clock = clock

        self.score = 0
        self.level_count = 0
        self.timer = Timer()
        self.running = True
        self.has_ended = False
        self.has_lost = False
        self.has_won = False

        self.level_configs = levels

        self.arena = self.__create_arena()

        self.active_level = self.__next_level()

    def __next_level(self):
        # print('Next level:', self.level_count, len(self.level_configs))
        if self.level_count < len(levels):
            level = Level(self, levels[self.level_count])
            self.active_level = level
            self.level_count += 1
            self.timer.pause()

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
        self.has_lost = True
        self.has_ended = True

    def calculate_time(self):
        if not self.timer.time_started:
            return 0

        return self.timer.get(1)

    def tick(self):
        if not self.running:
            return

        self.active_level.tick()

        if self.active_level.loaded:
            # for first level
            self.timer.start()
            # for level transitions
            self.timer.resume()

        # determine end of a level, either continue, die, or win
        if self.active_level.completed:
            self.has_lost = self.active_level.has_lost
            self.has_won = self.active_level.has_won

            if self.active_level.has_won:
                if not self.__check_finished():
                    self.__next_level()
                    return

            self.has_ended = True
            self.running = False

    def __check_finished(self):
        return self.level_count >= len(self.level_configs)

    def __create_arena(self):
        margin_vertical = 50
        margin_horizontal = 50
        win_rect = self.win.get_rect()

        return Arena((margin_horizontal, margin_vertical),
                     (win_rect.width - margin_horizontal * 2, win_rect.height - margin_vertical * 2))

    def render_game(self):
        self.active_level.render()

    def handle_event(self, event):
        self.active_level.handle_event(event)
