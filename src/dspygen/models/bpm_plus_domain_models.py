from typing import List, Optional

from pydantic import BaseModel, Field

from dspygen.utils.yaml_tools import YAMLMixin, uuid_factory


class Flow(BaseModel):
    """
    Represents a flow within a BPMN process, defining the sequence or message flow between elements.
    """
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the flow.")
    sourceRef: str = Field(..., description="The source element of the flow.")
    targetRef: str = Field(..., description="The target element the flow points to.")
    condition: str | None = Field(None, description="The condition that determines whether the flow is taken.")


class Task(BaseModel):
    """
    Represents a task within a BPMN process. A task is a unit of work within a process.
    """
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the task.")
    name: str = Field(..., description="The name of the task.")
    type: str = Field(..., description="The type of the task, e.g., 'serviceTask', 'userTask'.")
    properties: dict | None = Field(default=None,
                                       description="Additional properties of the task, defined as a dictionary.")


class Process(BaseModel):
    """
    Represents a BPMN process, which is a collection of tasks and flows that define the workflow.
    """
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the process.")
    name: str = Field(..., description="The name of the process.")
    tasks: list[Task] = Field(..., description="A list of tasks within the process.")
    flows: list[Flow] = Field(...,
                              description="A list of flows that define the sequence and message flows within the process.")


class BPMN(BaseModel, YAMLMixin):
    """
    Defines a BPMN model, which may contain one or more processes. This model includes methods for parsing from and dumping to YAML.
    """
    processes: list[Process] = Field(..., description="A list of processes defined in the BPMN model.")


class Sentry(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the sentry.")
    name: str
    condition: str


class PlanItem(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the plan item.")
    name: str
    type: str
    role: str
    description: str
    entryCriterion: str | None = None


class Stage(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the stage.")
    name: str
    tasks: list[PlanItem]


class Case(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the case.")
    name: str
    roles: list[str]
    stages: list[Stage]
    planItems: list[PlanItem]
    sentries: list[Sentry]


class CMMN(BaseModel, YAMLMixin):
    cases: list[Case]


class Input(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the input.")
    label: str
    inputExpression: str
    inputValues: list[str]


class Output(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the output.")
    label: str
    outputValues: list[str]


class Rule(BaseModel):
    inputEntries: list[str] = Field(
        ...,
        description="The conditions under which the rule applies.",
        example=["Credit Score >= 700", "Income >= 3000", "Loan Amount <= 50000"]  # Adding example directly to the field
    )
    outputEntries: list[str] = Field(
        ...,
        description="The outcomes or actions taken when conditions are met.",
        example=["Loan Approved", "Interest Rate: 3.5%", "Maximum Loan Amount: 50000"]  # Adding example directly to the field
    )


class DecisionTable(BaseModel):
    inputs: list[Input]
    outputs: list[Output]
    rules: list[Rule]


class Decision(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the decision.")
    name: str
    decisionTable: DecisionTable


class DMN(BaseModel, YAMLMixin):
    definitions: dict[str, Decision]


def main():
    """Main function"""
    # init_ol()
    from dspygen.utils.dspy_tools import init_dspy, init_ol
    init_dspy()
    print(DMN.model_json_schema())
    from dspygen.modules.prompt_to_json_module import instance
    DMN.model_validate_json()
    print(instance(DMN.model_json_schema(), ))


if __name__ == '__main__':
    main()
