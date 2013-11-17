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
        return 10*60 # 3 per second

    def getSpread(self):
        return 10

