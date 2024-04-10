import pygame

from constants import Direction, Factions
from config import Config
from game.actors.aactor import AActor
from game.utils import load_and_transform_img, get_directional_vector, get_rotation_angle

projectileConfig = Config.projectile
projectileSize = (projectileConfig.width, projectileConfig.height)
IMG_PROJECTILE = load_and_transform_img(projectileConfig.image, projectileSize)


class Projectile(AActor):
    def __init__(self, creator, x, y, faction: Factions, direction):
        width = Config.projectile.width
        height = Config.projectile.height
        velocity = Config.projectile.velocity
        # rotate
        if direction in [Direction.RIGHT, Direction.LEFT]:
            width = Config.projectile.width
            height = Config.projectile.height

        super().__init__(creator.level, x, y, width, height, faction, velocity)

        self.creator = creator
        self.direction = direction
        self.color = Config.projectile.color

    def _on_hit(self):
        self.alive = False

    def get_move_vector(self):
        vector = get_directional_vector(self.direction)
        vector.scale_to_length(self.velocity)

        return vector

    def move(self):
        if not self.alive:
            return

        if not self.level.game.arena.contains(self.calculate_new_position()):
            self._on_hit()
            return

        super().move()

    def draw(self, win):
        if self.alive:
            img = IMG_PROJECTILE.copy()

            win.blit(self.__rotate_img(img), self.rect)

    def __rotate_img(self, img):
        angle = get_rotation_angle(self.direction)

        return pygame.transform.rotate(img, angle)
