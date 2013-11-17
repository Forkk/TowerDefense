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

    def __init__(self, enemyIdName, health=100, speed=.1):
        self.name = enemyIdName
        self.default_health = health
        self.default_speed = speed
    
    def initEntity(self, entity):
        pass
    
    def update(self, entity, elapsed):
        '''
        moves the entity and applies miscellanious updates.
        '''
        entity.move(elapsed)
        entity.applyDot(elapsed)
    