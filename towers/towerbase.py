# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame

from copy import deepcopy

class TowerStats(object):
    """
    Base class for tower stats.
    This class determines a tower's base stats such as damage, fire rate, etc.
    """
    def __init__(self, stat_dict={}):
        self.stat_dict = stat_dict
        self.change_callbacks = []

    def __len__(self):
        return len(self.stat_dict)

    def __getitem__(self, key):
        return self.stat_dict[key]

    def __setitem__(self, key, value):
        self.stat_dict[key] = value
        self.changed(key)

    def __delitem__(self, key):
        del self.stat_dict[key]
        self.changed(key)

    def __contains__(self, item):
        return item in self.stat_dict

    def changed(self, key):
        """
        Calls all the change callbacks.
        """
        [func(self, key) for func in self.change_callbacks if func is not None]

    def addChangeListener(self, func):
        """
        Calls the given function when a value changes.
        The change listeners will be called whenever a value changes or is removed.
        """
        self.change_callbacks.append(func)
    
    def removeChangeListener(self, func):
        """
        Stops calling the given function when a value changes.
        """
        self.change_callbacks.remove(func)

    def copy(self):
        """
        Returns a copy of this stats object.
        The copy will not have any of this object's change listeners.
        """
        return TowerStats(deepcopy(self.stat_dict))


class TowerBase(object):
    """
    The base class for towers.
    Each tower will be a separate instance of an object inheriting from this class.
    """

    def __init__(self, game, pos, tower_type):
        # Set the tower's current position.
        self.pos = pos

        # ************* THE GAME *************
        self.game = game

        # Copy the base stats
        self.stats = tower_type.base_stats.copy()

        # Set the tower type.
        self.tower_type = tower_type

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

    def getStats(self):
        """
        Gets a tower's stats.
        """
        return self.stats

