#!/usr/bin/env python2

"""This module contains the global constants to be used by the program"""

import multiprocessing
import wave_gen
import wave_trans
import vector
import terminal_writer
import glow_seq
import math
import py_glow

WORLD_WIDTH = 80
WORLD_HEIGHT = 40
LED_GPIO_CODE = [5, 6, 12, 13, 16, 19, 20, 26]
BUZZER_GPIO_CODE = 4
CONTROL_I2C_ADDR = 0x21
CONTROL_1_ADDR = 0x10
CONTROL_2_ADDR = 0x40

BUS = None
SERIAL_OUTPUT = None

PLAYER_1_SERVE = 10
PLAYER_2_SERVE = 11

PLAYER_1_ENLARGE = 9
PLAYER_2_ENLARGE = 18

LEFT_BAT_RETURN_ANGLES = (math.pi * -0.25, 0, math.pi * 0.25)
LEFT_BAT_COLOUR = terminal_writer.COLOUR_GREEN
LEFT_BAT_INIT_POSITION = vector.Vector(3, 18)

RIGHT_BAT_RETURN_ANGLES = (math.pi * -0.75, math.pi, math.pi * 0.75)
RIGHT_BAT_COLOUR = terminal_writer.COLOUR_CYAN
RIGHT_BAT_INIT_POSITION = vector.Vector(76, 18)

BAT_SIZE = vector.Vector(1, 3)
BAT_ENLARGE_SIZE = vector.Vector(1, 5)
BAT_ENLARGE_TIME = 15.0

BALL_SIZE = vector.Vector(1, 1)
BALL_COLOUR = terminal_writer.COLOUR_YELLOW

MUSIC_SEQ = None
MIXER_QUEUE = multiprocessing.Queue()

BALL_BOUNCE_SFX = wave_trans.attack_and_sustain(wave_trans.VaryWave(wave_gen.SquareWave(400),
                                                                    wave_gen.SquareWave(800),
                                                                    wave_gen.SineWave(12)),
                                                0, 0, 0.25)

INPUT_THRESHOLD = 1.2
ADC_SIGNAL_MAX = 0b1000000000
ADC_RATIO_MIN = 0.5 / 3.0
ADC_RATIO_MAX = 2.5 / 3.0

NORMAL_PATTERN = glow_seq.GlowPattern()
for (index, tri_led) in enumerate(py_glow.COLOR_LED_LIST):
    sine_wave = wave_gen.SineWave(1.0 / 3.0)
    offset = wave_trans.Translate(sine_wave, index)
    if index == 0:
        mapped = wave_trans.Map(offset, lambda x: int((x + 1.0) * 32 + 1))
    else:
        mapped = wave_trans.Map(offset, lambda x: int((x + 1.0) * 64 + 1))
    for led in tri_led:
        NORMAL_PATTERN.insert(led, mapped)

SCORE_PATTERN = glow_seq.GlowPattern()
for (index, tri_led) in enumerate(py_glow.COLOR_LED_LIST):
    sine_wave = wave_gen.SineWave(1.0 / 3.0)
    offset = wave_trans.Translate(sine_wave, index)
    compressed = wave_trans.Compress(offset, 5)
    if index == 0:
        mapped = wave_trans.Map(compressed, lambda x: int((x + 1.0) * 32 + 1))
    else:
        mapped = wave_trans.Map(compressed, lambda x: int((x + 1.0) * 64 + 1))
    for led in tri_led:
        SCORE_PATTERN.insert(led, mapped)

SCORE_PATTERN_LENGTH = 3.0
