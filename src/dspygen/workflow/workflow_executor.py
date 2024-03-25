import copy
from typing import Optional, Dict, Any

from dspygen.typetemp.functional import render, render_native
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

    if '__builtins__' in new_context:
        del new_context['__builtins__']  # Remove builtins from context

    rendered_context = {}
    for arg, value in new_context.items():
        if "{{" in str(value):
            # Render the string value with Jinja2
            rendered_context[arg] = render(value, **new_context)

            # Convert the rendered string to a native Python type
            try:
                rendered_context[arg] = eval(rendered_context[arg])
            except Exception as e:
                logger.error(f"Error converting rendered value to native Python type: {e}")
        else:
            # Non-string values are added to the context unchanged
            rendered_context[arg] = value
    return rendered_context


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
        rendered_code = render(action.code, **action_context)
        # Execute action's code, allowing it to modify the action-specific context
        exec(rendered_code, action_context, action_context)
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

    if '__builtins__' in global_context:
        del global_context['__builtins__']  # Remove builtins from context

    return global_context
