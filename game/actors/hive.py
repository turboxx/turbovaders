from random import randrange

import pygame

from constants import Direction, Factions
from config import Config
from game.actors.aactor import AActor
from game.utils import load_and_transform_img, loadSound, get_reverse_direction, get_side_directions, get_relative_left, \
    get_directional_vector, get_rotation_angle
from game.weapons.basic import BasicWeapon

invaderConfig = Config.invader
invaderSize = (invaderConfig.width, invaderConfig.height)

# Images
IMG_INVADER_BASIC_HEALTHY = load_and_transform_img(invaderConfig.image_healthy, invaderSize)
IMG_INVADER_BASIC_DAMAGED = load_and_transform_img(invaderConfig.image_damaged, invaderSize)
IMG_INVADER_BASIC_DYING = load_and_transform_img(invaderConfig.image_dying, invaderSize)
# sounds
SFX_HIT = loadSound(invaderConfig.sfx_hit)


class HiveConfig:
    def __init__(self, init_count: int, can_spawn: bool = False, final_count: int = 10, can_speed_up: bool = False,
                 can_berserk: bool = False):
        self.init_count = init_count
        self.final_count = final_count
        self.can_spawn = can_spawn
        self.can_speed_up = can_speed_up
        self.can_berserk = can_berserk


class Hive:
    def __init__(self, level, config: HiveConfig):
        self.level = level
        self.config = config
        self.invaders: list[Invader] = []
        self.alive = True

        self.move_direction = self.__get_init_direction()
        self.last_move_direction = self.move_direction

    def spawn_invader(self, x, y):
        self.invaders.append(Invader(self.level, x, y))

    def is_alive(self):
        return self.alive

    def check_dead_invaders(self):
        aliveCount = len(self.get_live_invaders())
        if aliveCount <= 0:
            self.alive = False

    def check_reached_end(self, end_rect: pygame.Rect):
        for invader in self.invaders:
            if not invader.alive:
                continue

            iRect = pygame.Rect(invader.rect)
            if iRect.colliderect(end_rect):
                return True

        return False

    def get_live_invaders(self):
        return list(filter(lambda i: i.alive is True, self.invaders))

    def __speed_up(self):
        for invader in self.get_live_invaders():
            speed_increase = 2
            invader.speed_up(speed_increase)

    def __get_side_invaders(self):
        rightMost = self.invaders[0]
        leftMost = self.invaders[0]

        level_direction = self.level.config.direction

        for invader in self.invaders:
            if not invader.alive:
                continue

            if level_direction is Direction.DOWN:
                if rightMost.x < invader.x:
                    rightMost = invader
                if leftMost.x > invader.x:
                    leftMost = invader

            if level_direction is Direction.UP:
                if rightMost.x > invader.x:
                    rightMost = invader
                if leftMost.x < invader.x:
                    leftMost = invader

            if level_direction is Direction.RIGHT:
                if rightMost.y < invader.y:
                    rightMost = invader
                if leftMost.y > invader.y:
                    leftMost = invader
            if level_direction is Direction.LEFT:
                if rightMost.y > invader.y:
                    rightMost = invader
                if leftMost.y < invader.y:
                    leftMost = invader

        return rightMost, leftMost

    def determine_invader_direction(self):
        (rightMost, leftMost) = self.__get_side_invaders()
        self.__bounce_and_reverse(rightMost, leftMost)

        return self.move_direction

    def __bounce_and_reverse(self, right_most, left_most):
        if self.level.config.direction is self.move_direction:
            reverse_direction = get_reverse_direction(self.last_move_direction)
            self.move_direction = reverse_direction
            self.last_move_direction = reverse_direction
            return

        (relative_left, relative_right) = get_side_directions(self.level.config.direction)
        if (self.move_direction is relative_right and
                not self.level.game.arena.contains(right_most.calculate_new_position())):
            self.move_direction = self.level.config.direction
        if (self.move_direction is relative_left and
                not self.level.game.arena.contains(left_most.calculate_new_position())):
            self.move_direction = self.level.config.direction

        return

    def __get_init_direction(self):
        return get_relative_left(self.level.config.direction)


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

    def __get_projectile_position(self):
        offset = 10

        if self.fire_direction == Direction.DOWN:
            return self.x + self.width / 2, self.y + self.height + offset
        if self.fire_direction == Direction.UP:
            return self.x + self.width / 2, self.y - offset
        if self.fire_direction == Direction.LEFT:
            return self.x - offset, self.y + self.height / 2
        if self.fire_direction == Direction.RIGHT:
            return self.x + self.width + offset, self.y + self.height / 2

    def get_move_vector(self):
        vector = get_directional_vector(self.move_direction)
        vector.scale_to_length(self.velocity)

        return vector

    def move(self):
        if not self.alive:
            return

        self.__action()

        super().move()

    def __action(self):
        roll = randrange(1, 100)

        if roll <= 1:
            self.__fire()

        if roll >= 99:
            self.__reload()

    def __reload(self):
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
