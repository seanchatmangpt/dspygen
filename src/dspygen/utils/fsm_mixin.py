import inspect

from transitions import Machine
import functools
from enum import Enum, auto

from transitions.core import State


from transitions import Machine
import functools
from enum import Enum, auto

import inspect
import functools
from transitions import Machine

import inspect
import functools
from transitions import Machine


# A decorator that adds transition metadata to methods
def trigger(source, dest, conditions=None, unless=None, before=None, after=None, prepare=None):
    def decorator(func):
        if not hasattr(func, '_transitions'):
            func._transitions = []
        func._transitions.append({
            'trigger': func.__name__,
            'source': source,
            'dest': dest,
            'conditions': conditions or [],
            'unless': unless or [],
            'before': before,
            'after': after,
            'prepare': prepare
        })

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Execute any 'prepare' callbacks
            if prepare:
                [getattr(self, p)() for p in (prepare if isinstance(prepare, list) else [prepare])]

            # Check 'unless' conditions to prevent transition
            if unless and any([getattr(self, u)() for u in (unless if isinstance(unless, list) else [unless])]):
                return func(self, *args, **kwargs)

            # Check 'conditions' to allow transition
            if conditions is None or all(
                    [getattr(self, c)() for c in (conditions if isinstance(conditions, list) else [conditions])]):
                if before:
                    [getattr(self, b)() for b in (before if isinstance(before, list) else [before])]

                # Correctly trigger the transition through the state machine
                event_trigger = getattr(self, 'trigger')
                event_trigger(func.__name__)

                result = func(self, *args, **kwargs)  # Execute the actual function logic

                if after:
                    [getattr(self, a)() for a in (after if isinstance(after, list) else [after])]
                return result

            return func(self, *args, **kwargs)  # Conditions not met, no transition

        return wrapper

    return decorator


class FSMMixin:
    def setup_fsm(self, state_enum, initial):
        self.states = [State(state.name) for state in state_enum]
        self.machine = Machine(model=self, states=self.states, initial=initial, auto_transitions=False)
        self.initialize_transitions()

    def initialize_transitions(self):
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(method, '_transitions'):
                for trans in method._transitions:
                    self.machine.add_transition(**trans)


def state_transition_possibilities(fsm):
    current_state = fsm.state
    transitions = fsm.machine.get_transitions()
    return [transition.dest for transition in transitions if transition.source == current_state]
