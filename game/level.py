import pygame

import constants
from config import Config
from game.actors.hive import Hive
from game.actors.player import Player
from game.actors.projectile import Projectile
from game.timer import Timer
from game.ui.utils import renderText


class LevelConfig:
    def __init__(self, hive_config, direction=constants.DIRECTION_DOWN):
        self.hive_config = hive_config
        self.direction = direction


class Level:
    def __init__(self, game, config: LevelConfig):
        self.config = config
        self.game = game
        self.win: pygame.Surface = self.game.win
        self.clock: pygame.time.Clock = self.game.clock
        (player, hive, invaders) = self.__generateStartingActors()

        # state
        self.completed = False
        self.has_lost = False
        self.has_won = False
        self.score = 0

        # actors
        self.player = player
        self.invaders = invaders
        self.hive = hive
        self.projectiles: list[Projectile] = []

        self.kill_zone = self.__create_kill_zone()

        self.timer = Timer()



    def __generateStartingActors(self):
        (p_x, p_y) = self.__get_player_starting_location()
        player = Player(self, p_x, p_y)
        hive = Hive(self, self.config.hive_config)
        invaders = hive.spawn_level()

        return player, hive, invaders

    def __get_player_starting_location(self):
        pWidth = Config.player.width
        offset = 5

        x = self.game.arena.x + self.game.arena.width / 2 - pWidth / 2
        y = self.game.arena.y + self.game.arena.height / 2 - pWidth / 2

        if self.config.direction is constants.DIRECTION_UP:
            y = self.game.arena.y + offset
        if self.config.direction is constants.DIRECTION_DOWN:
            y = self.game.arena.height - offset
        if self.config.direction is constants.DIRECTION_RIGHT:
            x = self.game.arena.width - offset
        if self.config.direction is constants.DIRECTION_LEFT:
            x = self.game.arena.x + offset

        return x, y

    def __create_kill_zone(self):
        offset = 70
        height = 5
        if self.config.direction is constants.DIRECTION_UP:
            return pygame.Rect(self.game.arena.x, self.game.arena.y + offset, self.game.arena.width, height)
        if self.config.direction is constants.DIRECTION_RIGHT:
            return pygame.Rect(self.game.arena.x + self.game.arena.width - offset, self.game.arena.y, height, self.game.arena.height)
        if self.config.direction is constants.DIRECTION_LEFT:
            return pygame.Rect(self.game.arena.x + offset, self.game.arena.y, height,
                               self.game.arena.height)
            # return pygame.Rect(self.game.arena.x, self.game.arena.y + offset, self.game.arena.width, height)

        return pygame.Rect(self.game.arena.x, self.game.arena.y + self.game.arena.height - offset, self.game.arena.width, height)

    def tick(self):
        self.clock.tick(constants.FPS)
        self.moveActors()
        self.checkCollisions()
        self.check_state()

    def moveActors(self):
        self.player.move()

        direction = self.hive.determine_invader_direction()
        for invader in self.invaders:
            invader.set_direction(direction)
            invader.move()

        for projectile in self.projectiles:
            projectile.move()

    def checkCollisions(self):
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

    def finish(self, victory: bool):
        if victory:
            self.has_won = True
        else:
            self.has_lost = True
            self.player.kill()

        self.completed = True

    def calculate_time(self):
        if not self.timer.time_started:
            self.timer.start()

        return self.timer.get(1)

    def render_ui(self):
        time_spend = self.calculate_time()
        text = f'Score: {self.game.score}'

        renderText(self.win, text, constants.BLACK, 36, (60, 20))
        renderText(self.win, f'{time_spend}', constants.BLACK, 36, (constants.WIDTH / 2, 20))
        renderText(self.win, f'Lives: {self.player.health}', constants.BLACK, 36, (constants.WIDTH - 60, 20))

        pygame.draw.rect(self.win, (255, 0, 0), self.kill_zone)

    def redraw_level(self):
        self.render_ui()

        self.player.draw(self.win)

        for invader in self.invaders:
            invader.draw(self.win)

        for projectile in self.projectiles:
            projectile.draw(self.win)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire()
