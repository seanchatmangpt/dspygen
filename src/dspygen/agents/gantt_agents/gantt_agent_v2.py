from enum import Enum, auto

from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger

# Define the states for the Gantt agent
class GanttState(Enum):
    INITIALIZING = auto()
    PLANNING = auto()
    EXECUTING = auto()
    MONITORING = auto()
    COMPLETING = auto()

# Define the GanttAgent class with FSM
class GanttAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.setup_fsm(state_enum=GanttState, initial=GanttState.INITIALIZING)

    @trigger(source=GanttState.INITIALIZING, dest=GanttState.PLANNING)
    def start_planning(self):
        ...

    @trigger(source=GanttState.PLANNING, dest=GanttState.EXECUTING)
    def start_execution(self):
        ...

    @trigger(source=GanttState.EXECUTING, dest=GanttState.MONITORING)
    def start_monitoring(self):
        ...

    @trigger(source=GanttState.MONITORING, dest=GanttState.COMPLETING)
    def complete_tasks(self):
        ...

    @trigger(source=GanttState.COMPLETING, dest=GanttState.INITIALIZING)
    def reset(self):
        ...

