from constants import Direction
from game.actors.aactor import AActor
from game.actors.projectile import Projectile


class AWeapon:
    def __init__(self, actor: AActor):
        self.actor = actor
        self.level = actor.level

        self.fire_direction = actor.fire_direction
        self.projectiles_count = 0

    def fire(self):
        for projectile_number in range(0, self.projectiles_count):
            (p_x, p_y) = self._get_projectile_position(projectile_number)
            self.level.projectiles.append(Projectile(self, p_x, p_y, self.actor.faction, self.actor.fire_direction))

    def _get_projectile_position(self, projectile_number):
        offset = 5

        if self.fire_direction == Direction.DOWN:
            return self.actor.x + self.actor.width / 2, self.actor.y + self.actor.height + offset
        if self.fire_direction == Direction.UP:
            return self.actor.x + self.actor.width / 2, self.actor.y - offset * 2
        if self.fire_direction == Direction.LEFT:
            return self.actor.x - offset * 2, self.actor.y + self.actor.height / 2
        if self.fire_direction == Direction.RIGHT:
            return self.actor.x + self.actor.width + offset, self.actor.y + self.actor.height / 2
