# vim: set expandtab ts=4 sw=4 softtabstop=4:

import math

from vector import Vector

# The starting alpha of shot lines.
DEFAULT_ALPHA = 255

# The default speed at which shot lines fade out.
DEFAULT_FADE_RATE = 80

# The default extra distance shot lines travel after hitting.
DEFAULT_EXTRA_DIST = 1


def shotAtAngle(origin, angle, alpha=DEFAULT_ALPHA, fade_rate=DEFAULT_FADE_RATE):
    """
    Returns a shot line representing a shot carrying on endlessly at a given angle.
    """
    shot_end = (origin[0] + math.cos(math.radians(angle))*1000, origin[1] - math.sin(math.radians(angle))*1000)
    return ShotLine(origin, shot_end, alpha, fade_rate)

def toEnemy(origin, angle, enemy_mgr, alpha=DEFAULT_ALPHA, fade_rate=DEFAULT_FADE_RATE, extra_dist=DEFAULT_EXTRA_DIST):
    """
    Creates a shot line traveling from the given origin at the given angle until it hits an enemy.
    This will return a tuple containing the shot line and the enemy.
    You must also pass this function an enemy manager whose enemies should be checked for hits.
    Also note the extra_dist argument. This specifies how much further the bullet travels after hitting.
    It's only for visual effect.
    """
    # Trace the line until it hits something.
    shot_slope = Vector(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))
    check_pos = Vector(origin)
    hit_enemy = None
    for x in range(0, 1000):
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


    return (ShotLine(origin, check_pos, alpha, fade_rate), enemy)


class ShotLine(object):
    """
    Class that represents a bullet line shot by a turret.
    """
    def __init__(self, origin, end, alpha=255, fade_rate=80):
        """
        Creates a new shot line from the given origin to the given point.
        """
        self.origin = origin
        self.end = end
        self.alpha = alpha
        self.fade_rate = fade_rate

