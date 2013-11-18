# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.time
import pygame.draw

from towerbase import TowerBase, TowerStats

from vector import Vector, toVector

import shotline

import os
import math
import random

import utils

def shootyTowerStats(damage, rate, spread, bps=1):
    return TowerStats({
        "damage": damage,
        "fire_rate": rate,
        "bullets_per_shot": bps,
        "spread": spread,
        })

class ShootyTower(TowerBase):
    """
    Base class for towers that shoot things at enemies.
    Note: If getBaseDamage, getFireRate, or any of the functions
    that return the tower's attributes change at any time other than
    when the tower is upgraded, you must call the updateStats() function.

    Shooty towers need the following tower stats:
    damage - The base damage per bullet.
    fire_rate - The tower's fire rate in rounds per minute.
    bullets_per_shot - How many bullets are fired per shot.
    spread - The maximum angle of spread for shots.
    """
    
    def __init__(self, game, pos, tower_type):
        super(ShootyTower, self).__init__(game, pos, tower_type)
        
        # Shooty towers need a certain set of stats.
        if not all(key in self.stats for key in ("damage", "fire_rate", "bullets_per_shot", "spread")):
            raise ValueError("Missing some stats for shooty tower.")

        # The time last time the tower shot.
        self.last_shot = 0

        # The enemy that the tower is currently targeting.
        self.target = None

        # Reload info from the tower's stats.
        self.updateStats()

        # Recalculate firing delay when stats change.
        self.stats.addChangeListener(self.statsChanged)


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
        pass

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


    def statsChanged(self, stats, key):
        self.updateStats()

    def updateStats(self):
        """
        Recalculates the tower's firing cooldown and other stats based on
        the stat functions.
        This should be called every time the tower's stats change.
        """
        # Gets the amount of time (in milliseconds) to delay between shots in shots per second.
        self.shot_delay_time = 60*1000 / self.stats["fire_rate"]

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
    
    def __init__(self, game, pos, tower_type):
        super(ShootyTurret, self).__init__(game, pos, tower_type)

        if not all(key in tower_type.sprites for key in ("head", "base")):
            raise ValueError("Shooty turret missing head or body sprite in tower type data.")
        else:
            self.setSprites(tower_type.sprites["head"], tower_type.sprites["base"])

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
        error_angle = (random.random()-0.5)*self.stats["spread"]
        shot_angle = self.aim_angle + error_angle

        # The origin should be the end of the barrel.
        # To do this, we get the slope of the barrel's aim line and multiply it by the barrel length.
        aim_slope = Vector(math.cos(math.radians(shot_angle)), -math.sin(math.radians(shot_angle)))
        barrel_len = self.getSize()[0] / 2
        origin = toVector(self.getCenter()) + (aim_slope * barrel_len)

        shot_line, hit_enemy = shotline.toEnemy(origin, shot_angle, self.game.enemy_mgr)

        if hit_enemy != None:
            hit_enemy.damage(self.stats["damage"], hit_pos = shot_line.end)

        self.game.fx_mgr.addEffect(shot_line)

