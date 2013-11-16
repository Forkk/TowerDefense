"""
enemy.py - The most basic enemy in the game.
"""

import pygame
import os
import Queue
import maptile

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
        
        tilequeue = Queue.Queue()
        # Get the tile we're on
        pixel_coordinates = self.getCoordinates()
        coordinates = mapdata.getTileCoordinates((pixel_coordinates[0],
                                                  pixel_coordinates[1]))
        start_tile = mapdata.tiles[coordinates[0]][coordinates[1]]
        start_tile.visited = True
        tilequeue.put(start_tile)
        while(not tilequeue.empty()):
            tile = tilequeue.get()
            tile.visited = True
            if(tile.type == maptile.DESTINATION):
                # Go backwards until we hit the tile before the start
                while(tile.parent != None and tile.parent != start_tile):
                    tile = tile.parent
                # Figure out the direction
                retval = self.findDirection(start_tile, tile)
                # Clear the tile list of parent and visited status
                for tilelist in mapdata.tiles:
                    for curr in tilelist:
                        curr.visited = False
                        curr.parent = None
                return retval
            else:
                # Get the row and column numbers
                # Queue the neighboring tiles
                self.addtoQueue(tilequeue, tile.x-1, tile.y, mapdata, tile)
                self.addtoQueue(tilequeue, tile.x+1, tile.y, mapdata, tile)
                self.addtoQueue(tilequeue, tile.x, tile.y+1, mapdata, tile)
                self.addtoQueue(tilequeue, tile.x, tile.y-1, mapdata, tile)
        
                

    """
    Add the tile to the queue if the coordinates given are valid
    and if the tile hasn't been visited yet.
    """
    def addtoQueue(self, queue, x, y, mapdata, parent):
        # Make sure the coordinates are valid
        mapsize = mapdata.getMapSize()
        if(x >= 0 and x < mapdata.numColumns and y >= 0 and y < mapdata.numRows):
            tile = mapdata.tiles[x][y]
            # If this tile hasn't been visited yet, and it's not a plot, add it
            if(not tile.visited and tile.type != maptile.PLOT):
                # Update the parent
                tile.parent = parent
                queue.put(tile)

    """
    Find the direction from the first tile to the second tile.
    The tiles have to be adjacent for this to work.
    """
    def findDirection(self, first_tile, second_tile):
        if(first_tile.x > second_tile.x):
            return DIRECTION_WEST
        elif(first_tile.x < second_tile.x):
            return DIRECTION_EAST
        elif(first_tile.y > second_tile.y):
            return DIRECTION_NORTH
        elif(first_tile.y < second_tile.y):
            return DIRECTION_SOUTH
        else:
            return DIRECTION_NONE
        

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

    """
    Returns true if the enemy is at the destination.
    """
    def atDestination(self, mapdata):
        coordinates = self.getCoordinates()
        tile_number = mapdata.getTileCoordinates(coordinates)
        if(mapdata.tiles[tile_number[0]][tile_number[1]].type == maptile.DESTINATION):
            return True
        else:
            return False

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
    
