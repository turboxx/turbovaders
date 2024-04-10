from random import randrange

import pygame

from constants import Direction, Factions
from config import Config
from game.actors.aactor import AActor
from game.utils import load_and_transform_img, loadSound, get_directional_vector, get_rotation_angle
from game.weapons.basic import BasicWeapon

invaderConfig = Config.invader
invaderSize = (invaderConfig.width, invaderConfig.height)

# Images
IMG_INVADER_BASIC_HEALTHY = load_and_transform_img(invaderConfig.image_healthy, invaderSize)
IMG_INVADER_BASIC_DAMAGED = load_and_transform_img(invaderConfig.image_damaged, invaderSize)
IMG_INVADER_BASIC_DYING = load_and_transform_img(invaderConfig.image_dying, invaderSize)
# sounds
SFX_HIT = loadSound(invaderConfig.sfx_hit)


class Invader(AActor):
    def __init__(self, level, x, y):
        width = invaderConfig.width
        height = invaderConfig.height
        velocity = invaderConfig.velocity
        super().__init__(level, x, y, width, height, Factions.ENEMY, velocity)

        self.color = invaderConfig.color
        self.move_direction: Direction = Direction.DOWN
        self.face_direction: Direction = level.config.direction

        self.maxHealth = invaderConfig.max_health
        self.health = self.maxHealth
        self.score_gain = invaderConfig.score_gain
        # to avoid initial onslaught
        self.can_fire = False

        self.weapon = BasicWeapon(self)

    def _on_hit(self):
        SFX_HIT.play()
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def set_direction(self, direction):
        self.move_direction = direction

    def get_move_vector(self):
        vector = get_directional_vector(self.move_direction)
        vector.scale_to_length(self.velocity)

        return vector

    def move(self):
        if not self.alive:
            return

        self._action()

        super().move()

    def _action(self):
        roll = randrange(1, 100)

        if roll <= 1:
            self.__fire()

        if roll >= 99:
            self._reload()

    def _reload(self):
        self.can_fire = True

    def __fire(self):
        if self.can_fire:
            self.weapon.fire()
            self.can_fire = False

    def draw(self, win):
        if self.alive:
            if self.health == 3:
                img = IMG_INVADER_BASIC_DYING.copy()
            elif self.health == 2:
                img = IMG_INVADER_BASIC_DAMAGED.copy()
            else:
                img = IMG_INVADER_BASIC_HEALTHY.copy()

            win.blit(self.__rotate_img(img), self.rect)
            # pygame.draw.rect(win, color, self.rect)
        # else:
        #     pygame.draw.rect(win, (125,125,125), self.rect)

    def __rotate_img(self, img):
        angle = get_rotation_angle(self.face_direction)

        return pygame.transform.rotate(img, angle)

    def speed_up(self, increase: int):
        self.velocity += increase

    def get_bounty(self):
        return self.score_gain
