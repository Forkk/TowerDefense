'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import pygame
import os

class MyClass():
    '''
    the base tower class
    every tower should ahve the following properties
    power
    
    methods:
    getRangeForLevel (gets the range for the current level)
    getPowerForLevel (gets the range for the current level)
    '''

    # constant file path thing
    IMAGE_PATH = "images"

    def __init__(self, towerIdName):
        self.name = towerIdName
        '''
        whatever you want.. nobody cares.
        '''
        pass
    
    def getBaseImage(self, level):
        return pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_base_" + level + ".png"))
        
    def getHeadImage(self, level):
        return pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_head_" + level + ".png"))
        
    def getRangeForLevel(self, level):
        return level + 2
    
    def getPowerforLevel(self, level):
        return level * 2
    
    def shoot(self, tower, target):
        target.damage(self.getPowerforLevel(tower.level))
        tower.cooldown = 