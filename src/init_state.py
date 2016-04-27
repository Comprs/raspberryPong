#!/usr/bin/env python2

import RPi.GPIO as GPIO
import smbus
import consts

def init():
    consts.BUS = smbus.SMBus(1)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in const.LED_GPIO_CODE:
        GPIO.setup(i, GPIO.OUT)

    consts.SERIAL_OUTPUT = Serial("/dev/ttyAMA0", 38400)
