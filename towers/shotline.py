# vim: set expandtab ts=4 sw=4 softtabstop=4:

import math

class ShotLine(object):
    """
    Class that represents a bullet line shot by a turret.
    """
    def __init__(self, origin, angle, alpha=255, fade_rate=80):
        """
        Creates a new shot line from the given origin traveling at the given angle.
        """
        self.origin = origin
        self.end = (origin[0] + math.cos(math.radians(angle))*1000, origin[1] - math.sin(math.radians(angle))*1000)
        self.alpha = alpha
        self.fade_rate = fade_rate

