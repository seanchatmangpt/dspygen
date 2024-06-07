from enum import Enum, auto
from typing import List, Optional

import dspy
from pydantic import BaseModel, Field
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger

# Define the states for the Gantt agent
class GanttState(Enum):
    INITIALIZING = auto()
    PLANNING = auto()
    EXECUTING = auto()
    MONITORING = auto()
    COMPLETING = auto()

# Define the Task model
class Task(BaseModel):
    name: str
    status: Optional[str] = Field(None, description="Status of the task, e.g., 'done', 'active', 'crit', 'milestone'")
    id: Optional[str] = Field(None, description="ID of the task")
    start_date: Optional[str] = Field(None, description="Start date of the task in the format specified by dateFormat")
    end_date: Optional[str] = Field(None, description="End date of the task in the format specified by dateFormat")
    duration: Optional[str] = Field(None, description="Duration of the task")
    dependencies: Optional[str] = Field(None, description="Dependencies on other tasks using 'after' keyword")

# Define the Section model
class Section(BaseModel):
    name: str
    tasks: List[Task]

# Define the GanttChart model
class GanttChart(BaseModel):
    date_format: str = Field(..., alias='dateFormat', description="Format of the dates used in the Gantt chart")
    title: Optional[str] = Field(None, description="Title of the Gantt chart")
    excludes: Optional[str] = Field(None, description="Dates or days to be excluded, e.g., 'weekends', specific dates")
    sections: List[Section]
    tick_interval: Optional[str] = Field(None, alias='tickInterval', description="Interval for axis ticks")
    weekday: Optional[str] = Field(None, description="Start day of the week for tickInterval")
    axis_format: Optional[str] = Field(None, alias='axisFormat', description="Format of the dates on the axis")

# Define the GanttAgent class with FSM
class GanttAgent(FSMMixin):
    def __init__(self):
        super().__init__()
        self.task = None
        self.plan = None
        self.execution = None
        self.setup_fsm(state_enum=GanttState, initial=GanttState.INITIALIZING)

    @trigger(source=GanttState.INITIALIZING, dest=GanttState.PLANNING)
    def start_planning(self):
        print("Starting planning phase.")
        # self.plan = dspy.Predict("task -> plan")(task=self.task.model_dump_json()).plan
        self.plan = """Plan: 

1. Review the completed task details, including status and timeline.
2. Analyze any dependencies that were involved in this task to understand their impact on related tasks.
3. Update project documentation or records with the completion of this task for future reference.
4. Communicate the successful completion of the task to relevant stakeholders if necessary.
5. Assess and plan next steps, including any follow-up actions required due to dependencies or outcomes from this completed task."""
        self.start_execution()

    @trigger(source=GanttState.PLANNING, dest=GanttState.EXECUTING)
    def start_execution(self):
        print("Starting execution phase.")
        self.execution = dspy.Predict("plan -> execution")(plan=self.plan).execution
        self.start_monitoring()

    @trigger(source=GanttState.EXECUTING, dest=GanttState.MONITORING)
    def start_monitoring(self):
        print("Starting monitoring phase.")
        raise NotImplementedError("Monitoring phase not yet implemented.")

    @trigger(source=GanttState.MONITORING, dest=GanttState.COMPLETING)
    def complete_tasks(self):
        print("Completing all tasks.")
        raise NotImplementedError("Task completion not yet implemented.")

    @trigger(source=GanttState.COMPLETING, dest=GanttState.INITIALIZING)
    def reset(self):
        print("Resetting for a new cycle.")

# Example usage of GanttAgent and GanttChart
def main():
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    # Initialize the Gantt chart data
    gantt_chart = GanttChart(
        dateFormat="YYYY-MM-DD",
        title="Adding GANTT diagram functionality to mermaid",
        excludes="weekends",
        sections=[
            Section(
                name="A section",
                tasks=[
                    Task(name="Completed task", status="done", id="des1", start_date="2014-01-06", end_date="2014-01-08"),
                    Task(name="Active task", status="active", id="des2", start_date="2014-01-09", duration="3d"),
                    Task(name="Future task", id="des3", duration="5d", dependencies="after des2"),
                    Task(name="Future task2", id="des4", duration="5d", dependencies="after des3"),
                ]
            ),
            Section(
                name="Critical tasks",
                tasks=[
                    Task(name="Completed task in the critical line", status="crit, done", start_date="2014-01-06", duration="24h"),
                    Task(name="Implement parser and jison", status="crit, done", duration="2d", dependencies="after des1"),
                    Task(name="Create tests for parser", status="crit, active", duration="3d"),
                    Task(name="Future task in critical line", status="crit", duration="5d"),
                    Task(name="Create tests for renderer", duration="2d"),
                    Task(name="Add to mermaid", dependencies="until isadded"),
                    Task(name="Functionality added", status="milestone", id="isadded", start_date="2014-01-25", duration="0d"),
                ]
            ),
            Section(
                name="Documentation",
                tasks=[
                    Task(name="Describe gantt syntax", status="active", id="a1", duration="3d", dependencies="after des1"),
                    Task(name="Add gantt diagram to demo page", duration="20h", dependencies="after a1"),
                    Task(name="Add another diagram to demo page", id="doc1", duration="48h", dependencies="after a1"),
                ]
            ),
            Section(
                name="Last section",
                tasks=[
                    Task(name="Describe gantt syntax", duration="3d", dependencies="after doc1"),
                    Task(name="Add gantt diagram to demo page", duration="20h"),
                    Task(name="Add another diagram to demo page", duration="48h"),
                ]
            )
        ]
    )

    # Initialize the Gantt agent
    agent = GanttAgent()

    # Wild loop to iterate over all tasks in the Gantt chart
    def iterate_over_tasks(agent):
        for section in gantt_chart.sections:

            print(f"Section: {section.name}")
            for task in section.tasks:
                agent.task = task
                agent.prompt(f"Starting task {task.name}")
                print(f"Task: {task.name}, Status: {task.status}, Duration: {task.duration}")

    # Example usage
    iterate_over_tasks(agent)

if __name__ == '__main__':
    main()
