#!/usr/bin/env python2

"""
This module initialises the global constants
"""

import consts
import RPi.GPIO as GPIO
import smbus
from serial import Serial
import sequencer
import wave_gen
import wave_trans
from note_gen import get_frequency, ChromaticSeries

def init():
    consts.BUS = smbus.SMBus(1)

    # Setup the GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Setup all of the LED GPIO ports for writing out
    for i in consts.LED_GPIO_CODE:
        GPIO.setup(i, GPIO.OUT)

    # Setup all of the controller buttons for reading in
    for i in [consts.PLAYER_1_SERVE,
              consts.PLAYER_2_SERVE,
              consts.PLAYER_1_ENLARGE,
              consts.PLAYER_2_ENLARGE]:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup the serial link for the display
    consts.SERIAL_OUTPUT = Serial("/dev/ttyAMA0", 38400)

    seq = sequencer.Sequencer()

    # Define the music
    music = [(ChromaticSeries.C, 0, 4, 0.0, 0.4), (ChromaticSeries.C, 0, 4, 0.5, 0.9),
             (ChromaticSeries.G, 0, 4, 1.0, 1.4), (ChromaticSeries.G, 0, 4, 1.5, 1.9),
             (ChromaticSeries.A, 0, 5, 2.0, 2.4), (ChromaticSeries.A, 0, 5, 2.5, 2.9),
             (ChromaticSeries.G, 0, 4, 3.0, 3.9),
             (ChromaticSeries.F, 0, 4, 4.0, 4.4), (ChromaticSeries.F, 0, 4, 4.5, 4.9),
             (ChromaticSeries.E, 0, 4, 5.0, 5.4), (ChromaticSeries.E, 0, 4, 5.5, 5.9),
             (ChromaticSeries.D, 0, 4, 6.0, 6.4), (ChromaticSeries.D, 0, 4, 6.5, 6.9),
             (ChromaticSeries.C, 0, 4, 7.0, 7.9),
             (ChromaticSeries.G, 0, 4, 8.0, 8.4), (ChromaticSeries.G, 0, 4, 8.5, 8.9),
             (ChromaticSeries.F, 0, 4, 9.0, 9.4), (ChromaticSeries.F, 0, 4, 9.5, 9.9),
             (ChromaticSeries.E, 0, 4, 10.0, 10.4), (ChromaticSeries.E, 0, 4, 10.5, 10.9),
             (ChromaticSeries.D, 0, 4, 11.0, 11.9),
             (ChromaticSeries.G, 0, 4, 12.0, 12.4), (ChromaticSeries.G, 0, 4, 12.5, 12.9),
             (ChromaticSeries.F, 0, 4, 13.0, 13.4), (ChromaticSeries.F, 0, 4, 13.5, 13.9),
             (ChromaticSeries.E, 0, 4, 14.0, 14.4), (ChromaticSeries.E, 0, 4, 14.5, 14.9),
             (ChromaticSeries.D, 0, 4, 15.0, 15.9),
             (ChromaticSeries.C, 0, 4, 16.0, 16.4), (ChromaticSeries.C, 0, 4, 16.5, 16.9),
             (ChromaticSeries.G, 0, 4, 17.0, 17.4), (ChromaticSeries.G, 0, 4, 17.5, 17.9),
             (ChromaticSeries.A, 0, 5, 18.0, 18.4), (ChromaticSeries.A, 0, 5, 18.5, 18.9),
             (ChromaticSeries.G, 0, 4, 19.0, 19.9),
             (ChromaticSeries.F, 0, 4, 20.0, 20.4), (ChromaticSeries.F, 0, 4, 20.5, 20.9),
             (ChromaticSeries.E, 0, 4, 21.0, 21.4), (ChromaticSeries.E, 0, 4, 21.5, 21.9),
             (ChromaticSeries.D, 0, 4, 22.0, 22.4), (ChromaticSeries.D, 0, 4, 22.5, 22.9),
             (ChromaticSeries.C, 0, 4, 23.0, 23.9)]
    
    for (series, a, b, c, d) in music:
        seq.insert(wave_gen.SquareWave(get_frequency(series, a, b)), c, d)

    # Loop the music infinitely and store it
    consts.MUSIC_SEQ = wave_trans.Loop(seq, 24.5)

    # Place the music into the mixer
    consts.MIXER_QUEUE.put((consts.MUSIC_SEQ, float("inf")))

    # Setup the GPIO port for the buzzer to output
    GPIO.setup(consts.BUZZER_GPIO_CODE, GPIO.OUT)
