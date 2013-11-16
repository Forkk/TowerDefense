'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import pygame
import os

class MyClass():
    '''
    A singleton instance of an entityType
    default_health
    default_speed
    textures (dictionary of DIRECTION -> sprite)
    '''
    # constant file path thing
    IMAGE_PATH = "images"

    def __init__(self, enemyIdName):
        self.name = enemyIdName
        '''
        whatever you want.. nobody cares.
        '''
        pass
    
    def getImage(self, direction):
            return pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_" + direction + ".png"))
    
    def draw(self, entity):
        pass
    
    def initEntity(self, entity):
        pass
    
    def update(self, entity):
        '''
        moves the entity and applies miscellanious updates.
        '''
        
        entity.move()
        entity.applyDot()
    