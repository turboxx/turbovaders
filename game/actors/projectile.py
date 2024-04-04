import pygame

import constants
import file_utils
from config import Config

IMG_PROJECTILE = pygame.transform.scale(pygame.image.load(file_utils.resource_path('assets/img/projectile_1.png')), (5, 10))

SFX_HIT = pygame.mixer.Sound(file_utils.resource_path('assets/sfx/sfx_hit.wav'))


class Projectile:
    def __init__(self, creator, x, y, direction):
        (width, height, color) = Config.projectile
        self.creator = creator
        self.level = creator.level
        self.x = x
        self.y = y
        self.direction = direction
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.alive = True

    def hit(self):
        self.alive = False

    def move(self):
        if not self.alive:
            return

        if ((self.direction is constants.DIRECTION_UP and (self.y - self.vel) <= self.level.game.arena.y)
                or (self.direction is constants.DIRECTION_DOWN and (self.y + self.vel) >= self.level.game.arena.height)):
            self.hit()
            return

        if self.direction == constants.DIRECTION_UP:
            self.y -= self.vel
        elif self.direction == constants.DIRECTION_DOWN:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        if self.alive:
            img = IMG_PROJECTILE.copy()

            win.blit(img, self.rect)
