#!/usr/bin/env python2

import init_state
from scheduler import Scheduler
from pong import Pong

if __name__ == "__main__":
    init_state.init()
    pong = Pong()
    schedule = Scheduler()
    schedule.insert(lambda x: pong.update(x), 60.0)
    schedule.insert(lambda x: pong.render(), 15.0)
    schedule.start()
