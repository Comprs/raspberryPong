#!/usr/bin/env python2

import consts

if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
    import RPi.GPIO as GPIO
    import smbus

if consts.CURRENT_TARGET == consts.PossibleTargets.GENERIC_TERMINAL:
    import sys

def init():
    if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
        consts.BUS = smbus.SMBus(1)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for i in const.LED_GPIO_CODE:
            GPIO.setup(i, GPIO.OUT)

        consts.SERIAL_OUTPUT = Serial("/dev/ttyAMA0", 38400)

        consts.CONTROL_1_ADDR = 0x10

    if consts.CURRENT_TARGET == consts.PossibleTargets.GENERIC_TERMINAL:
        consts.SERIAL_OUTPUT = sys.stdout


