#!/usr/bin/env python2

"""
This module provides objects for sequencing the PiGLow
"""

import py_glow
import wave_gen

class GlowPattern(object):
    """This object represents a pattern which can be displayed on the PiGlow

    Arguments:
        expire_time: The point in time where the pattern is considered
            exhausted
    """
    def __init__(self):
        self.light_function_association = {led: wave_gen.ConstantSignal(0) for led in py_glow.LED_LIST}

    def sample(self, sample_time):
        return {x: self.light_function_association[x].sample(sample_time)
                for x in py_glow.LED_LIST}

    def insert(self, led_code, pattern_wave):
        self.light_function_association[led_code] = pattern_wave

class GlowSequencer(object):
    def __init__(self, pi_glow_obj = py_glow.PyGlow()):
        self.current_time = 0.0
        self.pi_glow_obj = pi_glow_obj
        self.pattern_stack = []

    def insert(self, pattern, duration):
        self.pattern_stack.append((pattern, duration + self.current_time))

    def sample(self, time_delta):
        self.current_time += time_delta
        self.pattern_stack = filter(lambda pattern: pattern[1] > self.current_time, self.pattern_stack)
        sample_buffer = {led: 0.0 for led in py_glow.LED_LIST}
        for pattern in self.pattern_stack:
            sample_buffer.update(pattern[0].sample(self.current_time))
        for (led, value) in sample_buffer.items():
            self.pi_glow_obj.led(led, value)
