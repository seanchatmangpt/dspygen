import inspect

from transitions import Machine
from transitions.core import State
from dspygen.modules.fsm_trigger_module import fsm_trigger_call

import functools


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
            # if prepare:
            #     [getattr(self, p)() for p in (prepare if isinstance(prepare, list) else [prepare])]

            # Check 'unless' conditions to prevent transition
            if unless and any([getattr(self, u)() for u in (unless if isinstance(unless, list) else [unless])]):
                return func(self, *args, **kwargs)

            # Check 'conditions' to allow transition
            if conditions is None or all(
                    [getattr(self, c)() for c in (conditions if isinstance(conditions, list) else [conditions])]):
                # if before:
                #     [getattr(self, b)() for b in (before if isinstance(before, list) else [before])]

                # Correctly trigger the transition through the state machine
                event_trigger = getattr(self, 'trigger')
                event_trigger(func.__name__)

                result = func(self, *args, **kwargs)  # Execute the actual function logic

                # if after:
                #     [getattr(self, a)() for a in (after if isinstance(after, list) else [after])]
                return result

            return func(self, *args, **kwargs)  # Conditions not met, no transition

        return wrapper

    return decorator


class FSMMixin:
    def __init__(self):
        self.states = []
        self.machine = None
        self.state = None

    def setup_fsm(self, state_enum, initial=None):
        self.states = [State(state.name) for state in state_enum]

        if initial is None:
            initial = [state for state in state_enum][0]

        self.machine = Machine(model=self, states=self.states, initial=initial, auto_transitions=False)
        self.initialize_transitions()
        self.setup_transitions()

    def setup_transitions(self):
        pass

    def initialize_transitions(self):
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(method, '_transitions'):
                for trans in method._transitions:
                    self.add_transition(**trans)

    def add_transition(self, trigger, source, dest, conditions=None, unless=None, before=None, after=None,
                       prepare=None):
        self.machine.add_transition(trigger, source, dest, conditions=conditions, unless=unless, before=before,
                                    after=after, prepare=prepare)

    def possible_transitions(self):
        return state_transition_possibilities(self)

    def possible_triggers(self):
        # Get possible destination states from the current state
        return self.machine.get_triggers(self.state)

    def prompt(self, prompt, **kwargs):
        return fsm_trigger_call(prompt, self, **kwargs)


def state_transition_possibilities(fsm):
    current_state = fsm.state
    transitions = fsm.machine.get_transitions()
    return [transition.dest for transition in transitions if transition.source == current_state]
