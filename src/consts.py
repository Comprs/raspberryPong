#!/usr/bin/env python2

"""This module contains the global constants to be used by the program"""

import multiprocessing
import wave_gen
import wave_trans

class PossibleTargets:
    GENERIC_TERMINAL = 0
    RBPI = 1

CURRENT_TARGET = PossibleTargets.GENERIC_TERMINAL

WORLD_WIDTH = 80
WORLD_HEIGHT = 40
LED_GPIO_CODE = [5, 6, 12, 13, 16, 19, 20, 26]
BUZZER_GPIO_CODE = 2
CONTROL_I2C_ADDR = 0x21
CONTROL_1_ADDR = None
CONTROL_2_ADDR = None

BUS = None
SERIAL_OUTPUT = None

PLAYER_1_SERVE = 10
PLAYER_2_SERVE = 11

PLAYER_1_ENLARGE = 9
PLAYER_2_ENLARGE = 8

MUSIC_SEQ = None
MIXER_QUEUE = multiprocessing.Queue()

BALL_BOUNCE_SFX = wave_trans.attack_and_sustain(wave_trans.VaryWave(wave_gen.SquareWave(400),
                                                                    wave_gen.SquareWave(800),
                                                                    wave_gen.SineWave(12)),
                                                0, 0, 0.25)

INPUT_THRESHOLD = 0
VOLTS = 3
VMIN = 0.5
VMAX = 2.5
