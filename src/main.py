#!/usr/bin/env python2

import consts
import init_state
from scheduler import Scheduler
from pong import Pong
from mixer import Mixer

if __name__ == "__main__":
    init_state.init()
    pong = Pong()
    mixer = Mixer(lambda x: None)
    mixer.insert(consts.MUSIC_SEQ, float("inf"))
    schedule = Scheduler()
    schedule.insert(lambda x: pong.update(x), 60.0)
    schedule.insert(lambda x: pong.render(), 15.0)
    if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
        schedule.insert(lambda x: mixer.sample(x), 44100.0)
    schedule.start()
