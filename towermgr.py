# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.draw

import towers.shotline
import towers.towertypes
import towers.guntower

import math

class TowerManager(object):
    """
    Class that manages the towers in the game.
    """

    def __init__(self, game):
        self.game = game
        self.towers = {}

        # Shot lines is a list of lines representing shots fired by turrets.
        self.shot_lines = []

        self.towerTypes = [
                towers.towertypes.TowerType("Gun Tower", towers.guntower.GunTower, 50, description="A basic, fast firing, low damage tower."),
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

    def addShotLine(self, line):
        """
        Adds a new shot line from the given origin to the given endpoint.
        """
        self.shot_lines += [line]

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

        surface.lock()
        for line in self.shot_lines:
            # Fade the lines.
            line.alpha -= line.fade_rate
            if line.alpha <= 0: self.shot_lines.remove(line)
            else: pygame.draw.line(fx_surface, (255, 255, 0, line.alpha), line.origin, line.end, 2)
        surface.unlock()

