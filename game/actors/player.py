import pygame

import constants
from config import Config
from game.actors.projectile import Projectile
from game.utils import loadSound

playerConfig = Config.player

SFX_HIT = loadSound(playerConfig.sfx_hit)
SFX_DEATH = loadSound(playerConfig.sfx_death)


class Player:
    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.width = Config.player.width
        self.height = Config.player.height
        self.color = Config.player.color
        self.rect = (x, y, self.width, self.height)
        self.vel = 3
        self.alive = True
        self.health = 3
        self.maxHealth = self.health

    def draw(self, win):
        (r, g, b) = self.color
        heathMod = self.health / self.maxHealth
        color = (int(r * heathMod), int(g * heathMod), int(b * heathMod))
        pygame.draw.rect(win, color, self.rect)

    def fire(self):
        self.level.projectiles.append(Projectile(self, self.x + self.width / 2, self.y - 10, constants.DIRECTION_UP))

    def hit(self):
        SFX_HIT.play()
        self.health -= 1
        if self.health <= 0:
            SFX_DEATH.play()
            self.alive = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.x > self.level.game.arena.x:
            self.x -= self.vel

        if keys[pygame.K_d] and self.x + self.width < self.level.game.arena.x + self.level.game.arena.width:
            self.x += self.vel

        # if keys[pygame.K_w] and self.y > self.height:
        #     self.y -= self.vel
        #
        # if keys[pygame.K_s] and self.y > 0:
        #     self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)
