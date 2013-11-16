'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import pygame
import os

class EnemyType(object):
    '''
    A singleton instance of an entityType
    default_health
    default_speed
    textures (dictionary of DIRECTION -> sprite)
    '''
    # constant file path thing
    IMAGE_PATH = "images"

    def __init__(self, enemyIdName, health=100, speed=1):
        self.name = enemyIdName
        self.default_health = health
        self.default_speed = speed
    
    def initEntity(self, entity):
        pass
    
    def update(self, entity):
        '''
        moves the entity and applies miscellanious updates.
        '''
        entity.move()
        entity.applyDot()
    