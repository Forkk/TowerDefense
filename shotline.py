# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.draw

import math
import copy

from vector import Vector

from effects import Effect

# The starting alpha of shot lines.
DEFAULT_ALPHA = 255

# The default speed at which shot lines fade out.
DEFAULT_FADE_RATE = 255 * 5

# The default extra distance shot lines travel after hitting.
DEFAULT_EXTRA_DIST = 10

DEFAULT_THICKNESS = 2

DEFAULT_COLOR = (255, 255, 0)

# The default distance a shot will travel.
DEFAULT_RANGE = 1000

class ShotLine(Effect):
    """
    Class that represents a bullet line shot by a turret.
    """
    def __init__(self, origin, end, alpha=DEFAULT_ALPHA, fade_rate=DEFAULT_FADE_RATE, thickness=DEFAULT_THICKNESS, color=DEFAULT_COLOR):
        """
        Creates a new shot line from the given origin to the given point.
        Note: fade rate is measured in alpha units per second.
        """
        super(ShotLine, self).__init__()
        self.origin = origin
        self.end = end
        self.alpha = alpha
        self.fade_rate = float(fade_rate) / 1000
        self.thickness = thickness
        self.color = color

    def update(self, delta):
        self.alpha -= self.fade_rate * delta
        if self.alpha <= 0:
            self.game.fx_mgr.removeEffect(self)

    def draw(self, game_surface, fx_surface, ui_surface):
        pygame.draw.line(fx_surface, (self.color[0], self.color[1], self.color[2], int(self.alpha)), self.origin, self.end, self.thickness)


def shotAtAngle(origin, angle, alpha=DEFAULT_ALPHA, fade_rate=DEFAULT_FADE_RATE):
    """
    Returns a shot line representing a shot carrying on endlessly at a given angle.
    """
    shot_end = (origin[0] + math.cos(math.radians(angle))*1000, origin[1] - math.sin(math.radians(angle))*1000)
    return ShotLine(origin, shot_end, alpha, fade_rate)

def toEnemy(origin, angle, enemy_mgr, shot_range=DEFAULT_RANGE, extra_dist=DEFAULT_EXTRA_DIST, **kwargs):
    """
    Creates a shot line traveling from the given origin at the given angle until it hits an enemy.
    This will return a tuple containing the shot line and the enemy.
    You must also pass this function an enemy manager whose enemies should be checked for hits.
    You may specify the maximum bullet travel distance with the shot_range argument.
    Also note the extra_dist argument. This specifies how much further the bullet travels after hitting.
    It's only for visual effect.
    """
    # Trace the line until it hits something.
    # check_dist specifies how far to jump between each check. This will reduce how many times we have to check.
    # By doing this, we significantly reduce the amount of time it takes to trace the shot to wherever it hits.
    # Unfortunately, setting this value too high may cause the system to be inaccurate.
    check_dist = 16
    shot_slope = Vector(math.cos(math.radians(angle)), -math.sin(math.radians(angle))) * check_dist
    check_pos = Vector(origin)
    hit_enemy = None
    for x in range(0, shot_range/check_dist):
        check_pos += shot_slope
        # Check each enemy to see if they've been hit.
        # TODO: Optimize this. We probably don't need to check EVERY single enemy. Maybe just ones nearby?
        for enemy in enemy_mgr.enemies_list:
            if enemy.isTocuhing(check_pos):
                hit_enemy = enemy
                break

        # Break loops when we find a hit.
        if hit_enemy != None:
            break
    
    if hit_enemy == None:
        check_pos = shot_slope * 1000

    check_pos += shot_slope * extra_dist


    return (ShotLine(origin, check_pos, **kwargs), enemy)

def throughEnemies(origin, angle, enemy_mgr, shot_range=DEFAULT_RANGE, **kwargs):
    """
    Creates a shot line traveling from the given origin at the given angle and passing through all enemies.
    This will return a tuple containing the shot line and a list of enemies that were hit.
    You may specify the maximum shot travel distance with the shot_range argument.
    You must also pass this function an enemy manager whose enemies should be checked for hits.
    """
    # Trace the line until it hits something.
    # See the comment about check_dist above.
    check_dist = 16
    shot_slope = Vector(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))*check_dist
    check_pos = Vector(origin)
    hit_enemies = []

    # Clone the enemy list. Every time we hit an enemy, we'll remove it from this and
    # add it to the hit enemies list.
    enemy_list = copy.copy(enemy_mgr.enemies_list)
    
    for x in range(0, shot_range/check_dist):
        check_pos += shot_slope
        # Check each enemy to see if they've been hit.
        # TODO: Optimize this. We probably don't need to check EVERY single enemy. Maybe just ones nearby?
        for enemy in enemy_list:
            if enemy.isTocuhing(check_pos):
                hit_enemies.append(enemy)
                enemy_list.remove(enemy)

    return (ShotLine(origin, check_pos, **kwargs), hit_enemies)

