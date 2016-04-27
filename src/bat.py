#!/usr/bin/python2

import consts
from vector import Vector
import game_object

class Bat(game_object.GameObject):
    def __init__(self, control_address = None, *args, **kwargs):
        self.control_address = control_address
        super(Bat, self).__init__(*args, **kwargs)

    def update(self, time, ball_y_pos):
        if self.control_address == None:
            if ball_y_pos < self.position.y:
                self.velocity = Vector(0, -10)
            elif ball_y_pos > self.position.y + self.size.y:
                self.velocity = Vector(0, 10)
        else:
            pass
            consts.BUS.write_byte(CONTROL_I2C_ADDR, self.control_address)
            tmp = consts.BUS.read_word_data(CONTROL_I2C_ADDR, 0x00)
            swap_tmp = ((tmp & 0x00FF) << 6) | ((tmp & 0xFF00) >> 10 )
            height_ratio = swap_tmp / float(0b1111111111)
            self.position = Vector(self.position.x, height_ratio * WORLD_HEIGHT)
            self.velocity = Vector(0, 0)

        super(Bat, self).update(time)

        if round(self.position.y) < 0:
            self.position.y = 0

        if round(self.position.y + self.size.y) > consts.WORLD_HEIGHT:
            self.position.y = consts.WORLD_HEIGHT - self.size.y
