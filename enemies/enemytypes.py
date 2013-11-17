'''
Created on Nov 16, 2013

@author: AbrarSyed
'''

import enemybase
import os
import pygame

class EnemyTank(enemybase.EnemyBase):
    def __init__(self):
        super(EnemyTank, self).__init__("tank", health=100, speed=1)
        
class EnemyTruck(enemybase.EnemyBase):
    def __init__(self):
        super(EnemyTruck, self).__init__("truck", health=50, speed=2)

class EnemyUFO(enemybase.EnemyBase):
    def __init__(self):
        super(EnemyUFO, self).__init__("alien", health=500, speed=1, resources=50, load_images=False)
        self.images = (
                       pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_5" + ".png")),
                       )
        
    def getImage(self, direction):
        return self.images[0]

