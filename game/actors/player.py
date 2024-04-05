import pygame

import constants
from config import Config
from game.actors.actor import AActor
from game.actors.projectile import Projectile
from game.utils import loadSound, get_reverse_direction

playerConfig = Config.player

SFX_HIT = loadSound(playerConfig.sfx_hit)
SFX_DEATH = loadSound(playerConfig.sfx_death)


class Player(AActor):
    def __init__(self, level, x, y):
        width = playerConfig.width
        height = playerConfig.height
        # rotating actor
        if level.config.direction is constants.DIRECTION_RIGHT or level.config.direction is constants.DIRECTION_LEFT:
            width = playerConfig.height
            height = playerConfig.width

        velocity = playerConfig.velocity
        color = playerConfig.color

        super().__init__(level, x, y, width, height, velocity)

        self.fire_direction = get_reverse_direction(self.level.config.direction)
        self.color = color
        self.maxHealth = Config.player.max_health
        self.health = self.maxHealth

    def draw(self, win):
        (r, g, b) = self.color
        heathMod = self.health / self.maxHealth
        color = (int(r * heathMod), int(g * heathMod), int(b * heathMod))
        pygame.draw.rect(win, color, self.rect)

    def fire(self):
        (p_x, p_y) = self.__get_projectile_position()
        self.level.projectiles.append(Projectile(self, p_x, p_y, self.fire_direction))

    def __get_projectile_position(self):
        offset = 5

        if self.fire_direction == constants.DIRECTION_DOWN:
            return self.x + self.width / 2, self.y + self.height + offset
        if self.fire_direction == constants.DIRECTION_UP:
            return self.x + self.width / 2, self.y - offset * 2
        if self.fire_direction == constants.DIRECTION_LEFT:
            return self.x - offset * 2, self.y + self.height / 2
        if self.fire_direction == constants.DIRECTION_RIGHT:
            return self.x + self.width + offset, self.y + self.height / 2



    def hit(self):
        SFX_HIT.play()
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def kill(self):
        SFX_DEATH.play()
        self.alive = False

    def move(self):
        # todo remove double fetching loading
        new_position = self.calculate_new_position()
        if not self.level.game.arena.contains(new_position):
            return

        super().move()

    def get_move_vector(self):
        keys = pygame.key.get_pressed()

        vector = (0, 0)
        if self.level.config.direction is constants.DIRECTION_DOWN:
            if keys[pygame.K_a]:
                vector = (-self.velocity, 0)

            if keys[pygame.K_d]:
                vector = (self.velocity, 0)

        if self.level.config.direction is constants.DIRECTION_UP:
            if keys[pygame.K_a]:
                vector = (self.velocity, 0)

            if keys[pygame.K_d]:
                vector = (-self.velocity, 0)

        if self.level.config.direction is constants.DIRECTION_RIGHT:
            if keys[pygame.K_a]:
                vector = (0, self.velocity)

            if keys[pygame.K_d]:
                vector = (0, -self.velocity)

        if self.level.config.direction is constants.DIRECTION_LEFT:
            if keys[pygame.K_a]:
                vector = (0, -self.velocity)

            if keys[pygame.K_d]:
                vector = (0, self.velocity)


        # if keys[pygame.K_w]:
        #     vector = (0, -self.velocity)
        #
        # if keys[pygame.K_s]:
        #     vector = (0, self.velocity)

        return pygame.Vector2(vector)
