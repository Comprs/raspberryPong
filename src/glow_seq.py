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
        # Provide a sane default association for the LEDs
        self.light_function_association = {led: wave_gen.ConstantSignal(0) for led in py_glow.LED_LIST}

    def sample(self, sample_time):
        """Return a sample of the status of the LEDs given the current time

        Arguments:
            sample_time: The point in time to sample
        """
        # Go through all of the associated function and provide the time to
        # them in order to sample them
        return {x: self.light_function_association[x].sample(sample_time)
                for x in py_glow.LED_LIST}

    def insert(self, led_code, pattern_wave):
        """Associate a LED with a wave pattern

        Arguments:
            led_code: The numerical code of the led to associate a function with
            pattern_wave: The function to associate
        """
        self.light_function_association[led_code] = pattern_wave

class GlowSequencer(object):
    """This object sequences multiple patterns together with a provided lifetime

    Arguments:
        pi_glow_object: A PiGlow object to use internally. Defaults to
            initialising one itself
    """
    def __init__(self, pi_glow_obj = py_glow.PyGlow()):
        self.current_time = 0.0
        self.pi_glow_obj = pi_glow_obj
        self.pattern_stack = []

    def insert(self, pattern, duration):
        """Insert a new pattern into the sequencer

        Arguments:
            pattern: The pattern itself to insert
            duration: The length of time the pattern should last for
        """
        self.pattern_stack.append((pattern, duration + self.current_time))

    def sample(self, time_delta):
        """Write out the state of the patterns contained within the sequencer
        into the stored pi_glow_object

        Arguments:
            time_delta: The amount of time since the last call to this method
        """
        self.current_time += time_delta
        # Remove all of the expired patterns
        self.pattern_stack = filter(lambda pattern: pattern[1] > self.current_time, self.pattern_stack)
        # Create a buffer to sample into. Defaults to 0 which is LED off
        sample_buffer = {led: 0.0 for led in py_glow.LED_LIST}

        # Sample all of the patterns in the order in the pattern stack
        for pattern in self.pattern_stack:
            # Update the buffer replacing all of the previous values
            sample_buffer.update(pattern[0].sample(self.current_time))

        # Write out all of the sampled values
        for (led, value) in sample_buffer.items():
            self.pi_glow_obj.led(led, value)
