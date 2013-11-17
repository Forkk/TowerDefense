'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import enemybase
import os
import pygame

class EnemyTank(enemybase.EnemyBase):
    def __init__(self):
        super(EnemyTank, self).__init__("tank", 100, .1)
        
class EnemyTruck(enemybase.EnemyBase):
    def __init__(self):
        super(EnemyTruck, self).__init__("truck", 100, .15)

class EnemyUFO(enemybase.EnemyBase):
    def __init__(self):
        self.name = "alien"
        self.default_health = 500
        self.default_speed = .099999
        self.images = (
                       pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_5" + ".png")),
                       )
        
    def getImage(self, direction):
        return self.images[0]