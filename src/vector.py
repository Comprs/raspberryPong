#!/usr/bin/env python2

import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __div__(self, other):
        return Vector(self.x / other, self.y / other)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def unit_vector(self):
        return self / self.magnitude()

    def angle(self):
        return math.atan2(self.y, self.x)

    @staticmethod
    def create_with_angle(angle):
        return Vector(math.cos(angle), math.sin(angle))

def rect_intersect(pos_1, size_1, pos_2, size_2):
    # Test for intersection by checking that one rect is not above, below, left
    # or right of the other
    return not (pos_1.x + size_1.x < pos_2.x or
                pos_2.x + size_2.x < pos_1.x or
                pos_1.y + size_1.y < pos_2.y or
                pos_2.y + size_2.y < pos_1.y)
             
