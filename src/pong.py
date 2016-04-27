#!/usr/bin/env python2

from itertools import cycle
import terminal_writer
from vector import Vector
from number_renderer import convert_number
import consts
from ball import Ball
from bat import Bat

class Pong:
    def __init__(self):
        self.output = terminal_writer.Writer(consts.SERIAL_OUTPUT, True)
        self.ball = Ball(Vector(40, 20), Vector(1, 1), Vector(8, 8), terminal_writer.COLOUR_YELLOW)
        self.left_bat = Bat(consts.CONTROL_1_ADDR, Vector(3, 18), Vector(1, 3), Vector(0, 0), terminal_writer.COLOUR_GREEN)
        self.right_bat = Bat(consts.CONTROL_2_ADDR, Vector(76, 18), Vector(1, 3), Vector(0, 0), terminal_writer.COLOUR_CYAN)
        self.left_score = 0
        self.right_score = 0

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
            self.ball.position = Vector(40, 20)
        elif self.ball.position.x + self.ball.size.x >= consts.WORLD_WIDTH:
            self.left_score += 1
            self.ball.position = Vector(40, 20)

