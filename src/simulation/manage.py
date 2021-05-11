from __future__ import annotations

import random
import simpy

from typing import Generator, Any
from simpy import Timeout, Event

from src.simulation.steps_line import WaitersLine

processes_flow_logs = []
lot_times = []
working_waiters = 0


class Source:
    def __init__(self, env: simpy.Environment, attributes: object) -> None:
        self.env = env
        self.attributes = attributes

    @property
    def setup(self) -> Generator[Timeout, Any, None]:
        global working_waiters
        process = Restaurant(self.env, self.attributes, self.attributes.work_count)

        # Create initial waiters
        for working_waiters in range(self.attributes.workers):
            self.__start_process(working_waiters, process)

        # Time for recreate a new process
        yield self.env.timeout(1)

    def __start_process(self, count: int, process: Restaurant) -> None:
        waiter_identifier = 'Waiter [%d]:' % count
        processes_flow_logs.append('%s started his shift at %.2f.' % (waiter_identifier, self.env.now))
        self.env.process(waiter(self.env, waiter_identifier, process, target='BRING_MENU'))


class Restaurant(object):
    FLOW_LOGS_MESSAGE = '%s on %s step at %.2f.'

    def __init__(self, env: simpy.Environment, attributes: object, workers: int) -> None:
        self.env = env
        self.attributes = attributes
        self.workers = simpy.Resource(env, workers)

    def waiter_step(self, worker: str, next_step: str, steps: list) -> None:
        if next_step is not None:
            self.env.process(waiter(self.env, worker, process=self, target=next_step))

        for step in steps:
            yield self.env.timeout(self.attributes.times[step])
            processes_flow_logs.append(self.FLOW_LOGS_MESSAGE % (worker, step, self.env.now))


def waiter(env, name: str, process: Restaurant, target: str) -> Generator[Event, Any, Any]:
    with process.workers.request() as request:
        yield request
        line = WaitersLine.target_step(target)

        processes_flow_logs.append('%s enters the %s station at %.2f.' % (name, target, env.now))
        yield env.process(process.waiter_step(name, line.next_step, line.steps))
        processes_flow_logs.append('%s leaves the %s station at %.2f.' % (name, target, env.now))

        if line.next_step is None:
            lot_times.append(env.now)


def simulation(attrs: object) -> None:
    working_minutes_per_day = attrs.working_hours * 60
    random.seed(attrs.random_seed)

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(Source(env, attrs).setup)

    # Execution
    env.run(until=attrs.working_days * working_minutes_per_day)
