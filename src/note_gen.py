#!/usr/bin/env python2

"""
This module provides a convenience function for generating frequencies for
waves based on musical notes.

These frequencies are based on the frequencies of the sound waves created by a
piano. This module also takes C4 (octave 4) to be middle C
"""

class ChromaticSeries:
    """A chromatic series "enum" based on the semitone offset between each note"""
    A = 0
    B = 2
    C = 3
    D = 5
    E = 7
    F = 8
    G = 10

class ChromaticHalfStep:
    """An "enum" for each half step with the relative semitone difference between
    associated with them
    """
    Null = 0
    Sharp = 1
    Flat = -1

def get_frequency(chromatic_note, chromatic_half_step, octave):
    """Get the frequency of the given note specifications

    Arguments:
        chromatic_note: The note (C, D, E, etc) in which to get a frequency
        chromatic_half_step: The half set in which to get a frequency
        octave: The octave in which to get the frequency
    """
    if chromatic_note == ChromaticSeries.C and chromatic_half_step == ChromaticHalfStep.Flat:
        raise ValueError("Note cannot be \"C\" and \"Flat\"")
    if chromatic_note == ChromaticSeries.E and chromatic_half_step == ChromaticHalfStep.Sharp:
        raise ValueError("Note cannot be \"E\" and \"Sharp\"")
    if chromatic_note == ChromaticSeries.F and chromatic_half_step == ChromaticHalfStep.Flat:
        raise ValueError("Note cannot be \"C\" and \"Flat\"")
    if chromatic_note == ChromaticSeries.B and chromatic_half_step == ChromaticHalfStep.Sharp:
        raise ValueError("Note cannot be \"E\" and \"Sharp\"")
    n = 12 * octave + chromatic_note + chromatic_half_step
    return 440.0 * 2.0 ** ((n - 49.0) / 12.0)
