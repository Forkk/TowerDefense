# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.time
import pygame.draw

import towerbase

from vector import Vector

import shotline

import math
import random

import utils

class ShootyTower(towerbase.TowerBase):
    """
    Base class for towers that shoot things at enemies.
    Note: If getBaseDamage, getFireRate, or any of the functions
    that return the tower's attributes change at any time other than
    when the tower is upgraded, you must call the updateStats() function.
    """
    
    def __init__(self, game, pos, level=1):
        super(ShootyTower, self).__init__(game, pos, level)

        # The time last time the tower shot.
        self.last_shot = 0

        # The enemy that the tower is currently targeting.
        self.target = None

        # Update the tower's stats.
        self.updateStats()


    def update(self):
        ticks = pygame.time.get_ticks()
        if self.shouldFire() and self.canFire() and self.last_shot + self.shot_delay_time < ticks:
            self.shoot()
            self.last_shot = ticks

        # If we don't have a target, try to find one.
        if self.target == None or not self.target.alive:
            self.findTarget()

    def shoot(self):
        """
        Causes the tower to shoot.
        """
        print("Bang!")
        

    def setTarget(self, enemy):
        """
        Sets this tower's target to the given enemy.
        """
        self.target = enemy

    def findTarget(self):
        """
        Finds and sets a new target for the tower.
        """
        # TODO: Implement a targeting algorithm that actually takes enemy position into account.
        enemies = self.game.enemy_mgr.enemies_list
        if len(enemies) > 0:
            self.setTarget(enemies[0])
        else:
            self.setTarget(None)


    def updateStats(self):
        """
        Recalculates the tower's firing cooldown and other stats based on
        the stat functions.
        """
        # Gets the amount of time (in milliseconds) to delay between shots in shots per second.
        self.shot_delay_time = 60*1000 / self.getFireRate()
    

    def getBaseDamage(self):
        """
        Gets this tower's current direct damage per shot.
        This value indicates how much damage each bullet does.
        This doesn't include splash damage or damage bonuses.
        """
        pass

    def getFireRate(self):
        """
        Gets the tower's firing rate in shots per minute.
        """
        pass

    def getBulletsPerShot(self):
        """
        Gets how many bullets this tower fires in a single shot.
        """
        return 1
    
    def getSpread(self):
        """
        Gets a value representing how much a bullet fired from the 
        tower might deviate from where the tower is aiming.
        """
        pass


    def onFire(self):
        """
        Called every time the tower fires a bullet (or set of bullets).
        This can be used for cooldowns and such.
        """
        pass

    def canFire(self):
        """
        Returns true if this tower is currently allowed to fire.
        The default implementation always returns true, but this can be
        overridden by subclasses to implement things such as cooldown times.
        """
        return True

    def shouldFire(self):
        """
        Returns true if the tower has a target and is aimed to fire.
        If this and canFire() return true, the tower will fire at its target.
        """
        return self.target != None and self.target.alive


class ShootyTurret(ShootyTower):
    """
    A shooty tower with a rotating turret.
    """
    
    def __init__(self, game, pos, level=1):
        super(ShootyTurret, self).__init__(game, pos, level)
        self.aim_angle = 0

        self.shot_lines = []

    def setSprites(self, head, base):
        self.head_sprite = pygame.transform.scale(head, self.game.map.getTileSize())
        self.base_sprite = pygame.transform.scale(base, self.game.map.getTileSize())

    def update(self):
        super(ShootyTurret, self).update()

        if self.target and self.target.alive:
            # Calculate turret rotation.
            center = self.getCenter()
            tile_size = self.game.map.getTileSize()
            target_pos = (self.target.loc_x + tile_size[0]/2, self.target.loc_y + tile_size[1]/2)
            self.aim_angle = math.degrees(math.atan2(target_pos[1] - center[1],
                                                    -target_pos[0] + center[0]))+180

    def draw(self, surface, fx_surface):
        center = self.getCenter()
        pixel_pos = self.getPixelPosition()

        # Get the tower's position in pixel coordinates.
        surface.blit(self.base_sprite, pixel_pos);

        head_size = self.head_sprite.get_size()
        head_pos = (pixel_pos[0] - head_size[0]/2, pixel_pos[1] - head_size[1]/2)
        surface.blit(utils.rot_center(self.head_sprite, self.aim_angle), (head_pos[0] + head_size[0]/2, head_pos[1] + head_size[1]/2));
        
        # Aim lines for debugging.
        #aim_end = (center[0] + math.cos(math.radians(self.aim_angle))*1000, center[1] - math.sin(math.radians(self.aim_angle))*1000)
        #pygame.draw.line(fx_surface, pygame.Color(255, 0, 0, 50), self.getCenter(), aim_end, 2)
    
    def shoot(self):
        # Draw the shot line.
        error_angle = (random.random()-0.5)*self.getSpread()
        shot_angle = self.aim_angle + error_angle

        # The origin should be the end of the barrel.
        # To do this, we get the slope of the barrel's aim line and multiply it by the barrel length.
        aim_slope = Vector(math.cos(math.radians(shot_angle)), -math.sin(math.radians(shot_angle)))
        barrel_len = self.getSize()[0] / 2
        origin = Vector(self.getCenter()) + (aim_slope * barrel_len)

        shot_line, hit_enemy = shotline.toEnemy(origin, shot_angle, self.game.enemy_mgr)

        if hit_enemy != None:
            hit_enemy.damage(self.getBaseDamage())

        self.game.tower_mgr.addShotLine(shot_line)
