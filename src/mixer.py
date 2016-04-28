#/usr/bin/env python2

import struct
import wave_trans

class Mixer(object):
    def __init__(self, write_out_callback):
        self.write_out_callback = write_out_callback
        self.position = 0.0
        self.sounds = []

    def insert(self, wave, duration):
        self.sounds.append(wave_trans.TimedWave(wave, self.position, self.position + duration))

    def sample(self, time_delta):
        self.position += time_delta
        self.sounds = filter(lambda x: x.end_point >= self.position, self.sounds)
        self.write_out_callback(sum(filter(lambda x: x != None, map(lambda x: x.sample(self.position), self.sounds))) * 0.1)
