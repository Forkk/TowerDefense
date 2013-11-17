'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import pygame
import os

# The cardinal directions, used in pathfinding.
DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_EAST = 3
DIRECTION_WEST = 4
DIRECTION_NONE = 5

DIRECTION_MATRIX = {
                    DIRECTION_NORTH: (0, -1),
                    DIRECTION_SOUTH: (0, 1),
                    DIRECTION_EAST: (1, 0),
                    DIRECTION_WEST: (-1, 0),
                    DIRECTION_NONE: (0, 0)
                    }

class EnemyBase(object):
    '''
    A singleton instance of an entityType
    default_health
    default_speed
    textures (dictionary of DIRECTION -> sprite)
    '''
    # constant file path thing
    IMAGE_PATH = "images"

    def __init__(self, enemyIdName, health=100, speed=.1, resources=10, load_images=True):
        self.name = enemyIdName
        self.default_health = health
        self.default_speed = speed
        self.default_resources = resources
        if load_images:
            # If this is false, the subclass probably wants to load its own images.
            self.images = (
                           pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_1" + ".png")),
                           pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_2" + ".png")),
                           pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_3" + ".png")),
                           pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_4" + ".png"))
                           )
    
    def getImage(self, direction):
        if direction >= len(self.images) :
            return self.images[0]
        else:
            return self.images[direction]
    
    def initEntity(self, entity):
        pass
    
    def update(self, entity, elapsed):
        '''
        moves the entity and applies miscellanious updates.
        '''
        entity.move(elapsed)
        entity.applyDot(elapsed)
    
