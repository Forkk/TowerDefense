# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame

class TowerBase(object):
    """
    The base class for towers.
    Each tower will be a separate instance of an object inheriting from this class.
    """

    def __init__(self, game, pos, level=1):
        # Set the tower's current position.
        self.pos = pos

        # The tower's upgrade level.
        self.level = 0

        # ************* THE GAME *************
        self.game = game

    def update(self):
        """
        Updates this tower.
        This should do things such as recalculate the tower's aim, perform cooldown calculations, etc.
        """
        raise NotImplemented("update function isn't implemented.")

    def draw(self, surface, fx_surface):
        """
        Draws this tower to the given surface.
        """
        raise NotImplemented("draw function isn't implemented.")

    def getPixelPosition(self):
        """
        Gets the position of the tower in pixel coordinates.
        """
        return self.game.map.getPixelCoordinates(self.pos)

    def getPosition(self):
        """
        Gets the tower's position in tiles.
        """
        return self.pos

    def getSize(self):
        """
        Gets the size of the tower.
        Currently this can only be the size of a tile.
        """
        return self.game.map.getTileSize()

    def getCenter(self):
        """
        Gets the pixel coordinates of the center of the tower.
        """
        size = self.getSize()
        ppos = self.getPixelPosition()
        return (ppos[0] + size[0]/2, ppos[1] + size[1]/2)

