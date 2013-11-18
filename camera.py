# vim: set expandtab ts=4 sw=4 softtabstop=4:

"""
camera.py - Handles calculations for camera movement and how the game surfaces should be positioned and scaled.
"""

from vector import Vector, toVector

class Camera(object):
    """
    The camera class handles tracking information about the zooming and scrolling of the map.
    It does all of the math for moving the camera around.
    """
    def __init__(self, game_size, screen_size, min_zoom=0.5, max_zoom=1):
        self.game_size = toVector(game_size)
        self.screen_size = toVector(screen_size)

        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        
        # Half the size of the screen. Used for centering things.
        self.half_screen = self.screen_size / 2
        
        # Screen position.
        # This specifies the coordinates of the center of the "screen"
        # relative to ingame coordinates.
        self.pos = self.game_size / 2

        # Screen zoom.
        # This specifies how much to magnify the screen by.
        self.zoom_val = 1
        
        # Perform an initial update.
        self.updateValues()
        self.setUpdate()


    def move(self, by):
        """
        Moves the camera by the given value.
        """
        self.pos = self.pos + by
        self.setUpdate()

    def zoom(self, by):
        """
        Zooms the camera by the given value.
        """
        self.zoom_val += by
        if self.zoom_val < self.min_zoom: self.zoom_val = self.min_zoom
        if self.zoom_val > self.max_zoom: self.zoom_val = self.max_zoom
        self.setUpdate()

    
    def setPosition(self, pos):
        """
        Sets the camera's position to the given value.
        """
        self.pos = pos
        self.setUpdate()

    def setZoom(self, zoom):
        """
        Sets the camera's zoom level to the given value.
        """
        self.zoom_val = zoom
        self.setUpdate()


    def getPosition(self):
        """
        Gets the camera's position.
        """
        return self.pos
    
    def getZoom(self):
        """
        Gets the camera's zoom level.
        """
        return self.zoom_val


    def getSurfacePos(self):
        """
        Gets the position to draw the game surface (by the top left corner).
        """
        return self.surface_pos

    def getSurfaceSize(self):
        """
        Gets the size that the surface should be resized to.
        """
        return self.surface_size


    def toGameCoordinates(self, coords):
        """
        Translates the given screen coordinates to game coordinates.
        """
        return toVector(coords) - (self.surface_pos * self.zoom_val)


    def setUpdate(self, should_update=True):
        """
        Sets whether or not the camera values should be updated on the next tick.
        """
        self.needs_update = True

    def tickUpdate(self):
        """
        Called by the main loop every tick. Updates the camera's translation values if necessary.
        """
        if self.needs_update: self.updateValues()

    def updateValues(self):
        """
        Updates the camera's calculated surface_size and zoomed_pos values.
        This will be called automatically every game tick if self.needs_update is true.
        """
        # Size of the zoomed game surface.
        self.surface_size = (self.game_size * self.zoom_val).toIntVector()
        #(int(self.game_size[0] * self.zoom_val), int(self.game_size[1] * self.zoom_val))

        # Position of the screen after the zoom.
        self.surface_pos = (Vector(0, 0) - self.pos * (self.zoom_val)).toIntVector()
        #(int(-self.pos[0] * (self.zoom_val/2)), int(-self.pos[1] * (self.zoom_val/2)))

        self.needs_update = False
        
