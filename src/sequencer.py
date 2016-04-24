#!/usr/bin/env python2

"""
This module implements a sequencer which is used to arrange and mix numerous
waves together
"""

import math
from wave_gen import Wave

class SequencerItem(Wave):
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

class Sequencer(Wave):
    """A class which sequences waves

    This holds a list of lists of sequencer items. The top level list is split
    into time chunks of chunk_granularity length. The next level contains all
    of the sequencer items which exist, even partially, in this chunk.

    Arguments:
        chunk_granularity: The size of each chunk
    """

    def __init__(self, chunk_granularity = 0.5):
        self.chunks = [[]]
        self.chunk_granularity = chunk_granularity

    def insert(self, wave, start_point, end_point):
        """Insert a wave into the sequencer with the given time range

        Arguments:
            wave: The wave to insert
            start_point: The start time position of the wave
            end_point: The end time position of the wave
        """
        # Sanity check the time point parameters
        if end_point <= start_point:
            raise ValueError("The end point ({}s) of the wave must be"
                             "chronologically after the start point ({}s)"
                             .format(end_point, start_point))
        if start_point < 0:
            raise ValueError("The start point ({}s) must be larger than zero"
                             .format(start_point))

        # Wrap the wave and associated wave points into an item for insertion
        item = SequencerItem(wave, start_point, end_point)

        # Calculate the bounding indexes of the wave for the chunk list
        start_index = int(math.floor(start_point / self.chunk_granularity))
        end_index = int(math.ceil(end_point / self.chunk_granularity))

        # Add any additional storage space
        while len(self.chunks) < end_index + 1:
            self.chunks.append([])

        # Add the item to all of the appropriate lists
        for i in range(start_index, end_index + 1):
            self.chunks[i].append(item)

    def get_samples(self, time):
        """Sample the sequencer at the given time

        Arguments:
            time: The sample time
        """
        # If outside of the time covered by the sequencer, there can be no
        # waves to sample. With this information we can just not sample
        # anything and just return nothing
        if time > len(self.chunks) * self.chunk_granularity or time < 0:
            return None

        # Get the index of which the waves to be sampled exist in
        index = int(math.floor(time / self.chunk_granularity))

        # Sample all of the waves in the deduced check and filter out any
        # values which are None
        return filter(lambda sample: sample != None,
                      map(lambda wave: wave.sample(time), self.chunks[index]))

    def sample_sum(self, time):
        """Sample the sequencer and return the sum of all sampled waves

        Arguments:
            time: The point in time to sample
        """
        samples = self.get_samples(time)
        # The sampling function has indicated there is nothing left going
        # forward; pass this information up.
        if samples == None:
            return None
        # If no samples are collected, there is no sound be played at this time
        if len(samples) == 0:
            return 0.0
        # Perform the sum
        return sum(samples)

    def sample_average(self, time):
        """Sample the sequencer and return the average of all sampled waves

        Arguments:
            time: The point in time to sample
        """
        samples = self.get_samples(time)
        # The sampling function has indicated there is nothing left going
        # forward; pass this information up.
        if samples == None:
            return None
        # If no samples are collected, there is no sound be played at this time
        if len(samples) == 0:
            return 0.0
        # Perform the average
        return sum(samples) / len(samples)

    def sample(self, time):
        """Sample the sequencer at the given time. The current implementation
        just delegates this onto the sample_sum as that seems the best way to
        mix the waves

        Arguments:
            time: The point in time to sample
        """
        return self.sample_sum(time)
