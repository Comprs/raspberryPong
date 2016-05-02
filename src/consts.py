#!/usr/bin/env python2

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
BUZZER_GPIO_CODE = 10
CONTROL_I2C_ADDR = 0x21
CONTROL_1_ADDR = None
CONTROL_2_ADDR = None

BUS = None
SERIAL_OUTPUT = None

MUSIC_SEQ = None
MIXER_QUEUE = multiprocessing.Queue()

BALL_BOUNCE_SFX = wave_trans.attack_and_sustain(wave_trans.VaryWave(wave_gen.SquareWave(400),
                                                                    wave_gen.SquareWave(800),
                                                                    wave_gen.SineWave(12)),
                                                0, 0, 0.25)
