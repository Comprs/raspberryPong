#!/usr/bin/python2

import random
import consts
from vector import Vector
import game_object
import time

class Bat(game_object.GameObject):
    def __init__(self, return_angles, control_address = None, *args, **kwargs):
        self.return_angles = return_angles
        self.control_address = control_address
        self.next_shrink = 0.0
        super(Bat, self).__init__(*args, **kwargs)

    def update(self, timedelta, ball_y_pos):
        if time.time() >= self.next_shrink:
            self.size.y = 3
        if self.control_address == None:
            self.position.y = ball_y_pos - random.choice([0, 0, 0, 1, 2, 2, 2])
        else:
            consts.BUS.write_byte(consts.CONTROL_I2C_ADDR, self.control_address)
            tmp = consts.BUS.read_word_data(consts.CONTROL_I2C_ADDR, 0x00)
            swap_tmp = ((tmp & 0x00FF) << 6) | ((tmp & 0xFF00) >> 10 )
            try:
                VOLTS # Define this to active scaling
                VMIN, VMAX = 0.5, 2.5
                swap_tmp = max(min(swap_tmp, VMAX*VOLTS), VMIN*VOLTS)
                height_ratio = (swap_tmp - VMIN*VOLTS)/((VMAX-VMIN)*VOLTS) # Probably doesn't work correctly
            except:
                height_ratio = swap_tmp / float(0b1111111111)
            new_position_y = height_ratio * const.WORLD_HEIGHT
            self.position = Vector(self.position.x, new_position_y if abs(new_position_y - self.position.y) > consts.INPUT_THRESHOLD else self.position.y)
            self.velocity = Vector(0, 0)

        super(Bat, self).update(timedelta)

        if round(self.position.y) < 0:
            self.position.y = 0

        if round(self.position.y + self.size.y) > consts.WORLD_HEIGHT:
            self.position.y = consts.WORLD_HEIGHT - self.size.y

    def enlarge(self):
        self.next_shrink = time.time() + 15.0
        self.size.y = 5
