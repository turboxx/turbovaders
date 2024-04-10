import pygame

from constants import Direction, Factions, Color
from config import Config
from game.actors.aactor import AActor
from game.utils import loadSound, get_reverse_direction, get_directional_vector, get_rotation_angle, \
    load_and_transform_img
from game.weapons.basic import BasicWeapon
from game.weapons.double import DoubleBarrelWeapon

playerConfig = Config.player
playerSize = (playerConfig.width, playerConfig.height)
IMG_PLAYER = load_and_transform_img(playerConfig.image, playerSize)
SFX_HIT = loadSound(playerConfig.sfx_hit)
SFX_DEATH = loadSound(playerConfig.sfx_death)


class Player(AActor):
    def __init__(self, level, x: int, y: int):
        width = playerConfig.width
        height = playerConfig.height
        # rotating actor
        if level.config.direction in [Direction.RIGHT, Direction.LEFT]:
            width = playerConfig.height
            height = playerConfig.width

        velocity = playerConfig.velocity
        color = playerConfig.color

        super().__init__(level, x, y, width, height, Factions.PLAYER, velocity)

        self.color = color
        self.maxHealth = Config.player.max_health
        self.health = self.maxHealth
        self.is_shielded = False

        self.weapon = BasicWeapon(self)

    def draw(self, win):
        heathMod = self.health / self.maxHealth

        img = IMG_PLAYER.copy()

        (r, g, b) = Color.WHITE
        alpha = int(255 * heathMod)
        img.fill((r, g, b, alpha), None, pygame.BLEND_RGBA_MULT)

        win.blit(self.__rotate_img(img), self.rect)

    def __rotate_img(self, img):
        angle = get_rotation_angle(self.fire_direction)

        return pygame.transform.rotate(img, angle)

    def fire(self):
        self.weapon.fire()

    def _on_hit(self):
        if self.is_shielded:
            return

        SFX_HIT.play()
        self.downgrade_weapon()
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def kill(self):
        SFX_DEATH.play()
        self.alive = False

    def heal(self):
        self.health = self.maxHealth

    def set_shield(self, on=True):
        self.is_shielded = on

    def upgrade_weapon(self):
        self.weapon = DoubleBarrelWeapon(self)

    def downgrade_weapon(self):
        self.weapon = BasicWeapon(self)

    def _get_fire_direction(self):
        return get_reverse_direction(self.level.config.direction)

    def move(self):
        # todo remove double fetching loading
        new_position = self.calculate_new_position()
        if not self.level.game.arena.contains(new_position):
            return

        super().move()

    def get_move_vector(self):
        keys = pygame.key.get_pressed()

        # arrow keys sems to be bugged or used wrong, once pressed they stay pressed
        # print(keys[pygame.K_a], keys[pygame.K_LEFT], keys[pygame.K_d], keys[pygame.K_RIGHT])

        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]

        # do not move
        if not move_right and not move_left:
            return pygame.Vector2((0, 0))

        vector = get_directional_vector(self.level.config.direction).rotate(90)
        if move_right:
            vector = vector.rotate(180)

        vector.scale_to_length(self.velocity)

        return vector

    def change_level(self, level):
        if level.config.direction in [Direction.RIGHT, Direction.LEFT]:
            self.width = playerConfig.height
            self.height = playerConfig.width
        if level.config.direction in [Direction.UP, Direction.DOWN]:
            self.width = playerConfig.width
            self.height = playerConfig.height

        self.level = level
        self.rect = (self.x, self.y, self.width, self.height)
        self.fire_direction = self._get_fire_direction()

        self.weapon.transition_level(self)
