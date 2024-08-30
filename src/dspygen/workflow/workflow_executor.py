import copy
from typing import Optional, Dict, Any
from sungen.typetemp.functional import render, render_native
from dspygen.workflow.workflow_models import Workflow, Action, Job, DateTrigger, CronTrigger
from loguru import logger
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger as APSchedulerCronTrigger
from apscheduler.triggers.date import DateTrigger as APSchedulerDateTrigger
from datetime import datetime
import pytz
import sys

# Configure logger with timestamp and log level
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)
logger.add(
    "workflow_executor.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="1 MB"
)

def initialize_context(init_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Initializes the workflow context."""
    logger.debug(f"Initializing context with: {init_ctx}")
    return copy.deepcopy(init_ctx) if init_ctx else {}


def update_context(context: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Updates the workflow context with new values."""
    # logger.debug(f"Updating context. Current: {context}, Updates: {updates}")
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
    # logger.debug(f"Updated context: {rendered_context}")
    return rendered_context


def evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    """Evaluates a condition within the current context."""
    logger.debug(f"Evaluating condition: '{condition}' with context: {context}")
    try:
        safe_context = copy.deepcopy(context)
        result = eval(condition, {}, safe_context)
        logger.debug(f"Condition result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error evaluating condition '{condition}': {e}")
        return False


def execute_job(job: Job, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executes all actions within a job."""
    logger.info(f"Executing job: {job.name}")
    job_context = update_context(context, {})  # Isolate context for the job

    for action in job.steps:
        logger.info(f"Executing action: {action.name}")
        try:
            job_context = execute_action(action, job_context)  # Execute each action
            logger.info(f"Finished executing action: {action.name}")
        except Exception as e:
            logger.error(f"Error executing action {action.name}: {str(e)}")

    logger.debug(f"Job {job.name} completed. Updated context: {job_context}")
    return job_context


def execute_action(action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
    """Executes a single action, updating the context accordingly."""
    logger.info(f"Executing action: {action.name}")

    # Check for conditional execution
    if action.cond and not evaluate_condition(action.cond.expr, context):
        logger.info(f"Condition for action '{action.name}' not met, skipping.")
        return context  # Skip the action if condition not met

    action_context = update_context(context, {})  # Isolate context for the action

    if action.code:
        logger.debug(f"Executing code for action '{action.name}'")
        rendered_code = render(action.code, **action_context)
        logger.debug(f"Rendered code: {rendered_code}")
        try:
            exec(rendered_code, action_context, action_context)
            logger.info(f"Code execution for action '{action.name}' completed successfully")
        except Exception as e:
            logger.error(f"Error executing code for action '{action.name}': {str(e)}")
        context = update_context(context, action_context)  # Update global context with changes

    logger.debug(f"Action '{action.name}' completed. Updated context: {context}")
    return context


def execute_workflow(workflow: Workflow, init_ctx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executes all jobs defined in a workflow."""
    logger.info(f"Executing workflow: {workflow.name}")
    global_context = initialize_context(init_ctx)  # Initialize global context

    workflow.process_imports()
    workflow.topological_sort()

    for job in workflow.jobs:
        logger.info(f"Starting execution of job: {job.name}")
        try:
            global_context = execute_job(job, global_context)  # Execute each job
            logger.info(f"Finished execution of job: {job.name}")
        except Exception as e:
            logger.error(f"Error executing job {job.name}: {str(e)}")

    if '__builtins__' in global_context:
        del global_context['__builtins__']  # Remove builtins from context

    logger.info(f"Workflow '{workflow.name}' completed. Final context: {global_context}")
    return global_context


def schedule_workflow(workflow: Workflow, scheduler: BaseScheduler):
    """Schedules a workflow using the provided scheduler."""
    logger.info(f"Scheduling workflow: {workflow.name}")
    for trigger in workflow.triggers:
        if isinstance(trigger, CronTrigger):
            logger.debug(f"Adding cron job for trigger: {trigger.cron}")
            job = scheduler.add_job(
                execute_workflow,
                APSchedulerCronTrigger.from_crontab(trigger.cron, timezone=pytz.UTC),
                args=[workflow],
                timezone=pytz.UTC
            )
            logger.debug(f"Job added: {str(job)}")
        elif isinstance(trigger, DateTrigger):
            logger.debug(f"Adding date job for trigger: {trigger.run_date}")
            run_date = trigger.run_date if trigger.run_date != "now" else datetime.now(pytz.UTC)
            job = scheduler.add_job(
                execute_workflow,
                APSchedulerDateTrigger(run_date=run_date, timezone=pytz.UTC),
                args=[workflow],
                timezone=pytz.UTC
            )
            logger.debug(f"Job added: {str(job)}")
        else:
            logger.error(f"Unknown trigger type: {type(trigger)}")

    logger.info(f"Workflow '{workflow.name}' scheduled successfully")
    logger.debug(f"All jobs: {scheduler.get_jobs()}")
    return scheduler


if __name__ == "__main__":
    from apscheduler.schedulers.background import BackgroundScheduler
    
    workflow = Workflow.from_yaml("path/to/your/workflow.yaml")
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    schedule_workflow(workflow, scheduler)

    try:
        # Keep the script running
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

