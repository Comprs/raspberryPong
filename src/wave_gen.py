#!/usr/bin/env python2

"""
This module contains the Wave base class, basic wave primitives and basic ways
to adapt and manipulate waves
"""

import math

class Wave(object):
    """The Wave base class. This is not instantiated but provides ways to adapt
    a wave. It also contains the sample method which when called should return
    the value of the wave at the given time. This needs to be overridden by
    implementers of this class
    """

    def sample(self, time):
        return None

    def multiply(self, other):
        return Multiply(self, other)

    def multiply_const(self, value):
        return self.multiply(ConstantSignal(value))

    def add(self, other):
        return Add(self, other)

    def add_const(self, value):
        return self.add(ConstantSignal(value))

    def clip_right(self, clip_point):
        return ClipRight(self, clip_point)

    def clip_left(self, clip_point):
        return ClipLeft(self, clip_point)

    def transition(self, other, start_time, end_time):
        return Transition(self, other, start_time, end_time)

    def compress(self, magnitude):
        return Compress(self, magnitude)

    def vary_with(self, wave_1, wave_2):
        return VaryWave(wave_1, wave_2, self)

    def into_discrete_iter(self, sample_frequency):
        return DiscreteWaveIterator(self, sample_frequency)

class DiscreteWaveIterator(object):
    """A iterator which yields values sampled at the given frequency

    Arguments:
        wave: The wave which will be sampled
        sample_frequency: The number of points per second of time to sample
    """
    def __init__(self, wave, sample_frequency):
        self.wave = wave
        self.sample_period = 1.0 / sample_frequency
        self.next_sample = 0

    def __iter__(self):
        return self

    def next(self):
        # Sample the wave
        this_sample = self.wave.sample(self.next_sample)

        # The wave is exhausted given this result. Indicate the iterator has
        # come to and end
        if this_sample == None:
            raise StopIteration

        # Calculate the next point to sample for the next time this method is
        # called
        self.next_sample += self.sample_period
        return this_sample

class SineWave(Wave):
    def __init__(self, frequency):
        self.frequency = frequency

    def sample(self, time):
        return math.sin(time * self.frequency * math.pi * 2.0)

class SquareWave(Wave):
    def __init__(self, frequency, duty = 0.5):
        self.period = 1.0 / frequency
        self.duty = duty

    def sample(self, time):
        return float(time % self.period < self.period * self.duty) * 2.0 - 1.0

class SawtoothWave(Wave):
    def __init__(self, frequency):
        self.period = 1.0 / frequency

    def sample(self, time):
        return 2.0 * (time / self.period - math.floor(0.5 + time / self.period))

class TriangleWave(Wave):
    def __init__(self, frequency):
        self.sawtooth_wave = SawtoothWave(frequency)

    def sample(self, time):
        return 2.0 * abs(self.sawtooth_wave.sample(time)) - 1.0

class ConstantSignal(Wave):
    def __init__(self, signal_value):
        self.signal_value = signal_value

    def sample(self, time):
        return self.signal_value

class Multiply(Wave):
    def __init__(self, wave_1, wave_2):
        self.wave_1 = wave_1
        self.wave_2 = wave_2

    def sample(self, time):
        wave_1_value = self.wave_1.sample(time)
        wave_2_value = self.wave_2.sample(time)
        if wave_1_value == None or wave_2_value == None:
            return None
        return wave_1_value * wave_2_value

class Add(Wave):
    def __init__(self, wave_1, wave_2):
        self.wave_1 = wave_1
        self.wave_2 = wave_2

    def sample(self, time):
        wave_1_value = self.wave_1.sample(time)
        wave_2_value = self.wave_2.sample(time)
        if wave_1_value == None and wave_2_value == None:
            return None
        if wave_1_value == None:
            wave_1_value = 0.0
        if wave_2_value == None:
            wave_2_value = 0.0
        return wave_1_value * wave_2_value

class Average(Wave):
    def __init__(self, wave_1, wave_2):
        self.multiply_wave = Multiply(wave_1, wave_2)

    def sample(self, time):
        multiply_wave_value = self.multiply_wave.sample(time)
        if multiply_wave_value == None:
            return None
        return multiply_wave_value / 2.0

class ClipRight(Wave):
    def __init__(self, wave, clip_point):
        self.wave = wave
        self.clip_point = clip_point

    def sample(self, time):
        if time > self.clip_point:
            return None
        return self.wave.sample(time)

class ClipLeft(Wave):
    def __init__(self, wave, clip_point):
        self.wave = wave
        self.clip_point = clip_point

    def sample(self, time):
        if time < self.clip_point:
            return None
        return self.wave.sample(time)

class Transition(Wave):
    def __init__(self, wave_1, wave_2, start_time, end_time):
        self.wave_1 = wave_1
        self.wave_2 = wave_2
        self.start_time = start_time
        self.end_time = end_time

    def sample(self, time):
        wave_1_sample = self.wave_1.sample(time)
        wave_2_sample = self.wave_2.sample(time)
        if time < self.start_time:
            return wave_1_sample
        if time > self.end_time:
            return wave_2_sample
        if wave_1_sample == None:
            wave_1_sample = 0.0
        if wave_2_sample == None:
            wave_2_sample = 0.0
        transition_ratio = (time - self.start_time) / (self.end_time - self.start_time)
        return wave_1 * (1.0 - transition_ratio) + wave_2 * transition_ratio

class Compress(Wave):
    def __init__(self, wave, magnitude):
        self.wave = wave
        self.magnitude = magnitude

    def sample(self, time):
        return self.wave.sample(time * self.magnitude)

class VaryWave(Wave):
    def __init__(self, wave_1, wave_2, vary_wave):
        self.wave_1 = wave_1
        self.wave_2 = wave_2
        self.vary_wave = vary_wave

    def sample(self, time):
        vary_wave_sample = self.vary_wave.sample(time)
        wave_1_sample = self.wave_1.sample(time)
        wave_2_sample = self.wave_2.sample(time)
        if vary_wave_sample == None or (wave_1_sample == None and wave_2_sample == None):
            return None
        if wave_1_sample == None:
            wave_1_sample = 0.0
        if wave_2_sample == None:
            wave_2_sample = 0.0
        vary_ratio = (vary_wave_sample + 1.0) / 2.0
        return wave_1_sample * (1.0 - vary_ratio) + wave_2_sample * vary_ratio
