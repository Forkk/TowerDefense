# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.time

import towerbase

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
        if self.target == None:
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
        return self.target != None


class ShootyTurret(ShootyTower):
    """
    A shooty tower with a rotating turret.
    """
    
    def __init__(self, game, pos, level=1):
        super(ShootyTurret, self).__init__(game, pos, level)

    def setSprites(self, head, base):
        self.head_sprite = pygame.transform.scale(head, self.game.map.getTileSize())
        self.base_sprite = pygame.transform.scale(base, self.game.map.getTileSize())

    def draw(self, surface):
        pixel_pos = self.getPixelPosition()

        # Get the tower's position in pixel coordinates.
        surface.blit(self.base_sprite, pixel_pos);

        # TODO: Rotate the head towards the target.
        surface.blit(self.head_sprite, pixel_pos);

