# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.draw
import pygame.image

import towers.towertypes

from towertypes import TowerType
from towers.shootytower import ShootyTower, ShootyTurret, shootyTowerStats

import os
import math

class TowerManager(object):
    """
    Class that manages the towers in the game.
    """

    def __init__(self, game):
        self.game = game
        self.towers = {}

        # Load tower sprites.
        gun_tower_head = pygame.image.load(os.path.join("images", "gun_head_0.png"))
        gun_tower_base = pygame.image.load(os.path.join("images", "gun_base_0.png"))

        self.towerTypes = [
                TowerType(name="Gun Tower", tclass=ShootyTurret, cost=50, description="A basic, fast firing, low damage tower.",
                          stats=shootyTowerStats(damage=4, rate=5*60, spread=12),
                          sprites={"head": gun_tower_head, "base": gun_tower_base}),

                TowerType(name="Gatling Tower", tclass=ShootyTurret, cost=100,
                          description="Fires exremely fast, but has low damage and accuracy.",
                          stats=shootyTowerStats(damage=1, rate=20*60, spread=24),
                          sprites={"head": gun_tower_head, "base": gun_tower_base}),
                ]
        

    def getTowerTypes(self):
        """
        Returns a list of available tower types.
        """
        return self.towerTypes

    def addTower(self, tower):
        """
        Adds the given tower to the game.
        """
        if not tower.getPosition() in self.towers:
            self.towers[tower.getPosition()] = tower

    def removeTower(self, coords):
        """
        Removes the tower at the given coordinates.
        """
        self.towers[coords] = None

    def getTowerAt(self, pos):
        """
        Gets the tower at the given position.
        """
        if pos in self.towers: return self.towers[pos]
        else: return None

    def update(self):
        """
        Updates all the towers.
        """
        for pos, tower in self.towers.iteritems():
            if pos != tower.getPosition():
                # OH GOD OH GOD WHAT HAPPENED!? EVERYTHING IS BAD! OH CRAP!
                print("Tower position key didn't match tower position! Correcting...")
                tower.pos = pos
            tower.update()

    def draw(self, surface, fx_surface):
        """
        Draws towers and effects on the given surfaces.
        """
        for pos, tower in self.towers.iteritems():
            tower.draw(surface, fx_surface)

