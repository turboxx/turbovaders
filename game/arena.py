import pygame


class Arena:
    def __init__(self, position, size):
        (x, y) = position
        (width, height) = size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def contains(self, rect: pygame.Rect):
        # print(rect, self.rect)
        return self.rect.contains(rect)


