#!/usr/bin/env python2

import consts
import init_state
from scheduler import Scheduler
from pong import Pong
from mixer import Mixer
import time
import multiprocessing
if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
    import RPi.GPIO as GPIO

def mixer_process_function():
    mixer = Mixer(lambda x: GPIO.output(consts.BUZZER_GPIO_CODE, x > 0.0))
    time_old = time.time()
    while True:
        time_now = time.time()
        while not consts.MIXER_QUEUE.empty():
            mixer.insert(*consts.MIXER_QUEUE.get())
        time_delta = time_now - time_old
        mixer.sample(time_delta)
        time_old = time_now

if __name__ == "__main__":
    init_state.init()
    pong = Pong()
    schedule = Scheduler()
    schedule.insert(lambda x: pong.update(x), 60.0)
    schedule.insert(lambda x: pong.render(), 15.0)
    if consts.CURRENT_TARGET == consts.PossibleTargets.RBPI:
        sound_process = multiprocessing.Process(target = mixer_process_function)
        sound_process.start()
    schedule.start()
