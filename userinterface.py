# vim: set expandtab ts=4 sw=4 softtabstop=4:

"""
userinterface.py - Handles the game's user interface (UI) and draws it to the
screen.
"""

import os

import maptile

"""
The size of the font to use in the user interface
"""
FONT_SIZE = 25

"""
The number of pixels of padding to use between the font
and the screen.
"""
FONT_PADDING = 10

"""
The color of the font (this is an RGB value)
"""
FONT_COLOR = (0, 0, 0)

"""
The color used for the background behind the font.
"""
FONT_BACKGROUND = (255, 255, 255)

"""
The number of pixels between two lines of text on the screen.
"""
FONT_LINESPACE = 4

import pygame
import pygame.transform
import pygame.image

import os

class UserInterface:

    def __init__(self, game):
        self.game = game

        # Define a font object to use
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("ui", "larabie.ttf"), FONT_SIZE, )
        self.gamestate = True # The game is running

        # When placing a tower, this will be set to the coordinates the user wanted
        # to place it at.
        self.towerPlacePos = None

        self.placement_square = pygame.transform.scale(pygame.image.load(os.path.join("ui", "blue.png")), self.game.map.getTileSize())

    def update(self, gamedata):
        # We save a ui_surface containing the text we want to show.
        self.score = self.font.render("Score: " + str(gamedata.score),
                                      True, FONT_COLOR, FONT_BACKGROUND)
        self.lives = self.font.render("Lives: " + str(gamedata.lives),
                                      True, FONT_COLOR, FONT_BACKGROUND)
        self.resources = self.font.render("Resources: " + str(gamedata.resources),
                                          True, FONT_COLOR, FONT_BACKGROUND)
        self.defeat = self.font.render("You have been defeated!", True,
                                       FONT_COLOR, FONT_BACKGROUND)

    def draw(self, ui_surface, game_surface, fx_surface):
        # Draw the score in the upper left corner
        ui_surface.blit(self.score, (FONT_PADDING, FONT_PADDING))
        # Put the number of lives below the score
        ui_surface.blit(self.lives, (FONT_PADDING, FONT_SIZE+FONT_PADDING+FONT_LINESPACE))
        # Put the resources in the top right corner
        ui_surface.blit(self.resources, (ui_surface.get_width()-FONT_PADDING-self.resources.get_width(),
                                      FONT_PADDING))

        # If the game has ended, show a defeat message
        if not self.gamestate:
            ui_surface.blit(self.defeat, ((ui_surface.get_width()-self.defeat.get_width())/2,
                                       (ui_surface.get_height()-self.defeat.get_height())/2))
        
        # If we're placing a tower, draw the tower menu.
        if self.towerPlacePos != None:
            # TODO: We don't need to update all of this every frame. Only when the selection changes.
            
            # Draw the selected tile on the fx layer.
            fx_surface.blit(self.placement_square, self.game.map.getPixelCoordinates(self.towerPlacePos))

            tower_menu_text = ""

            selected_tower = self.game.tower_mgr.getTowerAt(self.towerPlacePos)
            if selected_tower:
                tower_menu_text = "TODO: Implement tower menu."
            elif self.game.map.tiles[self.towerPlacePos[0]][self.towerPlacePos[1]].type == maptile.PLOT:
                # If there's no tower at the selected position.
                types = self.game.tower_mgr.getTowerTypes()
                line_count = len(types)+2

                tower_menu_text = "Select a tower by pressing its number:"
                for i, ttype in enumerate(types):
                    i += 1
                    if i == 10: i = 0 # Hack to show the user to push the 0 key instead of the 10 key.
                    tower_menu_text += "\n<%d> %s - %s resources" % (i, ttype.name, ttype.cost)
            else:
                tower_menu_text = "You can only place towers on empty plots."

            tower_menu_text += "\n<Escape> Cancel"

            lines = tower_menu_text.splitlines()
            line_size = self.font.get_linesize()
            line_pos = ui_surface.get_height() - (line_size * len(lines)) - FONT_PADDING
            for i, line in enumerate(lines):
                self.drawText(ui_surface, line, (FONT_PADDING, line_pos))
                line_pos += line_size
            
    def drawText(self, surface, text, pos):
        text_surface = self.font.render(text, True, FONT_COLOR, FONT_BACKGROUND)
        surface.blit(text_surface, pos)

    def showDefeat(self):
        self.gamestate = False

