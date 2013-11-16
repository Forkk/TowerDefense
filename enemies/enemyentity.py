'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import enemybase
import pygame

class enemyentity():
    '''
    The class that represents every entity
    properties:
    type (instance of EnemyBase)
    speed
    health
    loc_x
    loc_y
    direction
    alive
    dot_time_left
    dot_damage
    '''

    def __init__(self, type, spritegroup):
        '''
        creates a new eneity of the specifid type.
        '''
        self.speed = type.defSpeed
        self.health = type.defHealth
        self.type = type
        self.sprite = pygame.sprite.Sprite()
        spritegroup.add(self.sprite)
        
    def spawn(self, map, loc_x, loc_y):
        '''
        actually spawns the entity with the given type.
        '''
        self.loc_x = loc_x
        self.loc = loc_y
        self.dot_active = False
        self.dot_time = 0
        self.dot_damage = 0
        self.alive = True
        self.map = map
        self.sprite.setRect
        
    def update(self):
        type.update(self)
    
    def applyDot(self):
        if self.dot_time_left <= 0 :
            return
        
        self.dot_time_left -= 1
        self.damage(self.dot_damage)
        
    def move(self):
        '''
        Moves the entity based on speed, and location
        '''
        self.calcDirection()
        self.sprite.image = self.images[self.direction]
        deltaX = self.speed * enemybase.DIRECTION_MATRIX[self.direction][1];
        deltaY = self.speed * enemybase.DIRECTION_MATRIX[self.direction][1];
        self.loc_x += deltaX
        self.loc_y += deltaY
        self.sprite.rect = self.sprite.rect.move(deltaX, deltaY)
    
    def calcDirection(self):
        # calculate the direction
        pass
        
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
        
