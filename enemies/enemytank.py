'''
Created on Nov 16, 2013

@author: AbrarSyed
'''
import enemybase
import os
import pygame

class EnemyTank(enemybase.EnemyBase):
    '''
    tank
    '''

    def __init__(self):
        super(EnemyTank, self).__init__("tank")
        self.images = (
                       pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_1" + ".png")),
                       pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_2" + ".png")),
                       pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_3" + ".png")),
                       pygame.image.load(os.path.join(self.IMAGE_PATH, self.name + "_4" + ".png"))
                       )
