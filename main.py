"""
main.py - The entry point into the game. This runs the main game loop.
"""

import pygame
import pygame.key
import sys
import gamemap
import os
import gamedata
import userinterface
import enemymanager

"""
The dimensions for the screen. These should remain constant.
"""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

"""
The max number of frames per second for the game.
"""
MAX_FPS = 60

"""
The game clock
"""
GameClock = None

"""
The title of the game. This should remain constant.
"""
TITLE = "Defensive Design"


# Keys for scrolling the screen.
# Dict for mapping keypresses to the direction they should move the screen.
# We should add some more extensible system for this later, but this will do for now.
KEYPRESS_SCROLL_MAP = {
        # Arrow keys.
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),

        # WASD
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0),
        }

# Screen scrolling speed in pixels per tick.
SCROLL_SPEED = 5

"""
This performs initial setup of the game. Any global variables
should also be defined here (yes, I know most people say global
variables are bad, but there really isn't a simple solution).
"""
def setup():
   
    # Set the title of the game.
    pygame.display.set_caption(TITLE)
    # Set up a new window.
    global ScreenSurface
    ScreenSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	# We'll have 3 surfaces, the UI surface, the game surface, and the screen surface.
    # The game surface will be for drawing the ingame stuff to. It'll be translated based on screen view position.
    # Will be initialized later based on the size of the gamemap.
    global GameSurface

    global UISurface
    UISurface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA);


    # Set up the map
    global Map

    # Set up the starting game data
    global Data
    Data = gamedata.GameData()
    
    # Set up the UI
    global UI
    UI = userinterface.UserInterface()
    Map = gamemap.GameMap("map1")

    # Now, create the game surface based on the map size.
    GameSurface = pygame.Surface(Map.getMapSize());

    # Initialize the enemy manager
    global EnemyManager
    EnemyManager = enemymanager.EnemyManager(Map.getTileSize())

    global GameClock
    GameClock = pygame.time.Clock()

    global GameState
    GameState = True

    # Screen position.
    # This specifies the coordinates of the top left corner of the "screen"
    # relative to ingame coordinates.
    global ViewPosition
    ViewPosition = (0, 0)

"""
This handles a single pygame event.
"""
def handleEvent(event):
    if(event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
        handleKeyEvent(event)
    if event.type == pygame.QUIT:
        # Quit the program safely
        pygame.quit()
        sys.exit()
    else:
        EnemyManager.spawnEnemy(event, Map.getStartingTile())

"""
This is the main game loop, called as many times as
the computer allows.
"""
def main():
    while(1):
        #Handle the event queue
        event = pygame.event.poll()
        # The event queue returns an event of type NOEVENT if the queue is empty
        while(event.type != pygame.NOEVENT):
            handleEvent(event)
            event = pygame.event.poll()
        # Delete anything already on the surface.
        ScreenSurface.fill((0, 0, 0))

        # If a scroll key is pressed, move the screen.
        
        update() # Update the game objects
        draw() # Draw all the game objects
        pygame.display.flip()

        # Maintain the max frame rate
        GameClock.tick(MAX_FPS)
       

"""
Handles any updating of game objects. This is called
once per game loop.
"""
def update():
    global GameState
    if(GameState):
        # Update the scren scrolling.
        for key, direction in KEYPRESS_SCROLL_MAP.iteritems():
            if pygame.key.get_pressed()[key]:
                global ViewPosition
                ViewPosition = (ViewPosition[0] + (direction[0] * SCROLL_SPEED), ViewPosition[1] + (direction[1] * SCROLL_SPEED))
        
        # Update the enemies
        livesLost = EnemyManager.update(Map)
        Data.lives -= livesLost
        
        # Update the UI
        UI.update(Data)

        # Check if the game is over
        if(Data.lives <= 0):
            GameState = False # The game is over
            UI.showDefeat()
       

"""
Draws all game objects to the screen. This is called once
per game loop.
"""
def draw():
    # Draw the map
    Map.draw(GameSurface)

    # Draw the enemies
    EnemyManager.draw(GameSurface)

    # Clear the UI surface to transparent and then draw the UI
    UISurface.fill(pygame.Color(0, 0, 0, 0))
    UI.draw(UISurface)

    # Now, we draw the game and UI surfaces onto the screen.
    # TODO: Screen scrolling by drawing the game surface in a different position.
    ScreenSurface.blit(GameSurface, (-ViewPosition[0], -ViewPosition[1]))

    ScreenSurface.blit(UISurface, (0, 0))
    

"""
Handles a single keyboard event (both key down and key up).
The event passed in is assumed to be a key event, or else
nothing happens.
"""
def handleKeyEvent(event):
    if(event.type == pygame.KEYDOWN):
        # If the escape key has been pressed, quit the game safely
        if(event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    else:
        if(event.type == pygame.KEYUP):
            return # TODO: Add stuff for key up events here

pygame.init()
setup()
main()
