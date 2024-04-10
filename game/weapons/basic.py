from game.weapons.aweapon import AWeapon


class BasicWeapon(AWeapon):
    def __init__(self, actor):
        super().__init__(actor)
        self.projectiles_count = 1

