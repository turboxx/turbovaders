import pygame

import constants
from config import Config
from game.actors.hive import Hive
from game.actors.player import Player
from game.timer import Timer
from game.ui.utils import renderText
from game.utils import loadSound

SFX_DEATH = loadSound(Config.player.sfx_death)


class LevelConfig:
    def __init__(self, hive_config):
        self.hive_config = hive_config


class Level:
    def __init__(self, game, config: LevelConfig):
        self.config = config
        self.game = game
        self.win = self.game.win
        self.clock = self.game.clock
        (player, hive, invaders, projectiles) = self.__generateStartingActors()

        # state
        self.completed = False
        self.score = 0

        # actors
        self.player = player
        self.invaders = invaders
        self.hive = hive
        self.projectiles = projectiles

        self.killZone = (game.arena.x, game.arena.height - 25, game.arena.width, 5)

        self.timer = Timer()

        # todo: delete
        self.hasLost = False
        self.hasWon = False
        self.hasEnded = False

    def __generateStartingActors(self):
        pWidth = Config.player.width

        projectiles = []
        player = Player(self, self.game.arena.x + self.game.arena.width / 2 - pWidth / 2, self.game.arena.height - 5)
        hive = Hive(self, self.config.hive_config)

        invaders = hive.spawn_level()

        return player, hive, invaders, projectiles

    def tick(self):
        self.clock.tick(constants.FPS)
        self.moveActors()
        self.checkCollisions()
        self.checkState()

    def moveActors(self):
        self.player.move()

        direction = self.hive.determineInvaderDirection()
        for invader in self.invaders:
            invader.setDirection(direction)
            invader.move()

        for projectile in self.projectiles:
            projectile.move()

    def checkCollisions(self):
        playerRect = pygame.Rect(self.player.rect)
        for projectile in self.projectiles:
            if not projectile.alive:
                continue

            pRect = pygame.Rect(projectile.rect)
            if pRect.colliderect(playerRect):
                self.player.hit()
                projectile.hit()
                self.updateScore(-1)

            for invader in self.invaders:
                if not invader.alive:
                    continue
                iRect = pygame.Rect(invader.rect)
                if pRect.colliderect(iRect):
                    invader.hit()
                    projectile.hit()
                    if not invader.alive:
                        self.updateScore(1)
                    continue

    def updateScore(self, amount: int):
        self.score += amount

        if amount >= 0:
            self.game.score += amount
            return

        # don't go negative
        if self.game.score + amount <= 0:
            self.game.score = 0
        else:
            self.game.score += amount

    def checkState(self):
        if not self.player.alive:
            SFX_DEATH.play()
            self.hasLost = True
            self.hasEnded = True
            return

        self.hive.checkDeadInvaders()
        if not self.hive.isAlive():
            self.hasWon = True
            self.hasEnded = True
            return

        killRect = pygame.Rect(self.killZone)
        if self.hive.checkReachedEnd(killRect):
            SFX_DEATH.play()
            self.hasLost = True
            self.hasEnded = True
            return

    def calculateTime(self):
        if not self.timer.time_started:
            self.timer.start()

        return self.timer.get(1)

    def renderUI(self):
        time_spend = self.calculateTime()
        text = f'Score: {self.game.score}'

        renderText(self.win, text, constants.BLACK, 36, (60, 20))
        renderText(self.win, f'{time_spend}', constants.BLACK, 36, (constants.WIDTH / 2, 20))
        renderText(self.win, f'Lives: {self.player.health}', constants.BLACK, 36, (constants.WIDTH - 60, 20))

        pygame.draw.rect(self.win, (255, 0, 0), self.killZone)

    def redrawLevel(self):
        self.renderUI()

        self.player.draw(self.win)

        for invader in self.invaders:
            invader.draw(self.win)

        for projectile in self.projectiles:
            projectile.draw(self.win)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire()
