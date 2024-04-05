import yaml

import file_utils

with open(file_utils.resource_path("config.yml"), 'r') as file:
    configFileData: dict = yaml.safe_load(file)

configPlayer = configFileData['config']['actors']['player']


class ConfigPlayer:
    width: int = configPlayer['width']
    height: int = configPlayer['height']
    color: tuple[int, int, int] = configPlayer['color']
    velocity: int = configPlayer['velocity']
    max_health: int = configPlayer['max_health']
    sfx_hit: str = configPlayer['sfx']['hit']
    sfx_death: str = configPlayer['sfx']['death']


configInvaderBasic = configFileData['config']['actors']['invaders']['basic']


class ConfigInvader:
    width: int = configInvaderBasic['width']
    height: int = configInvaderBasic['height']
    color: tuple[int, int, int] = configInvaderBasic['color']
    velocity: int = configInvaderBasic['velocity']
    max_health: int = configInvaderBasic['max_health']
    score_gain: int = configInvaderBasic['score_gain']
    image_healthy: str = configInvaderBasic['images']['healthy']
    image_damaged: str = configInvaderBasic['images']['damaged']
    image_dying: str = configInvaderBasic['images']['dying']
    sfx_hit: str = configInvaderBasic['sfx']['hit']


configProjectileBasic = configFileData['config']['actors']['projectiles']['basic']


class ConfigProjectile:
    width: int = configProjectileBasic['width']
    height: int = configProjectileBasic['height']
    color: tuple[int, int, int] = configProjectileBasic['color']
    velocity: int = configProjectileBasic['velocity']
    image: str = configProjectileBasic['image']
    sfx_hit: str = configProjectileBasic['sfx']['hit']


class Config:
    # width, height
    player = ConfigPlayer
    invader = ConfigInvader
    projectile = ConfigProjectile
