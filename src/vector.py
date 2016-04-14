#!/usr/bin/env python2

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

def rect_intersect(pos_1, size_1, pos_2, size_2):
    return not (pos_1.x + size_1.x < pos_2.x or
                pos_2.x + size_2.x < pos_1.x or
                pos_1.y + size_1.y < pos_2.y or
                pos_2.y + size_2.y < pos_1.y)
             
