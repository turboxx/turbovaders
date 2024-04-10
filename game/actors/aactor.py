import pygame

from constants import Factions


class AActor:
    def __init__(self, level, x, y, width, height, faction: Factions, velocity=0):
        self.level = level
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.faction = faction
        self.velocity = velocity
        self.alive = True
        self.fire_direction = self._get_fire_direction()
        self.rect = (self.x, self.y, self.width, self.height)

    def __str__(self):
        return f'{self.__class__.__name__}: (x: {self.x}, y: {self.y}) Alive: {self.alive}'

    def get_rect(self):
        return pygame.Rect(self.rect)

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, (240, 240, 240), self.rect)

    def get_move_vector(self):
        vector = (0, 0)

        return pygame.Vector2(vector)

    def calculate_new_position(self):
        movement_vector = self.get_move_vector()
        new_x = self.x + movement_vector.x
        new_y = self.y + movement_vector.y

        return pygame.Rect(new_x, new_y, self.width, self.height)

    def move(self):
        new_position = self.calculate_new_position()

        self.y = new_position.y
        self.x = new_position.x

        self.rect = (self.x, self.y, self.width, self.height)

    def teleport(self, x: int, y: int):
        self.x = x
        self.y = y

        self.rect = (self.x, self.y, self.width, self.height)

    def hit(self, attacker: "AActor"):
        if self.__check_is_enemy_faction(attacker):
            self._on_hit()

    def __check_is_enemy_faction(self, attacker: "AActor"):
        return self.faction != attacker.faction

    def _on_hit(self):
        print('hitting AActor __on_hit')
        pass

    def _get_fire_direction(self):
        return self.level.config.direction
