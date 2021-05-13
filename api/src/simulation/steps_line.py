from __future__ import annotations

from enum import Enum


class STEPS(Enum):
    BRING_MENU = {
        'actions': ['go_to_table', 'bring_menu'],
        'next_step': 'take_order'
    }
    TAKE_ORDER = {
        'actions': ['take_order'],
        'next_step': 'send_order'
    }
    SEND_ORDER = {
        'actions': ['go_to_kitchen', 'send_order'],
        'next_step': 'serve_table'
    }
    SERVE_TABLE = {
        'actions': ['go_to_table', 'serve_table'],
        'next_step': 'clean_table'
    }
    CLEAN_TABLE = {
        'actions': ['go_to_table', 'clean'],
        'next_step': 'bring_menu'
    }


class WaitersLine(object):
    def __init__(self, steps, next_step=None):
        self.next_step = next_step
        self.steps = steps

    @classmethod
    def target_step(cls, target: str) -> WaitersLine:
        processes = {}

        for step in STEPS:
            next_step = None if step.value["next_step"] is None else (step.value["next_step"]).upper()
            processes[step.name] = WaitersLine(step.value["actions"], next_step)

        line = processes.get(target, lambda: "Invalid process in fabric")
        return line
