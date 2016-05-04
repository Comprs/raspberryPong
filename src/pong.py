#!/usr/bin/env python2

from itertools import cycle
import math
import terminal_writer
from number_renderer import convert_number
import consts
import ball
import bat
import RPi.GPIO as GPIO

class Pong:
    def __init__(self):
        self.output = terminal_writer.Writer(consts.SERIAL_OUTPUT, True)

        self.left_bat = bat.Bat(consts.LEFT_BAT_RETURN_ANGLES, consts.CONTROL_1_ADDR)
        self.left_bat.position = consts.LEFT_BAT_INIT_POSITION
        self.left_bat.size = consts.BAT_SIZE
        self.left_bat.colour = consts.LEFT_BAT_COLOUR

        self.right_bat = bat.Bat(consts.RIGHT_BAT_RETURN_ANGLES, consts.CONTROL_2_ADDR)
        self.right_bat.position = consts.RIGHT_BAT_INIT_POSITION
        self.right_bat.size = consts.BAT_SIZE
        self.right_bat.colour = consts.RIGHT_BAT_COLOUR

        self.ball = ball.Ball()
        self.ball.size = consts.BALL_SIZE
        self.ball.colour = consts.BALL_COLOUR
        self.ball.attached_bat = self.left_bat

        self.left_score = 0
        self.right_score = 0

        GPIO.add_event_detect(consts.PLAYER_1_SERVE, GPIO.RISING, lambda x: self.ball.serve(consts.CONTROL_1_ADDR), bouncetime = 200)
        GPIO.add_event_detect(consts.PLAYER_1_ENLARGE, GPIO.RISING, lambda x: self.ball.enlarge(), bouncetime = 200)
        GPIO.add_event_detect(consts.PLAYER_2_SERVE, GPIO.RISING, lambda x: self.ball.serve(consts.CONTROL_2_ADDR), bouncetime = 200)
        GPIO.add_event_detect(consts.PLAYER_2_ENLARGE, GPIO.RISING, lambda x: self.ball.enlarge(), bouncetime = 200)

    def render(self):
        render_dict = {}
        render_dict.update({ (40, y): terminal_writer.COLOUR_WHITE for (y, do_draw) in zip(range(consts.WORLD_HEIGHT), cycle([False, False, True, True])) if do_draw })
        render_dict.update(convert_number(self.left_score, (29, 1)))
        render_dict.update(convert_number(self.right_score, (49, 1)))
        render_dict.update(self.ball.render())
        render_dict.update(self.left_bat.render())
        render_dict.update(self.right_bat.render())
        self.output.write_new_state(render_dict)

    def update(self, time):
        self.ball.update(time, self.left_bat, self.right_bat)
        self.left_bat.update(time, self.ball.position.y)
        self.right_bat.update(time, self.ball.position.y)
        if self.ball.position.x <= 0:
            self.right_score += 1
            self.ball.attached_bat = self.left_bat
        elif self.ball.position.x + self.ball.size.x >= consts.WORLD_WIDTH:
            self.left_score += 1
            self.ball.attached_bat = self.right_bat
        self.ball.serve(None)
