import pygame

import constants
import file_utils
from game.actors.projectile import Projectile

# IMG_INVADER_1 = pygame.transform.scale(pygame.image.load(utils.resource_path('assets/img/invader_1.png')), (50, 50))

SFX_HIT = pygame.mixer.Sound(file_utils.resource_path('assets/sfx/sfx_hit.wav'))
# SFX_DEATH = pygame.mixer.Sound(file_utils.resource_path('assets/sfx/sfx_death.wav'))
SFX_DEATH = SFX_HIT


class Player:
    def __init__(self, level, x, y, width, height, color):
        self.level = level
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
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
