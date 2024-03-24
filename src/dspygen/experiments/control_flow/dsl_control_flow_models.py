import json
from typing import List, Union, Dict, Any, Optional
from pydantic import BaseModel, validator, Field

from dspygen.utils.yaml_tools import YAMLMixin


class Condition(BaseModel):
    expr: str = Field(..., description="Expression to evaluate the condition.")


class Loop(BaseModel):
    over: str = Field(..., description="Iterable expression.")
    var: str = Field(..., description="Variable name for current item.")


class Action(BaseModel):
    name: str
    use: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
    code: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    cond: Optional[Condition] = Field(None)
    loop: Optional[Loop] = None


class Job(BaseModel):
    name: str
    depends: Optional[List[str]] = None
    runner: str
    steps: List[Action]
    env: Optional[Dict[str, str]] = None


class Workflow(BaseModel, YAMLMixin):
    name: str
    triggers: Union[str, List[str]]
    jobs: List[Job]


def evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    """
    Evaluates a condition expression against the given context.
    """
    try:
        return eval(condition, {}, context)
    except Exception as e:
        print(f"Error evaluating condition '{condition}': {e}")
        return False


def execute_action(action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a single action based on its type (use or code) and updates the context.
    """
    new_context = context.copy()
    if action.cond and not evaluate_condition(action.cond.expr, context):
        print(f"Skipping action {action.name} due to condition")
        return new_context

    if action.use:
        print(f"Executing module {action.use} with args {action.args}")
    elif action.code:
        # Prepare an isolated yet shared execution environment
        local_context = {}
        global_context = context
        exec(action.code, global_context, local_context)

        # Merge local changes back into the global context
        context.update(local_context)

    return context


def execute_loop(loop: Loop, actions: List[Action], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Iterates over a loop, executing contained actions for each item.
    """
    items = eval(loop.over, {}, context)
    for item in items:
        loop_context = context.copy()
        loop_context[loop.var] = item
        for action in actions:
            # Ensure loop_context is updated with each action's changes
            loop_context = execute_action(action, loop_context)
    return loop_context


def execute_job(job: Job, global_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes all actions in a job, respecting conditions and loops.
    """
    job_context = {**global_context, **(job.env or {})}
    for action in job.steps:
        if action.loop:
            job_context = execute_loop(action.loop, [action], job_context)
        else:
            job_context = execute_action(action, job_context)
    return job_context


def execute_workflow(workflow: Workflow, init_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Orchestrates the execution of all jobs in a workflow.
    """
    global_context = init_ctx
    for job in workflow.jobs:
        # In a real scenario, respect job.depends for execution order
        global_context = execute_job(job, global_context)
    print("Workflow execution completed.")
    return global_context


def serialize_context(context):
    serialized_context = {}
    for key, value in context.items():
        try:
            json.dumps(value)  # Test if value is serializable
            serialized_context[key] = value
        except (TypeError, ValueError):
            serialized_context[key] = str(value)  # Convert non-serializable types to string
    return serialized_context


def main():
    wf = Workflow.from_yaml("control_flow_workflow.yaml")
    execute_workflow(wf)
    wf.to_yaml("control_flow_workflow_output_new.yaml")


if __name__ == '__main__':
    main()
