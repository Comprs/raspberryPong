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

    Arguments:
        position: the start position of the object
        size the size of the object
        velocity: the initial velocity of the object
        colour: the colour which the renderer will render with
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
        x_origin = int(round(self.position.x))
        y_origin = int(round(self.position.y))
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
        self.position += self.velocity * time
