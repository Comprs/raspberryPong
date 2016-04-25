#!/usr/bin/env python2

"""
A module containing the classes to generate simple waves
"""

import math

class SineWave(object):
    def __init__(self, frequency):
        self.frequency = frequency

    def sample(self, time):
        return math.sin(time * self.frequency * math.pi * 2.0)

class SquareWave(object):
    def __init__(self, frequency, duty = 0.5):
        self.period = 1.0 / frequency
        self.duty = duty

    def sample(self, time):
        return float(time % self.period < self.period * self.duty) * 2.0 - 1.0

class SawtoothWave(object):
    def __init__(self, frequency):
        self.period = 1.0 / frequency

    def sample(self, time):
        return 2.0 * (time / self.period - math.floor(0.5 + time / self.period))

class TriangleWave(object):
    def __init__(self, frequency):
        self.sawtooth_wave = SawtoothWave(frequency)

    def sample(self, time):
        return 2.0 * abs(self.sawtooth_wave.sample(time)) - 1.0

class ConstantSignal(object):
    def __init__(self, signal_value):
        self.signal_value = signal_value

    def sample(self, time):
        return self.signal_value
