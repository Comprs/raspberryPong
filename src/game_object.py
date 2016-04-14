#!/usr/bin/env python2

from vector import Vector
from consts import WORLD_WIDTH, WORLD_HEIGHT

class GameObject(object):
    def __init__(self, position, size, velocity, colour):
        self.position = position
        self.size = size
        self.velocity = velocity
        self.colour = colour

    def render(self):
        x_origin = int(round(self.position.x))
        y_origin = int(round(self.position.y))
        return {
            (x, y): self.colour
            for x in range(x_origin, x_origin + self.size.x)
            for y in range(y_origin, y_origin + self.size.y)
            if x >= 0 and x < WORLD_WIDTH and y >= 0 and y < WORLD_HEIGHT
        }

    def update(self, time):
        self.position += self.velocity * time
