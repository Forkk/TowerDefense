'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import enemybase

class enemyentity():
    '''
    The class that represents every entity
    properties:
    type (instance of EnemyBase)
    speed
    health
    locX
    locY
    direction
    alive
    dot_time_left
    dot_damage
    '''

    def __init__(self, type):
        '''
        creates a new eneity of the specifid type.
        '''
        self.speed = type.defSpeed
        self.health = type.defHealth
        self.type = type
        
    def spawn(self, direction, locX, locY):
        '''
        actually spawns the entity with the given type.
        '''
        self.locX = locX
        self.loc = locY
        self.direction = direction
        self.dot_active = False
        self.dot_time = 0
        self.dot_damage = 0
        self.alive = True
        
    def draw(self):
        type.draw(self)
        
    def update(self):
        type.update(self)
    
    def applyDot(self):
        if self.dot_time_left <= 0 :
            return
        
        self.dot_time_left -= 1
        self.damage(self.dot_damage)
        
    def move(self):
        '''
        Moves the entity based on speed, direction, and location
        '''
        maskX = enemybase.DIRECTION_MATRIX[self.direction][1];
        maskY = enemybase.DIRECTION_MATRIX[self.direction][1];
        self.locX = self.speed * maskX
        self.locY = self.speed * maskY
        
    def damage(self, ammount):
        '''
        Damages the entity and sets its alive state
        '''
        if not self.alive :
            return
        
        self.health -= ammount
        
        if self.health <= 0 :
            self.health = 0
            self.alive = False
            self.type.onDeath()
        
