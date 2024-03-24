import copy
from typing import Optional, Dict, Any
from dspygen.workflow.workflow_models import Workflow, Action, Job
from loguru import logger


def initialize_context(init_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Initializes the workflow context."""
    return copy.deepcopy(init_ctx) if init_ctx else {}


def update_context(context: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Updates the workflow context with new values."""
    # Create a copy of context with only python primitives
    new_context = {k: v for k, v in context.items() if isinstance(v, (int, float, str, bool, list, dict))}

    new_context = copy.deepcopy(new_context)

    new_context.update(updates)

    return new_context


def evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    """Evaluates a condition within the current context."""
    try:
        safe_context = copy.deepcopy(context)
        return eval(condition, {}, safe_context)
    except Exception as e:
        logger.error(f"Error evaluating condition '{condition}': {e}")
        return False


def execute_job(job: Job, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executes all actions within a job."""
    logger.info(f"Executing job: {job.name}")
    job_context = update_context(context, {})  # Isolate context for the job

    for action in job.steps:
        job_context = execute_action(action, job_context)  # Execute each action

    return job_context


def execute_action(action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executes a single action, updating the context accordingly."""
    logger.info(f"Executing action: {action.name}")

    # Check for conditional execution
    if action.cond and not evaluate_condition(action.cond.expr, context):
        logger.info(f"Condition for action '{action.name}' not met, skipping.")
        return context  # Skip the action if condition not met

    action_context = update_context(context, {})# Isolate context for the action

    if action.code:
        # Execute action's code, allowing it to modify the action-specific context
        exec(action.code, action_context, action_context)
        context = update_context(context, action_context)  # Update global context with changes

    return context


def execute_workflow(workflow: Workflow, init_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executes all jobs defined in a workflow."""
    logger.info(f"Executing workflow: {workflow.name}")
    global_context = initialize_context(init_ctx)  # Initialize global context

    workflow.process_imports()
    workflow.topological_sort()

    for job in workflow.jobs:
        global_context = execute_job(job, global_context)  # Execute each job

    del global_context['__builtins__']  # Remove builtins from context

    return global_context
