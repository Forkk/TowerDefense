# vim: set expandtab ts=4 sw=4 softtabstop=4:
"""
effects.py - Contains classes and functions for the effects system.
"""

import pygame


class Effect(object):
    """
    Base class for effects.
    An effect is some visual effect such as a bullet line or damage indicator.
    """
    def created(self, game):
        """
        Called when this effect is created and added to the game.
        """
        self.game = game

    def destroyed(self):
        """
        Called when the effect is destroyed.
        """
        pass

    def draw(self, game_size, fx_surface, ui_surface):
        pass
    
    def update(self, delta):
        pass
        

class EffectsManager(object):
    """
    The effects manager handles drawing and updating effects such as bullet lines
    and damage markers.
    """

    def __init__(self, game):
        self.game = game
        
        self.effects = []

    def update(self, delta):
        """
        Updates all of the effects.
        """
        for fx in self.effects:
            fx.update(delta)

    def draw(self, game_surface, fx_surface, ui_surface):
        """
        Draws effects to the given game, effects, and UI surface.
        """
        for fx in self.effects:
            fx.draw(game_surface, fx_surface, ui_surface)

    def addEffect(self, fx):
        if fx not in self.effects:
            self.effects.append(fx)
            fx.created(self.game)

    def removeEffect(self, fx):
        self.effects.remove(fx)
        fx.destroyed()

