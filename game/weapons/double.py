from constants import Direction
from game.actors.aactor import AActor
from game.weapons.aweapon import AWeapon


class DoubleBarrelWeapon(AWeapon):
    def __init__(self, actor: AActor):
        super().__init__(actor)
        self.projectiles_count = 2

    def _get_projectile_position(self, projectile_number):
        vertical_offset = 5

        width_third = self.actor.width / 3
        height_third = self.actor.height / 3

        horizontal_position = width_third + width_third * projectile_number
        vertical_position = height_third + height_third * projectile_number

        if self.fire_direction == Direction.DOWN:
            return self.actor.x + horizontal_position, self.actor.y + self.actor.height + vertical_offset
        if self.fire_direction == Direction.UP:
            return self.actor.x + horizontal_position, self.actor.y - vertical_offset * 2
        if self.fire_direction == Direction.LEFT:
            return self.actor.x - vertical_offset * 2, self.actor.y + vertical_position
        if self.fire_direction == Direction.RIGHT:
            return self.actor.x + self.actor.width + vertical_offset, self.actor.y + vertical_position
