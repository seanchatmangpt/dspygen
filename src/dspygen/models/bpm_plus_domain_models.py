from pydantic import BaseModel, Field
from typing import List, Optional

from dspygen.utils.yaml_tools import YAMLMixin



class Flow(BaseModel):
    """
    Represents a flow within a BPMN process, defining the sequence or message flow between elements.
    """
    id: str = Field(..., description="The unique identifier for the flow.")
    sourceRef: str = Field(..., description="The source element of the flow.")
    targetRef: str = Field(..., description="The target element the flow points to.")
    condition: Optional[str] = Field(None, description="The condition that determines whether the flow is taken.")

class Task(BaseModel):
    """
    Represents a task within a BPMN process. A task is a unit of work within a process.
    """
    id: str = Field(..., description="The unique identifier for the task.")
    name: str = Field(..., description="The name of the task.")
    type: str = Field(..., description="The type of the task, e.g., 'serviceTask', 'userTask'.")
    properties: Optional[dict] = Field(default=None, description="Additional properties of the task, defined as a dictionary.")

class Process(BaseModel):
    """
    Represents a BPMN process, which is a collection of tasks and flows that define the workflow.
    """
    id: str = Field(..., description="The unique identifier for the process.")
    name: str = Field(..., description="The name of the process.")
    tasks: List[Task] = Field(..., description="A list of tasks within the process.")
    flows: List[Flow] = Field(..., description="A list of flows that define the sequence and message flows within the process.")

class BPMN(BaseModel, YAMLMixin):
    """
    Defines a BPMN model, which may contain one or more processes. This model includes methods for parsing from and dumping to YAML.
    """
    processes: List[Process] = Field(..., description="A list of processes defined in the BPMN model.")


class Sentry(BaseModel):
    id: str
    name: str
    condition: str

class PlanItem(BaseModel):
    id: str
    name: str
    type: str
    role: str
    description: str
    entryCriterion: Optional[str] = None

class Stage(BaseModel):
    id: str
    name: str
    tasks: List[PlanItem]

class Case(BaseModel):
    id: str
    name: str
    roles: List[str]
    stages: List[Stage]
    planItems: List[PlanItem]
    sentries: List[Sentry]

class CMMN(BaseModel, YAMLMixin):
    cases: List[Case]



class Input(BaseModel):
    id: str
    label: str
    inputExpression: str
    inputValues: List[str]

class Output(BaseModel):
    id: str
    label: str
    outputValues: List[str]

class Rule(BaseModel):
    inputEntries: List[str]
    outputEntries: List[str]

class DecisionTable(BaseModel):
    inputs: List[Input]
    outputs: List[Output]
    rules: List[Rule]

class Decision(BaseModel):
    id: str
    name: str
    decisionTable: DecisionTable

class DMN(BaseModel, YAMLMixin):
    definitions: dict[str, Decision]

