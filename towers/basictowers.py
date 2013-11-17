# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.image
import pygame.transform

import os

import towers.shootytower

class GunTower(towers.shootytower.ShootyTurret):
    """
    The gun tower is a basic tower that shoots bullets.
    """

    def __init__(self, game, pos, level=1):
        super(GunTower, self).__init__(game, pos, level=level)
        head = pygame.image.load(os.path.join("images", "gun_head_0.png"))
        base = pygame.image.load(os.path.join("images", "gun_base_0.png"))
        self.setSprites(head, base)

    def getBaseDamage(self):
        return 10 # TODO: Handle upgrades and stuff.

    def getFireRate(self):
        return 5*60 # 5 per second

    def getSpread(self):
        return 10

class GatlingTower(towers.shootytower.ShootyTurret):
    """
    The gatling tower is a fairly inaccurate, low damage tower that fires extremely fast.
    """

    def __init__(self, game, pos, level=1):
        super(GatlingTower, self).__init__(game, pos, level=level)
        head = pygame.image.load(os.path.join("images", "gun_head_0.png"))
        base = pygame.image.load(os.path.join("images", "gun_base_0.png"))
        self.setSprites(head, base)

    def getBaseDamage(self):
        return 1 # TODO: Handle upgrades and stuff.

    def getFireRate(self):
        return 30*60 # 30 per second

    def getSpread(self):
        return 20

