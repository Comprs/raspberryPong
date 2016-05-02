#/usr/bin/env python2

"""
This module contains the mixer class
"""

import struct
import wave_trans

class Mixer(object):
    """The mixer accepts and combines multiple sound so that they may be mixed
    together.

    Arguments:
        write_out_callback: the function in which to provide a value to when
            sampled
    """
    def __init__(self, write_out_callback):
        self.write_out_callback = write_out_callback
        self.position = 0.0
        self.sounds = []

    def insert(self, wave, duration):
        """Insert a new wave to be mixed

        Arguments:
            wave: the sound itself
            duration: the length of time to play the sound
        """
        self.sounds.append(wave_trans.TimedWave(wave, self.position, self.position + duration))

    def sample(self, time_delta):
        """Sample the current state of the wave given the time since the last
        sample

        Arguments:
            time_delta: The time since the last sample
        """
        # Update the current time
        self.position += time_delta
        # Remove all of the sounds which have exceeded their play time
        self.sounds = filter(lambda x: x.end_point >= self.position, self.sounds)
        # Write out to the callback a sum of all of the samples taken from
        # the current sounds at the current sample point
        self.write_out_callback(sum(filter(lambda x: x != None, map(lambda x: x.sample(self.position), self.sounds))) * 0.1)
