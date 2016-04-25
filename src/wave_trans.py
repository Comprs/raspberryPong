#!/usr/bin/env python2

"""
A module which contains wave adapters which are used to modify wave object which
have a sample method
"""

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

class TimedWave(object):
    """A class representing a single wave with timing information attached

    This is implemented as a wave itself. It automatically translates the start
    of the wave to the correct position in time and clips the wave as specified

    Arguments:
        wave: The wave which this item holds and samples
        start_point: The point in time in which the sound starts
        end_point: The point in time in which the sound ends
    """

    def __init__(self, wave, start_point, end_point):
        self.wave = wave
        self.start_point = start_point
        self.end_point = end_point

    def sample(self, time):
        """Sample the contained wave

        This delegates the retrieval of the value after applying time
        translation and clipping

        Arguments:
            time: The point in time to sample
        """
        if time < self.start_point or time > self.end_point:
            return None
        return self.wave.sample(time - self.start_point)

class Multiply(object):
    def __init__(self, wave_1, wave_2):
        self.wave_1 = wave_1
        self.wave_2 = wave_2

    def sample(self, time):
        wave_1_value = self.wave_1.sample(time)
        wave_2_value = self.wave_2.sample(time)
        if wave_1_value == None or wave_2_value == None:
            return None
        return wave_1_value * wave_2_value

class Add(object):
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

class Average(object):
    def __init__(self, wave_1, wave_2):
        self.multiply_wave = Multiply(wave_1, wave_2)

    def sample(self, time):
        multiply_wave_value = self.multiply_wave.sample(time)
        if multiply_wave_value == None:
            return None
        return multiply_wave_value / 2.0

class ClipRight(object):
    def __init__(self, wave, clip_point):
        self.wave = wave
        self.clip_point = clip_point

    def sample(self, time):
        if time > self.clip_point:
            return None
        return self.wave.sample(time)

class ClipLeft(object):
    def __init__(self, wave, clip_point):
        self.wave = wave
        self.clip_point = clip_point

    def sample(self, time):
        if time < self.clip_point:
            return None
        return self.wave.sample(time)

class Transition(object):
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

class Compress(object):
    def __init__(self, wave, magnitude):
        self.wave = wave
        self.magnitude = magnitude

    def sample(self, time):
        return self.wave.sample(time * self.magnitude)

class VaryWave(object):
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
