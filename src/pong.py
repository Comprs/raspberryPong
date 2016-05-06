#!/usr/bin/env python2

"""
This module defines the Pong game object
"""

from itertools import cycle, repeat, chain
import math
import terminal_writer
from number_renderer import convert_number
import consts
import ball
import bat
import RPi.GPIO as GPIO
import glow_seq
import sys

class Pong:
    """The Pong object which houses the state of the game"""
    def __init__(self):
        """Initialise the game state"""
        # Initialise the terminal writer with the serial output
        self.output = terminal_writer.Writer(consts.SERIAL_OUTPUT, True)

        # Initialise the two bats
        self.left_bat = bat.Bat(consts.LEFT_BAT_RETURN_ANGLES, consts.CONTROL_1_ADDR)
        self.left_bat.position = consts.LEFT_BAT_INIT_POSITION
        self.left_bat.size = consts.BAT_SIZE
        self.left_bat.colour = consts.LEFT_BAT_COLOUR

        self.right_bat = bat.Bat(consts.RIGHT_BAT_RETURN_ANGLES, consts.CONTROL_2_ADDR)
        self.right_bat.position = consts.RIGHT_BAT_INIT_POSITION
        self.right_bat.size = consts.BAT_SIZE
        self.right_bat.colour = consts.RIGHT_BAT_COLOUR

        self.serving_pattern = cycle(chain(repeat(self.left_bat, 5), repeat(self.right_bat, 5)))

        # Initialise the ball and attach it to the left bat ready for serving
        self.ball = ball.Ball()
        self.ball.size = consts.BALL_SIZE
        self.ball.colour = consts.BALL_COLOUR
        self.ball.attached_bat = next(self.serving_pattern)

        # Initialise the score
        self.left_score = 0
        self.right_score = 0

        # Setup the callbacks for the controller buttons
        # The callbacks themselves are functions which take one argument. This
        # is because the API which is being utilised here provides the GPIO pin
        # number as an argument. This is discarded as it is unneeded
        # The controller address is provided to the serve functions so that the
        # ball knows if the correct controller is trying to serve it
        GPIO.add_event_detect(consts.PLAYER_1_SERVE, GPIO.RISING, lambda x: self.ball.serve(consts.CONTROL_1_ADDR), bouncetime = 200)
        GPIO.add_event_detect(consts.PLAYER_1_ENLARGE, GPIO.RISING, lambda x: self.left_bat.enlarge(), bouncetime = 200)
        GPIO.add_event_detect(consts.PLAYER_2_SERVE, GPIO.RISING, lambda x: self.ball.serve(consts.CONTROL_2_ADDR), bouncetime = 200)
        GPIO.add_event_detect(consts.PLAYER_2_ENLARGE, GPIO.RISING, lambda x: self.right_bat.enlarge(), bouncetime = 200)

        # Create the glow sequencer
        self.glow_seq = glow_seq.GlowSequencer()
        self.glow_seq.insert(consts.NORMAL_PATTERN, float("inf"))

    def render(self):
        """Render the output to the display"""
        # Start with nothing drawn, which is no coordinate colour association
        render_dict = {}

        # Draw the net down the centre of the screen
        # This is done by taking the basic pattern of off, off, on and on
        # and looping it infinitely. Next this sequence is paired with a
        # range of numbers between 0 and the world height. Next the
        # coordinates (40, y), where y is a number in the previous sequence,
        # is associated with the colour white if the value yielded from the
        # initial pattern is true.
        render_dict.update({ (40, y): terminal_writer.COLOUR_WHITE for (y, do_draw) in zip(range(consts.WORLD_HEIGHT), cycle([False, False, True, True])) if do_draw })

        # Render the two scores
        render_dict.update(convert_number(self.left_score, (29, 1)))
        render_dict.update(convert_number(self.right_score, (49, 1)))

        # Render the ball
        render_dict.update(self.ball.render())

        # Render the two bats
        render_dict.update(self.left_bat.render())
        render_dict.update(self.right_bat.render())

        # Provide this to the writer to create a difference since the last
        # render and eventually only write out what has changed
        self.output.write_new_state(render_dict)

    def update(self, time):
        """Update the game state

        Arguments:
            time: The time since the last update
        """
        # Update the game objects
        self.left_bat.update(time, self.ball.position.y)
        self.right_bat.update(time, self.ball.position.y)
        self.ball.update(time, self.left_bat, self.right_bat)

        # Check that the ball has left the world on either size and increment
        # the score accordingly
        if self.ball.position.x <= 0:
            self.right_score += 1
            self.ball.attached_bat = next(self.serving_pattern)
            self.glow_seq.insert(consts.SCORE_PATTERN, consts.SCORE_PATTERN_LENGTH)
        elif self.ball.position.x + self.ball.size.x >= consts.WORLD_WIDTH:
            self.left_score += 1
            self.ball.attached_bat = next(self.serving_pattern)
            self.glow_seq.insert(consts.SCORE_PATTERN, consts.SCORE_PATTERN_LENGTH)
        if self.left_score >= 10 or self.right_score >= 10:
            self.render()
            sys.exit()

    def update_glow(self, time):
        """Update the PiGlow

        Arguments:
            time: The time since the last update
        """
        self.glow_seq.sample(time)
