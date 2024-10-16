from typing import List, Optional, Dict, Union
from pydantic import Field
from datetime import date

# Assuming DSLModel is defined in dspygen.utils.dsl_tools
from dspygen.utils.dsl_tools import DSLModel
from dspygen.utils.dspy_tools import init_versatile, init_instant


class BusinessRequirements(DSLModel):
    """Describes the business requirements for the project."""
    key_features: List[str] = Field(..., description="Key features required by the business.")
    target_audience: str = Field(..., description="Primary audience for the business requirements.")
    success_metrics: List[str] = Field(..., description="Metrics to measure the success of business requirements.")


class Development(DSLModel):
    """Describes development setup, guidelines, and review processes."""
    setup_steps: List[str] = Field(..., description="Steps to set up the development environments.")
    build_command: Optional[str] = Field(None, description="Command to build the project.")
    test_command: Optional[str] = Field(None, description="Command to run tests.")
    guidelines: Optional[List[str]] = Field(None, description="Guidelines to follow during development.")
    review_process: Optional[List[str]] = Field(None, description="Process for reviewing the development work.")


class Deployment(DSLModel):
    """Represents deployment configurations, platforms, and environments."""
    platform: str = Field(..., description="Deployment platform used.")
    cicd_pipeline: Optional[str] = Field(None, description="CI/CD pipeline configuration.")
    staging_environment: Optional[str] = Field(None, description="Staging environments setup.")
    production_environment: Optional[str] = Field(None, description="Production environments setup.")
    review_cycle: Optional[str] = Field(None, description="Frequency of deployment reviews.")


class Interaction(DSLModel):
    """Defines an interaction between roles, specifying the type and involved roles."""
    interaction_type: str = Field(..., description="Type of interaction between roles.")
    with_role: str = Field(..., alias='with', description="Role with which the interaction occurs.")
    description: Optional[str] = Field(None, description="Description of the interaction.")
    notifications: Optional[List[str]] = Field(None, description="Notifications triggered by the interaction.")


class Subtask(DSLModel):
    """Represents a subtask within a larger task, including its dependencies and interactions."""
    subtask_id: str = Field(..., description="Unique identifier for the subtask.")
    name: str = Field(..., description="Name of the subtask.")
    assigned_to: List[str] = Field(..., description="Roles assigned to the subtask.")
    dependencies: Optional[List[str]] = Field(None, description="List of task IDs that this subtask depends on.")
    estimated_time: Optional[str] = Field(None, description="Estimated time to complete the subtask.")
    interactions: Optional[List[Interaction]] = Field(None, description="Interactions involved in the subtask.")
    status: Optional[str] = Field(None, description="Current status of the subtask.")
    start_date: Optional[date] = Field(None, description="Start date of the subtask.")
    end_date: Optional[date] = Field(None, description="End date of the subtask.")


class Task(DSLModel):
    """Represents a task, including its description, dependencies, and subtasks."""
    task_id: str = Field(..., description="Unique identifier for the task.")
    name: str = Field(..., description="Name of the task.")
    description: Optional[str] = Field(None, description="Detailed description of the task.")
    assigned_to: List[str] = Field(..., description="Roles assigned to the task.")
    dependencies: Optional[List[str]] = Field(None, description="List of task IDs that this task depends on.")
    interactions: Optional[List[Interaction]] = Field(None, description="Interactions involved in the task.")
    subtasks: Optional[List[Subtask]] = Field(None, description="List of subtasks under this task.")
    estimated_time: Optional[str] = Field(None, description="Estimated time to complete the task.")
    priority: Optional[str] = Field(None, description="Priority level of the task.")
    status: Optional[str] = Field(None, description="Current status of the task.")
    start_date: Optional[date] = Field(None, description="Start date of the task.")
    end_date: Optional[date] = Field(None, description="End date of the task.")
    results: Optional[List[str]] = Field(None, description="Results or outputs from the task.")
    scheduled_date: Optional[date] = Field(None, description="Scheduled date for the task.")


class Workflow(DSLModel):
    """Defines the workflow for the project, organizing tasks in a specific order."""
    workflow_type: str = Field(..., description="Type of workflow (Sequential or Parallel).")
    tasks: List[str] = Field(..., description="List of task IDs in the workflow order.")


class Role(DSLModel):
    """Represents a role in the project, with its responsibilities and type."""
    name: str = Field(..., description="Name of the role.")
    role_type: str = Field(..., description="Type of the role (Human or AI).")
    description: Optional[str] = Field(None, description="Description of the role.")
    responsibilities: Optional[List[str]] = Field(None, description="List of responsibilities for the role.")
    abbreviation: Optional[str] = Field(None, description="Abbreviation for the role.")


class Project(DSLModel):
    """Represents a project, its roles, tasks, and overall workflow."""
    name: str = Field(..., description="Name of the project.")
    description: Optional[str] = Field(None, description="Description of the project.")
    timeframe: Optional[Dict[str, date]] = Field(None, description="Start and end dates of the project.")
    roles: List[Role] = Field(..., description="List of roles involved in the project.")
    tasks: List[Task] = Field(..., description="List of tasks within the project.")
    workflow: Optional[Workflow] = Field(None, description="Workflow structure of the project.")


class Amendment(DSLModel):
    """Represents an amendment made during a meeting, including the vote required to pass it."""
    amendment_id: str = Field(..., description="Unique identifier for the amendment.")
    description: str = Field(..., description="Description of the amendment.")
    made_by: str = Field(..., description="Participant who made the amendment.")
    seconded_by: Optional[str] = Field(None, description="Participant who seconded the amendment.")
    debate_allowed: bool = Field(..., description="Indicates if debate is allowed on the amendment.")
    vote_required: str = Field(..., description="Type of vote required to pass the amendment.")
    debate: Optional[Dict[str, Union[List[str], List[str]]]] = Field(None, description="Details of the debate if allowed.")


class Participant(DSLModel):
    """Represents a participant in a meeting."""
    name: str = Field(..., description="Name of the participant.")
    role: str = Field(..., description="Role of the participant.")


class Meeting(DSLModel):
    """Represents a meeting, its participants, agenda, and other details."""
    name: str = Field(..., description="Name of the meeting.")
    meeting_date: date = Field(..., description="Date of the meeting.")
    location: Optional[str] = Field(None, description="Location where the meeting is held.")
    chairperson: str = Field(..., description="Chairperson of the meeting.")
    secretary: str = Field(..., description="Secretary responsible for taking minutes.")
    participants: List[Participant] = Field(..., description="List of all participants in the meeting.")
    agenda: List[str] = Field(..., description="Agenda items for the meeting.")
    minutes: Optional[Dict[str, Union[str, bool, date]]] = Field(None, description="Minutes of the meeting.")
    rules_of_order: Optional[Dict[str, Union[str, List[str]]]] = Field(None, description="Rules governing the meeting.")


def main():
    """Main function"""
    init_instant()

    from sungen.dspy_modules.gen_pydantic_instance import GenPydanticInstance
    instance = GenPydanticInstance(Meeting)("Fortune 10 Board Meeting. Example values for empty fields")
    print(instance)


if __name__ == '__main__':
    main()
