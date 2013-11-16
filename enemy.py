"""
enemy.py - The most basic enemy in the game.
"""

import pygame
import os
import Queue

DEFAULT_HEALTH = 100
DEFAULT_SPEED = 0.1 # This is in number of pixels per second

# The cardinal directions, used in pathfinding.
DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_EAST = 3
DIRECTION_WEST = 4
DIRECTION_NONE = 5

class Enemy:

    """
    Initializes a new enemy at the given x and y coordinates.
    This also adds the enemy's sprite to the given sprite group.
    """
    def __init__(self, x, y, group, size):
        self.health = DEFAULT_HEALTH
        self.speed = DEFAULT_SPEED
        self.sprite = pygame.sprite.Sprite()
        self.direction = DIRECTION_NONE
        self.sprite.image = pygame.image.load(os.path.join("images", "enemy.png"))
        self.sprite.image = pygame.transform.scale(self.sprite.image, size)
        self.sprite.rect = pygame.Rect(x, y, size[0], size[1])
        group.add(self.sprite)

    """
    Update the sprite. The time_elapsed parameter is how much time
    has passed since the last update of this sprite. The mapdata
    parameter is a map object.
    """
    def update(self, time_elapsed, mapdata):
        # Find the direction we should go
        self.direction = self.determineDirection(mapdata)
        deltaY = 0
        deltaX = 0
        # Update depending on the current direction
        if(self.direction == DIRECTION_NORTH):
            deltaY = -self.speed*time_elapsed # Go up the screen
        elif(self.direction == DIRECTION_SOUTH):
            deltaY = self.speed*time_elapsed
        elif(self.direction == DIRECTION_WEST):
            deltaX =-self.speed*time_elapsed
        elif(self.direction == DIRECTION_EAST):
            deltaX = self.speed*time_elapsed
        # If the direction is NONE, do nothing

        # Update the coordinates and rectangle
        self.sprite.rect = self.sprite.rect.move(deltaX, deltaY)

    """
    Figure out which direction we should go. This uses a breadth-first
    search to find the goal. Be careful, this can take a while on open maps.
    """
    def determineDirection(self, mapdata):
        # TODO: Implement this function!
        return DIRECTION_SOUTH


        """
        tilequeue = Queue.Queue()
        # Get the tile we're on
        tilequeue.put(mapdata.tiles[self.x][self.y])
        while(not tilequeue.empty()):
        """

    """
    Determines if an enemy is dead or not.
    """
    def dead(self):
        if(self.health <= 0):
            return True
        else:
            return False

    """
    Determines if the enemy is offscreen or not. This only
    returns true if all parts of the enemy are offscreen.
    """
    def offscreen(self, mapdata):
        tilesize = mapdata.getTileSize()
        mapsize = mapdata.getMapSize()
        coordinates = self.getCoordinates()
        if(coordinates[0] < -tilesize[0] or coordinates[0] > mapsize[0]):
            return True
        elif(coordinates[1] < -tilesize[1] or coordinates[1] > mapsize[1]):
            return True
        else:
            return False

    def getCoordinates(self):
        return (self.sprite.rect.left, self.sprite.rect.top)

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
    
