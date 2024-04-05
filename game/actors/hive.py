from random import randrange

import pygame

import constants
from config import Config
from game.actors.actor import AActor
from game.actors.projectile import Projectile
from game.utils import loadAndTransformImg, loadSound, get_reverse_direction, get_side_directions, get_relative_left

invaderConfig = Config.invader
invaderSize = (invaderConfig.width, invaderConfig.height)

# Images
IMG_INVADER_BASIC_HEALTHY = loadAndTransformImg(invaderConfig.image_healthy, invaderSize)
IMG_INVADER_BASIC_DAMAGED = loadAndTransformImg(invaderConfig.image_damaged, invaderSize)
IMG_INVADER_BASIC_DYING = loadAndTransformImg(invaderConfig.image_dying, invaderSize)
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

    def spawn_level(self):
        iWidth = invaderConfig.width
        space_between = 10

        if self.level.config.direction is constants.DIRECTION_DOWN:
            offsetY = self.level.game.arena.y + 10
            offsetX = self.level.game.arena.x + 10
            for i in range(self.config.init_count):
                iY = offsetY
                iX = offsetX + i * iWidth
                if i > 0:
                    iX += i * space_between
                self.spawn_invader(iX, iY)

        if self.level.config.direction is constants.DIRECTION_UP:
            offsetY = self.level.game.arena.height - 10
            offsetX = self.level.game.arena.x + 10
            for i in range(self.config.init_count):
                iY = offsetY
                iX = offsetX + i * iWidth
                if i > 0:
                    iX += i * space_between
                self.spawn_invader(iX, iY)

        if self.level.config.direction is constants.DIRECTION_RIGHT:
            offsetY = self.level.game.arena.height - 10
            offsetX = self.level.game.arena.x + 10
            for i in range(self.config.init_count):
                iX = offsetX
                iY = offsetY - i * iWidth
                if i > 0:
                    iY -= i * space_between
                self.spawn_invader(iX, iY)

        if self.level.config.direction is constants.DIRECTION_LEFT:
            offsetY = self.level.game.arena.y + 10
            offsetX = self.level.game.arena.width - 10
            for i in range(self.config.init_count):
                iX = offsetX
                iY = offsetY + i * iWidth
                if i > 0:
                    iY += i * space_between
                self.spawn_invader(iX, iY)

        return self.invaders

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
        is_side_way = level_direction is constants.DIRECTION_LEFT or level_direction is constants.DIRECTION_RIGHT

        for invader in self.invaders:
            if not invader.alive:
                continue

            if level_direction is constants.DIRECTION_DOWN:
                if rightMost.x < invader.x:
                    rightMost = invader
                if leftMost.x > invader.x:
                    leftMost = invader

            if level_direction is constants.DIRECTION_UP:
                if rightMost.x > invader.x:
                    rightMost = invader
                if leftMost.x < invader.x:
                    leftMost = invader

            if level_direction is constants.DIRECTION_RIGHT:
                if rightMost.y < invader.y:
                    rightMost = invader
                if leftMost.y > invader.y:
                    leftMost = invader
            if level_direction is constants.DIRECTION_LEFT:
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
        print(relative_left, relative_right)
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
        super().__init__(level, x, y, width, height, velocity)

        self.color = invaderConfig.color
        self.move_direction = constants.DIRECTION_DOWN
        self.face_direction = level.config.direction
        self.fire_direction = level.config.direction

        self.maxHealth = invaderConfig.max_health
        self.health = self.maxHealth
        self.score_gain = invaderConfig.score_gain
        # to avoid initial onslaught
        self.canFire = False

    def hit(self):
        SFX_HIT.play()
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def set_direction(self, direction):
        self.move_direction = direction

    def fire(self):
        if self.canFire:
            (p_x, p_y) = self.__get_projectile_position()
            self.level.projectiles.append(
                Projectile(self, p_x, p_y, self.fire_direction))
            self.canFire = False

    def __get_projectile_position(self):
        offset = 10

        if self.fire_direction == constants.DIRECTION_DOWN:
            return self.x + self.width / 2, self.y + self.height + offset
        if self.fire_direction == constants.DIRECTION_UP:
            return self.x + self.width / 2, self.y - offset
        if self.fire_direction == constants.DIRECTION_LEFT:
            return self.x - offset, self.y + self.height / 2
        if self.fire_direction == constants.DIRECTION_RIGHT:
            return self.x + self.width + offset, self.y + self.height / 2

    def get_move_vector(self):
        vector = (0, 0)
        if self.move_direction == constants.DIRECTION_DOWN:
            vector = (0, self.velocity)
        if self.move_direction == constants.DIRECTION_UP:
            vector = (0, -self.velocity)
        if self.move_direction == constants.DIRECTION_LEFT:
            vector = (-self.velocity, 0)
        if self.move_direction == constants.DIRECTION_RIGHT:
            vector = (self.velocity, 0)

        return pygame.Vector2(vector)

    def move(self):
        if not self.alive:
            return

        roll = randrange(1, 100)
        if roll <= 1:
            self.fire()

        if roll >= 99:
            self.canFire = True

        super().move()

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
        angle = 0
        if self.face_direction == constants.DIRECTION_UP:
            angle = 180
        if self.face_direction == constants.DIRECTION_LEFT:
            angle = 270
        if self.face_direction == constants.DIRECTION_RIGHT:
            angle = 90

        return pygame.transform.rotate(img, angle)

    def speed_up(self, increase: int):
        self.velocity += increase

    def get_bounty(self):
        return self.score_gain
