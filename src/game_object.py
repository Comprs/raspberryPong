#!/usr/bin/env python2

"""This module contains the base class which is derived by the game objects
which are used in the game
"""

import vector
import consts
import terminal_writer

class GameObject(object):
    """This object is derived by other game objects in order to reuse the 
    vector update code and the render code
    """
    def __init__(self):
        self.position = vector.Vector(0, 0)
        self.size = vector.Vector(0, 0)
        self.velocity = vector.Vector(0, 0)
        self.colour = terminal_writer.COLOUR_WHITE

    def render(self):
        """Draw out the game object based on the size and position of the
        object
        """
        # Get the integral origin point
        x_origin = int(round(self.position.x))
        y_origin = int(round(self.position.y))
        # Return a dictionary with all of the x, y coordinates that are covered
        # by this object, associated with the colour of this object. This also
        # makes sure no points outside of the world are included to stop the
        # display from displaying errors.
        return {
            (x, y): self.colour
            for x in range(x_origin, x_origin + self.size.x)
            for y in range(y_origin, y_origin + self.size.y)
            if x >= 0 and x < consts.WORLD_WIDTH and y >= 0 and y < consts.WORLD_HEIGHT
        }

    def update(self, time):
        """Update the position

        Arguments:
            time: the time since the last call
        """
        # Using basic mechanical methods, calculate the new position
        self.position += self.velocity * time
