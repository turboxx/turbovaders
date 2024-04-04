from random import randrange

import pygame

import constants
from config import Config
import file_utils
from game.actors.projectile import Projectile

IMG_INVADER_1 = pygame.transform.scale(pygame.image.load(file_utils.resource_path('assets/img/invader_1.png')),
                                       (50, 50))
IMG_INVADER_2 = pygame.transform.scale(pygame.image.load(file_utils.resource_path('assets/img/invade_r2.png')),
                                       (50, 50))
IMG_INVADER_3 = pygame.transform.scale(pygame.image.load(file_utils.resource_path('assets/img/invader_3.png')),
                                       (50, 50))

SFX_HIT = pygame.mixer.Sound(file_utils.resource_path('assets/sfx/sfx_hit.wav'))


class HiveConfig:
    def __init__(self, init_count: int, can_spawn: bool = False, final_count: int = 10, can_speed_up: bool = False, can_berserk: bool = False):
        self.init_count = init_count
        self.final_count = final_count
        self.can_spawn = can_spawn
        self.can_speed_up = can_speed_up
        self.can_berserk = can_berserk


class Hive:
    def __init__(self, level, config: HiveConfig):
        self.level = level
        self.config = config
        self.invaders = []
        self.alive = True

        self.moveDirection = constants.DIRECTION_RIGHT
        self.lastMoveDirection = self.moveDirection

    def spawn_invader(self, x, y):
        self.invaders.append(Invader(self.level, x, y))

    def spawn_level(self):
        (iWidth, iHeight, iColor) = Config.invader
        offsetY = self.level.game.arena.y + 10
        offsetX = self.level.game.arena.x + 10
        space_between = 10
        for i in range(self.config.init_count):
            iY = offsetY
            iX = offsetX + i * iWidth
            if i > 0:
                iX += i * space_between
            self.spawn_invader(iX, iY)

        return self.invaders

    def isAlive(self):
        return self.alive

    def checkDeadInvaders(self):
        aliveCount = len(self.getLiveInvaders())
        if aliveCount <= 0:
            self.alive = False

    def checkReachedEnd(self, end_rect: pygame.Rect):
        for invader in self.invaders:
            if not invader.alive:
                continue

            iRect = pygame.Rect(invader.rect)
            if iRect.colliderect(end_rect):
                return True

        return False

    def getLiveInvaders(self):
        return list(filter(lambda i: i.alive is True, self.invaders))

    def __speedUp(self):
        for invader in self.getLiveInvaders():
            speedIncrease = 2
            invader.speedUp(speedIncrease)

    def determineInvaderDirection(self):
        rightMost = self.invaders[0]
        leftMost = self.invaders[0]

        for invader in self.invaders:
            if not invader.alive:
                continue

            if rightMost.x < invader.x:
                rightMost = invader
            if leftMost.x > invader.x:
                leftMost = invader

        # reverse when moving down
        if self.moveDirection == constants.DIRECTION_DOWN:
            if self.lastMoveDirection == constants.DIRECTION_RIGHT:
                self.moveDirection = constants.DIRECTION_LEFT
                self.lastMoveDirection = constants.DIRECTION_LEFT
                return self.moveDirection

            if self.lastMoveDirection == constants.DIRECTION_LEFT:
                self.moveDirection = constants.DIRECTION_RIGHT
                self.lastMoveDirection = constants.DIRECTION_RIGHT
                return self.moveDirection

        if self.moveDirection == constants.DIRECTION_RIGHT and rightMost.x + rightMost.width + rightMost.vel > self.level.game.arena.x + self.level.game.arena.width:
            self.moveDirection = constants.DIRECTION_DOWN
        if self.moveDirection == constants.DIRECTION_LEFT and leftMost.x - leftMost.vel < self.level.game.arena.x:
            self.moveDirection = constants.DIRECTION_DOWN

        return self.moveDirection


class Invader:
    def __init__(self, level, x, y):
        (width, height, color) = Config.invader
        self.level = level
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 2
        self.direction = constants.DIRECTION_DOWN
        self.health = 3
        self.maxHealth = self.health
        self.alive = True
        self.canFire = False

    def hit(self):
        SFX_HIT.play()
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def setDirection(self, direction):
        self.direction = direction

    def fire(self):
        if self.canFire:
            self.level.projectiles.append(
                Projectile(self, self.x + self.width / 2, self.y + self.height + 10, constants.DIRECTION_DOWN))
            self.canFire = False

    def move(self):
        if not self.alive:
            return

        roll = randrange(1, 100)
        if roll <= 1:
            self.fire()

        if roll >= 99:
            self.canFire = True

        if self.direction == constants.DIRECTION_DOWN:
            self.y += self.vel
        if self.direction == constants.DIRECTION_LEFT:
            self.x -= self.vel
        if self.direction == constants.DIRECTION_RIGHT:
            self.x += self.vel

        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        if self.alive:
            if self.health == 3:
                img = IMG_INVADER_3.copy()
            elif self.health == 2:
                img = IMG_INVADER_2.copy()
            else:
                img = IMG_INVADER_1.copy()

            win.blit(img, self.rect)
            # pygame.draw.rect(win, color, self.rect)
        # else:
        #     pygame.draw.rect(win, (125,125,125), self.rect)

    def speedUp(self, increase: int):
        self.vel += increase
