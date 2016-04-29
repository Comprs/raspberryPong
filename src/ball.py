#!/usr/bin/env python2

import consts

if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
    import RPi.GPIO as GPIO

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

        if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
            rounded_pos = int(len(consts.LED_GPIO_CODE) * self.position.x / consts.WORLD_WIDTH)
            for port, status in zip(consts.LED_GPIO_CODE, map(lambda x: x == rounded_pos, range(len(consts.LED_GPIO_CODE)))):
                GPIO.output(port, status)

    def intersect_bat(self, bat):
        if rect_intersect(self.position, self.size, bat.position, bat.size):
            self.velocity.x = -self.velocity.x
            if self.velocity.x > 0:
                self.position.x = bat.position.x + bat.size.x
            elif self.velocity.x < 0:
                self.position.x = bat.position.x - self.size.x
