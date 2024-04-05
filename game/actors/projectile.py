import constants
from config import Config
from game.utils import loadAndTransformImg, loadSound

projectileConfig = Config.projectile
projectileSize = (projectileConfig.width, projectileConfig.height)
IMG_PROJECTILE = loadAndTransformImg(projectileConfig.image, projectileSize)

SFX_HIT = loadSound(projectileConfig.sfx_hit)


class Projectile:
    def __init__(self, creator, x, y, direction):
        self.creator = creator
        self.level = creator.level
        self.x = x
        self.y = y
        self.direction = direction
        self.width = Config.projectile.width
        self.height = Config.projectile.height
        self.color = Config.projectile.color
        self.rect = (x, y, self.width, self.height)
        self.vel = 3
        self.alive = True

    def hit(self):
        self.alive = False

    def move(self):
        if not self.alive:
            return

        if ((self.direction is constants.DIRECTION_UP and (self.y - self.vel) <= self.level.game.arena.y)
                or (self.direction is constants.DIRECTION_DOWN and (self.y + self.vel) >= self.level.game.arena.height)):
            self.hit()
            return

        if self.direction == constants.DIRECTION_UP:
            self.y -= self.vel
        elif self.direction == constants.DIRECTION_DOWN:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        if self.alive:
            img = IMG_PROJECTILE.copy()

            win.blit(img, self.rect)
