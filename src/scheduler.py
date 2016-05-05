#!/usr/bin/env python2

"""
This module implements a scheduler which can then be used to schedule tasks
which need to be performed at set and constant frequencies. Each individual
task may have a different scheduling frequency.
"""

import time
import heapq
import functools

@functools.total_ordering
class Task(object):
    """A class representing a task.

    It holds a function which is the task itself and other timekeeping values
    regarding when the task was last run, when it should be run next and the
    desired time period between task runs. The object itself is order able based
    on the next run value so that it can be easier to select which task to run
    next in a collection.

    Additionally, this class is meant to be directly manipulated by the
    Scheduler. This means no helper methods are implemented.

    Arguments:
        function: The function to be run as the task. It should accept a
                  time delta since the last call.
        frequency: The number of times per second to perform the task.
    """

    def __init__(self, function, frequency):
        self.function = function
        self.period = 1.0 / frequency
        self.last_run = time.time()
        self.next_run = self.last_run

    def __lt__(self, other):
        return self.next_run < other.next_run

    def __eq__(self, other):
        return self.next_run == other.next_run

class Scheduler(object):
    """A Scheduler class which schedules and executes Task objects

    The Scheduler should be loaded with task to perform using the insert method
    and then can be started using the start method.
    """

    def __init__(self):
        self.task_queue = []

    def insert(self, function, frequency):
        """Insert a task to be executed periodically

        Arguments:
            function: The function to be run as the task. It should accept a
                      time delta since the last call.
            frequency: The number of times per second to perform the task.
        """
        heapq.heappush(self.task_queue, Task(function, frequency))

    def start(self):
        """Start the scheduler running

        It is not expected to return from this method
        """
        while True:
            # Get the reference point to this instance in time
            time_now = time.time()

            # Calculate the time we have to wait based on the time until the
            # next task is due to run
            wait_time = self.task_queue[0].next_run - time_now

            # If we can wait, do wait and then update the temporal reference
            if wait_time > 0:
                time.sleep(wait_time)
                time_now = time.time()

            # Get the immediate task to perform
            task = heapq.heappop(self.task_queue)

            # Get the time difference between the last time the function was run
            # and this instance so the task can compensate for lost or gained
            # time.
            update_time = time_now - task.last_run
            task.function(update_time)

            # Update the time tracking variables of the task
            task.last_run = time_now
            task.next_run = time_now + task.period

            # Place the task back into the queue
            heapq.heappush(self.task_queue, task)
