#!/usr/bin/env python2

"""
This module implements the ball which is presented to the players
"""

import consts
import random

if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
    import RPi.GPIO as GPIO

import game_object
from vector import Vector, rect_intersect

class Ball(game_object.GameObject):
    """The Ball class which represents a ball"""

    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)
        self.attached_bat = None

    def update(self, time, left_bat, right_bat):
        """Perform the update based on the time difference given. It also takes
        the two bats which will also be in the world in order to check if it
        has collided and should then bounce
        """

        # Perform the movement
        super(Ball, self).update(time)

        # Keep within the world bounds
        if round(self.position.y) < 0:
            self.position.y = 0
            self.velocity.y = -self.velocity.y
            consts.MIXER_QUEUE.put(consts.BALL_BOUNCE_SFX)

        if round(self.position.y + self.size.y) > consts.WORLD_HEIGHT:
            self.position.y = consts.WORLD_HEIGHT - self.size.y
            self.velocity.y = -self.velocity.y
            consts.MIXER_QUEUE.put(consts.BALL_BOUNCE_SFX)

        # Check for collisions with the bats
        self.intersect_bat(left_bat)
        self.intersect_bat(right_bat)

        # Set the LED display which shows the horizontal position
        if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
            # Get the "index" of the LED to illuminate
            rounded_pos = int(len(consts.LED_GPIO_CODE) * self.position.x / consts.WORLD_WIDTH)
            # Zip the LED GPIO codes with whether they should be illuminated,
            # then write out the boolean value to the correct port
            for port, status in zip(consts.LED_GPIO_CODE, map(lambda x: x == rounded_pos, range(len(consts.LED_GPIO_CODE)))):
                GPIO.output(port, status)

    def intersect_bat(self, bat):
        """Preform the collision detection and reaction"""

        # Check that the ball has collided with the bat based on the two
        # bounding boxes
        if rect_intersect(self.position, self.size, bat.position, bat.size):
            # Queue up the sound effect for playing
            consts.MIXER_QUEUE.put(consts.BALL_BOUNCE_SFX)

            # Get the angle to reflect with base upon the position the ball
            # collided with
            if self.position.y + self.size.y * 0.5 < bat.position.y + bat.size.y * (1.0 / 3.0):
                return_angle = bat.return_angles[0]
            elif self.position.y + self.size.y * 0.5 > bat.position.y + bat.size.y * (2.0 / 3.0):
                return_angle = bat.return_angles[2]
            else:
                return_angle = bat.return_angles[1]

            # Update the velocity to the new value based on the return angle
            # and a random value for the new speed
            self.velocity = Vector.create_with_angle(return_angle) * (80.0 / random.choice([2, 2, 2, 5, 5, 5, 15]))

            # Correct the position based upon the new velocity
            if self.velocity.x > 0:
                self.position.x = bat.position.x + bat.size.x
            elif self.velocity.x < 0:
                self.position.x = bat.position.x - self.size.x

    def serve(self, bat_num):
        if bat_num == self.attached_bat:
            #Something
