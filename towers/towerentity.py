'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import math


class MyClass(object):
    '''
    properties:
    type
    current_target
    loc_x
    loc_y
    level
    
    methods:
    shoot (attacks the target)
    refreshTarget (recalculates the target)
    '''

    def __init__(self, type, loc_x, loc_y, level=0):
        '''
        constructor
        '''
        self.type = type
        self.cooldown = 0
        self.current_target = None
        self.type = type
        self.level = 0
        self.loc_X = loc_x
        self.loc_y = loc_y
        
    def refreshTarget(self):
        if self.current_target = None or not self.isInRange(current_target) :
            # recalc target
            # TODO
            pass
        pass
    
    def distanceSquared(self, targetX, targetY):
        return math.pow(self.loc_x - targetX, 2) + math.pow(self.loc_y - targetY, 2)  
    
    def isInRange(self, target):
        return math.pow(self.type.getRangeForLevel(self.level), 2) >= self.distanceSquared(target.loc_x, target.loc_y)
    
    def shoot(self):
        if self.current_target != None
            type.shoot(self, self.current_Target)