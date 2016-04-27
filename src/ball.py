#!/usr/bin/env python2

import RPi.GPIO as GPIO
import consts
import game_object
from vector import Vector, rect_intersect

class Ball(game_object.GameObject):
    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)

    def update(self, time, left_bat, right_bat):
        super(Ball, self).update(time)

        if round(self.position.y) < 0:
            self.position.y = 0
            self.velocity.y = -self.velocity.y

        if round(self.position.y + self.size.y) > consts.WORLD_HEIGHT:
            self.position.y = consts.WORLD_HEIGHT - self.size.y
            self.velocity.y = -self.velocity.y

        self.intersect_bat(left_bat)
        self.intersect_bat(right_bat)

        rounded_pos = int(len(consts.LED_GPIO_CODE) * self.position.x / const.WORLD_WIDTH)
        for port, status in zip(consts.LED_GPIO_CODE, map(lambda x: x == rounded_pos, range(len(const.LED_GPIO_CODE)))):
            GPIO.output(port, status)

    def intersect_bat(self, bat):
        #TODO: Rework this later
        if rect_intersect(self.position, self.size, bat.position, bat.size):
            ball_centre = Vector(self.position.x + self.size.x / 2.0, self.position.y + self.size.y / 2.0)
            bat_centre = Vector(bat.position.x + bat.size.x / 2.0, bat.position.y + bat.size.y / 2.0)
            difference = ball_centre - bat_centre
            if abs(difference.x) < abs(difference.y):
                # Horizontal
                self.velocity.x = -self.velocity.x
                if difference.x < 0:
                    # Colliding on the right
                    self.position.x = bat.position.x - self.size.x
                else:
                    # Colliding on the left
                    self.position.x = bat.position.x + bat.size.x
