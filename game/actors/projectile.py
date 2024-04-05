import pygame

import constants
from config import Config
from game.actors.actor import AActor
from game.utils import loadAndTransformImg

projectileConfig = Config.projectile
projectileSize = (projectileConfig.width, projectileConfig.height)
IMG_PROJECTILE = loadAndTransformImg(projectileConfig.image, projectileSize)


class Projectile(AActor):
    def __init__(self, creator, x, y, direction):
        width = Config.projectile.width
        height = Config.projectile.height
        velocity = Config.projectile.velocity
        # rotate
        if direction is constants.DIRECTION_RIGHT or direction is constants.DIRECTION_LEFT:
            width = Config.projectile.width
            height = Config.projectile.height

        super().__init__(creator.level, x, y, width, height, velocity)

        self.creator = creator
        self.direction = direction
        self.color = Config.projectile.color

    def hit(self):
        self.alive = False

    def get_move_vector(self):
        vector = (0, 0)
        if self.direction is constants.DIRECTION_DOWN:
            vector = (0, self.velocity)
        if self.direction is constants.DIRECTION_UP:
            vector = (0, -self.velocity)
        if self.direction is constants.DIRECTION_LEFT:
            vector = (-self.velocity, 0)
        if self.direction is constants.DIRECTION_RIGHT:
            vector = (self.velocity, 0)

        return pygame.Vector2(vector)

    def move(self):
        if not self.alive:
            return

        if not self.level.game.arena.contains(self.calculate_new_position()):
            self.hit()
            return

        super().move()

    def draw(self, win):
        if self.alive:
            img = IMG_PROJECTILE.copy()

            win.blit(self.__rotate_img(img), self.rect)

    def __rotate_img(self, img):
        angle = 0
        if self.direction == constants.DIRECTION_UP:
            angle = 180
        if self.direction == constants.DIRECTION_LEFT:
            angle = 270
        if self.direction == constants.DIRECTION_RIGHT:
            angle = 90

        return pygame.transform.rotate(img, angle)
