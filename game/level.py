import pygame
import time

from constants import Direction, FPS
from game.actors.hive import Hive
from game.actors.player import Player
from game.actors.projectile import Projectile
from game.level_spawner import LevelSpawner
from game.timer import Timer


class LevelConfig:
    def __init__(self, hive_config, direction=Direction.DOWN):
        self.hive_config = hive_config
        self.direction = direction


class Level:
    def __init__(self, game, config: LevelConfig):
        self.config = config
        self.game = game
        self.win: pygame.Surface = self.game.win
        self.clock: pygame.time.Clock = self.game.clock

        self.spawner = LevelSpawner(self)

        # state
        self.loaded = False
        self.completed = False
        self.has_lost = False
        self.has_won = False
        self.score = 0

        (player, hive, invaders) = self.__generateStartingActors()
        self.kill_zone = self.spawner.create_kill_zone()

        # actors
        self.player = player
        self.invaders = invaders
        self.hive = hive
        self.projectiles: list[Projectile] = []

        self.timer = Timer()

        self.loading_delay = 3
        self.loading_start_time = None

    def __generateStartingActors(self):
        (p_x, p_y) = self.spawner.get_player_starting_location()

        player = Player(self, p_x, p_y)
        hive = Hive(self, self.config.hive_config)
        invaders = self.spawner.spawn_initial_invaders(hive)

        return player, hive, invaders

    def tick(self):
        self.clock.tick(FPS)
        if not self.loaded:
            self.__check_loaded()
            return

        self.move_actors()
        self.check_collisions()
        self.check_state()

    def move_actors(self):
        self.player.move()

        direction = self.hive.determine_invader_direction()
        for invader in self.invaders:
            invader.set_direction(direction)
            invader.move()

        for projectile in self.projectiles:
            projectile.move()

    def check_collisions(self):
        playerRect = pygame.Rect(self.player.rect)
        for projectile in self.projectiles:
            if not projectile.alive:
                continue

            pRect = projectile.get_rect()
            if pRect.colliderect(playerRect):
                self.player.hit()
                projectile.hit()
                self.update_score(-1)

            for invader in self.invaders:
                if not invader.alive:
                    continue

                iRect = invader.get_rect()
                if pRect.colliderect(iRect):
                    invader.hit()
                    projectile.hit()
                    if not invader.alive:
                        self.update_score(invader.get_bounty())
                    continue

    def update_score(self, amount: int):
        self.score += amount
        # don't go negative
        self.game.score = max(self.game.score + amount, 0)

    def check_state(self):
        # player dead or invaders reached end
        if not self.player.alive or self.hive.check_reached_end(self.kill_zone):
            self.finish(False)
            return

        self.hive.check_dead_invaders()
        if not self.hive.is_alive():
            self.finish(True)
            return

    def __check_loaded(self):
        if not self.loading_start_time:
            self.loading_start_time = time.perf_counter()
            return

        if self.get_loading_time_remaining() <= 0:
            self.loaded = True

    def get_loading_time_remaining(self):
        if not self.loading_start_time:
            self.loading_start_time = time.perf_counter()

        return max(self.loading_delay - int(time.perf_counter() - self.loading_start_time), 0)

    def finish(self, victory: bool):
        if victory:
            self.has_won = True
        else:
            self.has_lost = True
            self.player.kill()

        self.completed = True

    def render(self):
        self.player.draw(self.win)

        for invader in self.invaders:
            invader.draw(self.win)

        for projectile in self.projectiles:
            projectile.draw(self.win)

    def handle_event(self, event):
        if not self.loaded:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire()
