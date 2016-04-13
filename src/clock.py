#!/usr/bin/env python2

import time

class Clock(object):
    def __init__(self, target_framerate = None):
        if target_framerate == None:
            self.frame_time = 0.0
        else:
            self.frame_time = 1.0 / target_framerate
        self.time_1 = time.time()
        self.time_2 = self.time_1
        self.time_delta = 0

    def tick(self):
        self.time_1 = time.time()
        self.time_delta = self.time_1 - self.time_2
        wait_time = self.frame_time - self.time_delta
        if wait_time > 0:
            time.sleep(wait_time)
            self.time_1 = time.time()
            self.time_delta = self.time_1 - self.time_2
        self.time_2 = self.time_1

    def get_time_delta(self):
        return self.time_delta
