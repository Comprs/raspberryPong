#!/usr/bin/env python2

"""
Main execution point
"""

import consts
import init_state
from scheduler import Scheduler
from pong import Pong
from mixer import Mixer
import time
import multiprocessing
import RPi.GPIO as GPIO

def mixer_process_function():
    """This function is meant to be placed into is own process and loops in
    order to play the sounds without delay
    """
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
    # Initialise the global constants
    init_state.init()
    # Create the game object
    pong = Pong()
    # Create the scheduler and register some events
    schedule = Scheduler()
    schedule.insert(lambda x: pong.update(x), 60.0)
    schedule.insert(lambda x: pong.render(), 15.0)
    # Start the sound process
    sound_process = multiprocessing.Process(target = mixer_process_function)
    sound_process.start()
    # Start the scheduler
    schedule.start()
