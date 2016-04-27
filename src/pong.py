#!/usr/bin/env python2

from itertools import cycle
import terminal_writer
import game_object
from vector import Vector, rect_intersect
from scheduler import Scheduler
from number_renderer import convert_number
from consts import WORLD_WIDTH, WORLD_HEIGHT, LED_GPIO_CODE, CONTROL_I2C_ADDR, CONTROL_1_ADDR, CONTROL_2_ADDR
import RPi.GPIO as GPIO
from serial import Serial
import smbus

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for i in LED_GPIO_CODE:
    GPIO.setup(i, GPIO.OUT)

bus = smbus.SMBus(1)

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

        rounded_pos = int(len(LED_GPIO_CODE) * self.position.x / WORLD_WIDTH)
        for port, status in zip(LED_GPIO_CODE, map(lambda x: x == rounded_pos, range(len(LED_GPIO_CODE)))):
            GPIO.output(port, status)

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
            bus.write_byte(CONTROL_I2C_ADDR, self.control_address)
            tmp = bus.read_word_data(CONTROL_I2C_ADDR, 0x00)
            swap_tmp = ((tmp & 0x00FF) << 6) | ((tmp & 0xFF00) >> 10 )
            height_ratio = swap_tmp / float(0b1111111111)
            self.position = Vector(self.position.x, height_ratio * WORLD_HEIGHT)
            self.velocity = Vector(0, 0)

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
        self.left_bat = Bat(CONTROL_1_ADDR, Vector(3, 18), Vector(1, 3), Vector(0, 0), terminal_writer.COLOUR_GREEN)
        self.right_bat = Bat(CONTROL_2_ADDR, Vector(76, 18), Vector(1, 3), Vector(0, 0), terminal_writer.COLOUR_CYAN)
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
    schedule = Scheduler()
    schedule.insert(lambda x: pong.update(x), 60.0)
    schedule.insert(lambda x: pong.render(), 15.0)
    schedule.start()
