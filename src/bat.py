#!/usr/bin/python2

"""
This module implements the bat which is controlled by the player in game
"""

import random
import consts
import game_object
import time

class Bat(game_object.GameObject):
    """The Bat class which represents a bat in game

    Arguments:
        return_angles: A tuple of three angles which the ball should bounce
            back along when it hit a specific third of the bat
        control_address: The numerical address of the ADC to control the
            position of the bat
    """
    def __init__(self, return_angles, control_address = None, *args, **kwargs):
        self.return_angles = return_angles
        self.control_address = control_address
        self.next_shrink = 0.0
        super(Bat, self).__init__(*args, **kwargs)

    def update(self, time_delta, ball_y_pos):
        """Update the state of the bat

        Arguments:
            time_delta: The time passed since the last call to this method
        """
        # If the time has passed the point in which the bat should have shrunk
        # reset the bat's size to the default value
        if time.time() >= self.next_shrink:
            self.size = consts.BAT_SIZE
        if self.control_address == None:
            self.position.y = ball_y_pos - random.choice([0, 0, 0, 1, 2, 2, 2])
        else:
            consts.BUS.write_byte(consts.CONTROL_I2C_ADDR, self.control_address)
            tmp = consts.BUS.read_word_data(consts.CONTROL_I2C_ADDR, 0x00)
            swap_tmp = ((tmp & 0x00FF) << 6) | ((tmp & 0xFF00) >> 10 )
            swap_tmp = max(min(swap_tmp, consts.VMAX), consts.VMIN)
            height_ratio = (swap_tmp - consts.VMIN) / (consts.VMAX - consts.VMIN)
            new_position_y = height_ratio * consts.WORLD_HEIGHT
            if abs(new_position_y - self.position.y) > consts.INPUT_THRESHOLD:
                self.position.y = new_position_y

        super(Bat, self).update(time_delta)

        # Keep the bat within the bounds of the world
        if round(self.position.y) < 0:
            self.position.y = 0

        if round(self.position.y + self.size.y) > consts.WORLD_HEIGHT:
            self.position.y = consts.WORLD_HEIGHT - self.size.y

    def enlarge(self):
        """Enlarge the bat"""
        # Update the point when the bat will decrease it's size back to normal
        self.next_shrink = time.time() + consts.BAT_ENLARGE_TIME
        # Set the size
        self.size = consts.BAT_ENLARGE_SIZE
