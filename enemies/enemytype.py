'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import pygame
import os

class enemytype():
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
        self.images = (
                        pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_1" + ".png")),
                        pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_2" + ".png")),
                        pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_3" + ".png")),
                        pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_4" + ".png")),
                        pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_5" + ".png")),
                       )
    
    def initEntity(self, entity):
        pass
    
    def update(self, entity):
        '''
        moves the entity and applies miscellanious updates.
        '''
        entity.move()
        entity.applyDot()
    