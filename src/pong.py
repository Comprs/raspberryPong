#!/usr/bin/env python2

from itertools import cycle
import terminal_writer
import game_object
from vector import Vector, rect_intersect
from clock import Clock
from number_renderer import convert_number
from consts import WORLD_WIDTH, WORLD_HEIGHT
from serial import Serial

class Ball(game_object.GameObject):
    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)

    def update(self, time, left_bat, right_bat):
        super(Ball, self).update(time)

        if round(self.position.y) < 0:
            self.position.y = 0
            self.velocity.y = -self.velocity.y

        if round(self.position.y + self.size.y) > WORLD_HEIGHT:
            self.position.y = WORLD_HEIGHT - self.size.y
            self.velocity.y = -self.velocity.y

        self.intersect_bat(left_bat)
        self.intersect_bat(right_bat)

    def intersect_bat(self, bat):
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
            #else:
            #    self.velocity.y = -self.velocity.y
            #    # Vertical 
            #    if difference.y < 0:
            #        self.position.y = bat.position.y - self.size.y
            #    else:
            #        # Colliding on the top
            #        self.position.y = bat.position.y + bat.size.y

class Bat(game_object.GameObject):
    def __init__(self, *args, **kwargs):
        super(Bat, self).__init__(*args, **kwargs)

    def update(self, time, ball_y_pos):
        #if ball_y_pos < self.position.y:
        #    self.velocity = Vector(0, -10)
        #elif ball_y_pos > self.position.y + self.size.y:
        #    self.velocity = Vector(0, 10)

        super(Bat, self).update(time)

        if round(self.position.y) < 0:
            self.position.y = 0

        if round(self.position.y + self.size.y) > WORLD_HEIGHT:
            self.position.y = WORLD_HEIGHT - self.size.y

class Pong:
    def __init__(self):
        serial_output = Serial("/dev/ttyAMA0", 38400)
        self.output = terminal_writer.Writer(serial_output, True)
        self.ball = Ball(Vector(40, 20), Vector(1, 1), Vector(8, 8), terminal_writer.COLOUR_YELLOW)
        self.left_bat = Bat(Vector(3, 18), Vector(1, 3), Vector(0, 0), terminal_writer.COLOUR_GREEN)
        self.right_bat = Bat(Vector(76, 18), Vector(1, 3), Vector(0, 0), terminal_writer.COLOUR_CYAN)
        self.left_score = 0
        self.right_score = 0

    def render(self):
        render_dict = {}
        render_dict.update({ (40, y): terminal_writer.COLOUR_WHITE for (y, do_draw) in zip(range(WORLD_HEIGHT), cycle([False, False, True, True])) if do_draw })
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
        elif self.ball.position.x + self.ball.size.x >= WORLD_WIDTH:
            self.left_score += 1
            self.ball.position = Vector(40, 20)

if __name__ == "__main__":
    pong = Pong()
    clock = Clock(60.0)
    while True:
        pong.update(clock.get_time_delta())
        pong.render()
        clock.tick()
