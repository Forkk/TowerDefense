# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame

class TowerManager(object):
    """
    Class that manages the towers in the game.
    """

    def __init__(self, game):
        self.game = game
        self.towers = {}

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

    def draw(self, surface):
        """
        Draws towers on the given surface.
        """
        for pos, tower in self.towers.iteritems():
            tower.draw(surface)


