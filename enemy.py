"""
enemy.py - The most basic enemy in the game.
"""

import pygame
import os
import Queue

DEFAULT_HEALTH = 100
DEFAULT_SPEED = 5 # This is in number of pixels per second

# The cardinal directions, used in pathfinding.
DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_EAST = 3
DIRECTION_WEST = 4
DIRECTION_NONE = 5

class enemy:

    """
    Initializes a new enemy at the given x and y coordinates.
    This also adds the enemy's sprite to the given sprite group.
    """
    def __init__(self, x, y, group):
        self.x = x
        self.y = y
        self.health = DEFAULT_HEALTH
        self.speed = DEFAULT_SPEED
        self.sprite = pygame.sprite.Sprite()
        self.direction = DIRECTION_NONE
        self.sprite.image = pygame.image.load(os.path.join("images", "enemy.png"))
        self.sprite.rect = pygame.Rect(self.x, self.y, self.sprite.image.get_width(),
                                       self.sprite.image.get_height())
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
        self.x += deltaX
        self.y += deltaY
        self.sprite.rect.move(deltaX, deltaY)

    """
    Figure out which direction we should go. This uses a breadth-first
    search to find the goal. Be careful, this can take a while on open maps.
    """
    def determineDirection(self, mapdata):
        # TODO: Implement this function!
        return DIRECTION_NONE


        """
        tilequeue = Queue.Queue()
        # Get the tile we're on
        tilequeue.put(mapdata.tiles[self.x][self.y])
        while(not tilequeue.empty()):
        """

    """
    Determines if an enemy is dead or not.
    """
    def enemyDead(self):
        if(self.health <= 0):
            return True
        else:
            return False
