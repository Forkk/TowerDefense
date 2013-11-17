'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import enemybase
import pygame
import maptile
import math

class EnemyEntity(object):
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

    def __init__(self, enemy_type):
        '''
        creates a new eneity of the specifid enemy_type.
        '''
        self.speed = enemy_type.default_speed
        self.health = enemy_type.default_health
        self.enemy_type = enemy_type
        
    def spawn(self, game_map, spritegroup):
        '''
        actually spawns the entity with the given type.
        '''
        start = game_map.getStartingTile()
        self.loc_x = start[0]
        self.loc_y = start[1]
        self.path_index = 0
        self.dot_time_left = 0
        self.dot_damage = 0
        self.alive = True
        self.game_map = game_map
        self.needs_dir_update = True
        self.direction = 2
        
        # sprite stuff
        self.sprite = pygame.sprite.Sprite()
        size = game_map.getTileSize()
        self.sprite.rect = pygame.Rect(self.loc_x, self.loc_y, size[0], size[1])
        self.sprite.image = self.enemy_type.images[2]
        spritegroup.add(self.sprite)
        
    def update(self, elapsed):
        self.enemy_type.update(self, elapsed)
    
    def applyDot(self, elapsed):
        if self.dot_time_left <= 0 :
            return
        
        self.dot_time_left -= elapsed
        self.damage(self.dot_damage * elapsed)
        
    def move(self, elapsed):
        '''
        Moves the entity based on speed, and location
        '''
        for x in range(0, elapsed/10) :
            if self.needs_dir_update :
                self.calcDirection()
            self.sprite.image = self.enemy_type.images[self.direction-1]
            self.sprite.image = pygame.transform.scale(self.sprite.image, self.game_map.getTileSize())
            deltaX = self.speed * 10 * enemybase.DIRECTION_MATRIX[self.direction][0];
            deltaY = self.speed * 10 * enemybase.DIRECTION_MATRIX[self.direction][1];
            self.loc_x += deltaX
            self.loc_y += deltaY
            self.sprite.rect = self.sprite.rect.move(deltaX, deltaY)
            self.updatePathLoc()
    
    def calcDirection(self):
        # calculate the direction
        current = self.getPathLoc()
        nextLoc = self.getNextLoc()
        delta = (nextLoc[0] - current[0], nextLoc[1] - current[1])
        for direct, val in enemybase.DIRECTION_MATRIX.iteritems() :
            if val == delta :
                self.needs_dir_update = False
                self.direction = direct
            
    def updatePathLoc(self):
        current = self.getPathLoc()
        nextLoc = self.getNextLoc()
        
        if self.game_map.getTileCoordinates((self.loc_x, self.loc_y)) == current :
            # its in the same place it was.. thats fine.
            return
        
        # now we can safely assume, I hope.. that the entity is currently in the NEXT location
        
        # temp stuff...
        adder = enemybase.DIRECTION_MATRIX[self.direction]
        if self.direction == 4 or self.direction == 1:
            adder = (adder[0] * .1, adder[1] * .1)
        map_size = self.game_map.getTileSize()
        adder = (map_size[0] * adder[0], map_size[1] * adder[1])
        adder = (self.loc_x + adder[0], self.loc_y + adder[1])
        temp = self.game_map.getTileCoordinates(adder)
            
        if temp != nextLoc:
            self.path_index += 1
            self.needs_dir_update = True
            #print self.path_index
            #print self.game_map.path[self.path_index]
        
    
    def getPathLoc(self):
        return self.game_map.path[self.path_index]
    
    def getNextLoc(self):
        return self.game_map.path[self.path_index + 1]
    
    def getLoc(self):
        return (self.loc_x, self.loc_y)
        
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
            self.enemy_type.onDeath()
        
    
    def dead(self):
        if(self.health <= 0):
            return True
        else:
            return False
    
    """
    Determines if the enemy is offscreen or not. This only
    returns true if all parts of the enemy are offscreen.
    """
    def offscreen(self, mapdata):
        tilesize = mapdata.getTileSize()
        mapsize = mapdata.getMapSize()
        coordinates = self.getCoordinates()
        if(coordinates[0] < -tilesize[0] or coordinates[0] > mapsize[0]):
            return True
        elif(coordinates[1] < -tilesize[1] or coordinates[1] > mapsize[1]):
            return True
        else:
            return False

    def getCoordinates(self):
        return (self.sprite.rect.left, self.sprite.rect.top)

    """
    Returns true if the enemy is at the destination.
    """
    def atDestination(self, mapdata):
        coordinates = self.getCoordinates()
        mapsize = mapdata.getMapSize()
        # Make sure the coordinates are valid
        if(coordinates[0] < 0 or coordinates[0] >= mapsize[0] or coordinates[1] < 0
           or coordinates[1] >= mapsize[1]):
            return False        
        tile_number = mapdata.getTileCoordinates(coordinates)
        if(mapdata.tiles[tile_number[0]][tile_number[1]].type == maptile.DESTINATION):
            return True
        else:
            return False

# A little trick so we can run the game from here in IDLE
if __name__ == '__main__':
    execfile("main.py")
