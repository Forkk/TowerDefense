# vim: set expandtab ts=4 sw=4 softtabstop=4:

import pygame
import pygame.font

import os

from effects import Effect

# Do this here so we don't do it for every single instance of damage marker.
pygame.font.init()
font = pygame.font.Font(os.path.join("ui", "larabie.ttf"), 13)

class DamageMarker(Effect):
    def __init__(self, damage, pos):
        self.text = str(damage)
        self.pos = pos
        self.alpha = 255
        self.text_render = font.render(self.text, True, (255, 0, 0))

    def update(self, delta):
        self.pos += (0, -0.2) * delta
        self.alpha -= 0.2 * delta
        if self.alpha <= 0:
            self.game.fx_mgr.removeEffect(self)

    def draw(self, game_surface, fx_surface, ui_surface):
        text_copy = self.text_render.copy()
        text_copy.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
        fx_surface.blit(text_copy, self.pos)

