#!/usr/bin/python2

"""
This module implements the bat which is controlled by the player in game
"""

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
    def __init__(self, return_angles, control_address, *args, **kwargs):
        self.return_angles = return_angles
        self.control_address = control_address
        self.next_shrink = 0.0
        self.enlarges_left = 2
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
        # Get the data from the bus
        consts.BUS.write_byte(consts.CONTROL_I2C_ADDR, self.control_address)
        bus_value = consts.BUS.read_word_data(consts.CONTROL_I2C_ADDR, 0x00)

        # Byte swap the value
        swapped_value = ((bus_value & 0x000F) << 6) | ((bus_value & 0xFC00) >> 10)

        # Get a value as a ratio of the measured value to the maximum value
        value_ratio = swapped_value / float(consts.ADC_SIGNAL_MAX)

        # Clip the ratio to remove the bottom and top 0.5V
        clipped_ratio = max(min(value_ratio, consts.ADC_RATIO_MAX), consts.ADC_RATIO_MIN)

        # Rescale the ratio so that the value ranges from 0 to 1
        scaled_ratio = (clipped_ratio - consts.ADC_RATIO_MIN) / (consts.ADC_RATIO_MAX - consts.ADC_RATIO_MIN)

        # Calculate the position of the bat
        new_position_y = scaled_ratio * (consts.WORLD_HEIGHT - self.size.y)

        # Set the position if the movement is large enough
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
        if self.enlarges_left > 0:
            self.enlarges_left -= 1
            # Update the point when the bat will decrease it's size back to normal
            self.next_shrink = time.time() + consts.BAT_ENLARGE_TIME
            # Set the size
            self.size = consts.BAT_ENLARGE_SIZE
