"""
gamemap.py - Definition of the Map class, which represents the game's map in
memory and contains functions for adding towers and enemies.
"""

import os
import maptile
import pygame

"""
The size of each tile image, in pixels, from the images folder.
This is NOT the size on screen, the tiles are scaled to fit.
"""
TILE_SIZE = 300

class GameMap:

    """
    Constructor for the map class. This is called when a map is
    instantiated (declared in a program). This constructor requires
    the name of the map, which corresponds to a .txt file in the
    Maps directory.

    The map files are formatted as follows: The first integer is the
    number of rows in the map, and the second integer is the number
    of columns. The remaining characters represent the map itself:
    # = Spot where towers can be placed (and no enemies can step on)
    . = Spot where enemies can step on (and no towers can be placed)
    S = Where the enemies start coming in
    D = Where the enemies leave the map (their objective).
    """
    def __init__(self, mapname):
        
        # Read the file in the maps directory with the given name, line by line.
        # The "with" keyword opens the file while handling any exceptions.
        with open(os.path.join("Maps", mapname + ".txt"), "r") as file:
            for index, line in enumerate(file):
                # If this is the first line, we store it as numRows
                if(index == 0):
                    self.numRows = int(line)
                # If this is the second line, we store it as numColumns
                # and initialize the tile list
                elif(index == 1):
                    self.numColumns = int(line)
                    # The tile list is a 2 dimensional list
                    self.tiles = [[None for idx in range(0, self.numColumns)]
                                  for idx in range(0, self.numRows)]
                #Otherwise we read the line
                else:
                    # Put the line into the tile array
                    for x in range(0, self.numColumns):
                        self.tiles[x][index-2] = maptile.Tile(line[x], x, index-2)
            # Add the tiles to a sprite group
            self.spritegroup = pygame.sprite.Group()
            for tilelist in self.tiles:
                for tile in tilelist:
                    tile.getSprite(self.spritegroup)
            # Store a surface in the object (we need this for scaling later)
            self.tileSurface = None
      

    """
    Draws the map to the screen (passed in as a surface).
    """
    def draw(self, surface):
        # We need to scale the map to the size of the tiles. For that we
        # store a surface and use the transform operation in Pygame.
        if(self.tileSurface == None): # Initialize it
            self.tileSurface = pygame.Surface((self.numColumns*TILE_SIZE, self.numRows*TILE_SIZE))
            self.spritegroup.draw(self.tileSurface)
            newSize = (surface.get_width(), surface.get_height())
            self.tileSurface = pygame.transform.scale(self.tileSurface, newSize)
        # Blit this surface onto the given one (which draws it)
        surface.blit(self.tileSurface, (0,0))

    """
    Updates the map. Currently this does nothing.
    """
    def update(self):
        return
            
        
        
        

        
        
        
