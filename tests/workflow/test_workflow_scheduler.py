import pytest
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dspygen.workflow.workflow_models import Workflow, Job, Action, CronTrigger
from dspygen.workflow.workflow_executor import schedule_workflow
import pytz
import io
import sys
from unittest.mock import patch

class MockClock:
    def __init__(self, initial):
        self.current = initial.replace(tzinfo=pytz.UTC)

    def get_current_time(self):
        return self.current

    def advance(self, delta):
        self.current += delta

@pytest.fixture
def mock_clock():
    return MockClock(datetime(2023, 1, 1, 0, 0, 0))

@pytest.fixture
def scheduler(mock_clock):
    scheduler = BackgroundScheduler()
    scheduler.configure(clock=mock_clock.get_current_time)
    return scheduler

@pytest.fixture
def captured_output():
    output = io.StringIO()
    with patch('sys.stdout', new=output):
        yield output

def test_cron_trigger_simulation(scheduler, mock_clock, captured_output):
    workflow = Workflow(
        name="TestWorkflow",
        triggers=[CronTrigger(cron="*/5 * * * *")],  # Every 5 minutes
        jobs=[
            Job(
                name="TestJob",
                runner="python",
                steps=[Action(name="TestAction", code="print('Job executed')")]
            )
        ]
    )

    schedule_workflow(workflow, scheduler)
    scheduler.start()

    execution_times = []

    # Simulate 1 hour passing
    for _ in range(12):  # 12 * 5 minutes = 1 hour
        mock_clock.advance(timedelta(minutes=5))
        scheduler.wakeup()
        jobs = scheduler.get_jobs()
        for job in jobs:
            next_run_time = job.trigger.get_next_fire_time(None, mock_clock.current)
            if next_run_time and next_run_time <= mock_clock.current:
                execution_times.append(mock_clock.current)
                job.func(*job.args, **job.kwargs)

    scheduler.shutdown()

    # Assert that the job was executed 12 times (every 5 minutes for 1 hour)
    assert len(execution_times) == 12
    
    # Check that executions happened at 5-minute intervals
    for i in range(1, len(execution_times)):
        assert execution_times[i] - execution_times[i-1] == timedelta(minutes=5)

def test_daily_trigger_simulation(scheduler, mock_clock, captured_output):
    workflow = Workflow(
        name="DailyWorkflow",
        triggers=[CronTrigger(cron="0 12 * * *")],  # Every day at noon
        jobs=[
            Job(
                name="DailyJob",
                runner="python",
                steps=[Action(name="DailyAction", code="print('Daily job executed')")]
            )
        ]
    )

    schedule_workflow(workflow, scheduler)
    scheduler.start()

    execution_times = []

    # Simulate 5 days passing
    for day in range(5):
        # Calculate time to next noon
        current_time = mock_clock.current
        next_noon = current_time.replace(hour=12, minute=0, second=0, microsecond=0)
        if current_time >= next_noon:
            next_noon += timedelta(days=1)
        time_to_advance = next_noon - current_time

        # Advance to next noon
        mock_clock.advance(time_to_advance)
        scheduler.wakeup()

        jobs = scheduler.get_jobs()
        for job in jobs:
            next_run_time = job.trigger.get_next_fire_time(None, mock_clock.current)
            if next_run_time and next_run_time <= mock_clock.current:
                execution_times.append(mock_clock.current)
                job.func(*job.args, **job.kwargs)

    scheduler.shutdown()

    # Assert that the job was executed 5 times (once per day for 5 days)
    assert len(execution_times) == 5, f"Expected 5 executions, but got {len(execution_times)}"
    
    # Check that executions happened at daily intervals at noon
    for i, execution_time in enumerate(execution_times):
        assert execution_time.hour == 12, f"Execution {i} not at noon: {execution_time}"
        assert execution_time.minute == 0, f"Execution {i} not at the start of the hour: {execution_time}"
        if i > 0:
            time_diff = execution_time - execution_times[i-1]
            assert time_diff == timedelta(days=1), f"Incorrect interval between executions {i-1} and {i}: {time_diff}"

def test_multiple_triggers(scheduler, mock_clock, captured_output):
    workflow = Workflow(
        name="MultiTriggerWorkflow",
        triggers=[
            CronTrigger(cron="0 */2 * * *"),  # Every 2 hours
            CronTrigger(cron="30 * * * *"),   # Every hour at 30 minutes past
        ],
        jobs=[
            Job(
                name="MultiTriggerJob",
                runner="python",
                steps=[Action(name="MultiTriggerAction", code="print('Multi-trigger job executed')")]
            )
        ]
    )

    schedule_workflow(workflow, scheduler)
    scheduler.start()

    execution_times = []

    # Simulate 24 hours passing
    for hour in range(24):
        # Advance to the next hour
        mock_clock.advance(timedelta(hours=1))
        current_time = mock_clock.current
        print(f"Current time: {current_time}")

        # Check for job execution at the start of every even hour
        if current_time.hour % 2 == 0 and current_time.minute == 0:
            scheduler.wakeup()
            jobs = scheduler.get_jobs()
            for job in jobs:
                next_run_time = job.trigger.get_next_fire_time(None, current_time)
                if next_run_time and next_run_time <= current_time:
                    execution_times.append(current_time)
                    job.func(*job.args, **job.kwargs)
                    print(f"Job executed at {current_time}")

        # Advance 30 minutes within the same hour
        mock_clock.advance(timedelta(minutes=30))
        current_time = mock_clock.current
        print(f"Current time: {current_time}")

        # Check for job execution at 30 minutes past every hour
        scheduler.wakeup()
        jobs = scheduler.get_jobs()
        for job in jobs:
            next_run_time = job.trigger.get_next_fire_time(None, current_time)
            if next_run_time and next_run_time <= current_time:
                execution_times.append(current_time)
                job.func(*job.args, **job.kwargs)
                print(f"Job executed at {current_time}")

    scheduler.shutdown()

    # Assert that the job was executed 24 times (12 times for every 2 hours + 12 times for every hour at 30 minutes past)
    assert len(execution_times) == 24, f"Expected 24 executions, but got {len(execution_times)}"

    # Check that executions happened at correct intervals
    for time in execution_times:
        assert time.minute in [0, 30], f"Execution at incorrect minute: {time}"

    # Print all execution times for debugging
    print("Execution times:")
    for time in execution_times:
        print(time)

def test_weekly_trigger(scheduler, mock_clock, captured_output):
    workflow = Workflow(
        name="WeeklyWorkflow",
        triggers=[CronTrigger(cron="0 9 * * 1")],  # Every Monday at 9 AM
        jobs=[
            Job(
                name="WeeklyJob",
                runner="python",
                steps=[Action(name="WeeklyAction", code="print('Weekly job executed')")]
            )
        ]
    )

    schedule_workflow(workflow, scheduler)
    scheduler.start()

    execution_times = []

    # Simulate 4 weeks passing
    for week in range(4):
        print(f"\nSimulating week {week + 1}")
        # Advance to next Monday at 9 AM
        while mock_clock.current.weekday() != 0 or mock_clock.current.hour != 9:
            mock_clock.advance(timedelta(hours=1))
        
        print(f"Current time: {mock_clock.current}")
        scheduler.wakeup()
        jobs = scheduler.get_jobs()
        print(f"Number of jobs: {len(jobs)}")
        for job in jobs:
            print(f"Job: {job.name}, Next run time: {job.next_run_time}")
            if job.next_run_time and job.next_run_time <= mock_clock.current:
                execution_times.append(mock_clock.current)
                job.func(*job.args, **job.kwargs)
                output = captured_output.getvalue()
                if "Weekly job executed" in output:
                    print(f"Job executed at {mock_clock.current}")
                captured_output.truncate(0)
                captured_output.seek(0)
        
        # Advance to next day to avoid re-triggering
        mock_clock.advance(timedelta(days=1))

    scheduler.shutdown()

    print(f"\nTotal executions: {len(execution_times)}")
    print("Execution times:")
    for time in execution_times:
        print(time)

    # Assert that the job was executed 4 times (once per week for 4 weeks)
    assert len(execution_times) == 4, f"Expected 4 executions, but got {len(execution_times)}"

    # Check that executions happened on Mondays at 9 AM
    for time in execution_times:
        assert time.weekday() == 0, f"Execution not on Monday: {time}"
        assert time.hour == 9, f"Execution not at 9 AM: {time}"
        assert time.minute == 0, f"Execution not at the start of the hour: {time}"

def test_multiple_jobs(scheduler, mock_clock, captured_output):
    workflow = Workflow(
        name="MultiJobWorkflow",
        triggers=[CronTrigger(cron="0 * * * *")],  # Every hour
        jobs=[
            Job(
                name="Job1",
                runner="python",
                steps=[Action(name="Action1", code="print('Job 1 executed')")]
            ),
            Job(
                name="Job2",
                runner="python",
                steps=[Action(name="Action2", code="print('Job 2 executed')")]
            )
        ]
    )

    schedule_workflow(workflow, scheduler)
    scheduler.start()

    job1_executions = []
    job2_executions = []

    # Simulate 24 hours passing
    for hour in range(24):
        mock_clock.advance(timedelta(hours=1))
        print(f"Current time: {mock_clock.current}")
        scheduler.wakeup()
        jobs = scheduler.get_jobs()
        for job in jobs:
            next_run_time = job.trigger.get_next_fire_time(None, mock_clock.current)
            if next_run_time and next_run_time <= mock_clock.current:
                if job.name == "execute_workflow":  # The actual job name
                    job.func(*job.args, **job.kwargs)
                    output = captured_output.getvalue()
                    if "Job 1 executed" in output:
                        job1_executions.append(mock_clock.current)
                        print("Job 1 executed")
                    if "Job 2 executed" in output:
                        job2_executions.append(mock_clock.current)
                        print("Job 2 executed")
                    captured_output.truncate(0)
                    captured_output.seek(0)

    scheduler.shutdown()

    # Print captured output for debugging
    print("Captured output:")
    print(captured_output.getvalue())

    # Assert that both jobs were executed 24 times each
    assert len(job1_executions) == 24, f"Job1 executed {len(job1_executions)} times instead of 24"
    assert len(job2_executions) == 24, f"Job2 executed {len(job2_executions)} times instead of 24"

    # Check that executions happened at hourly intervals
    for i in range(1, len(job1_executions)):
        assert job1_executions[i] - job1_executions[i-1] == timedelta(hours=1)
        assert job2_executions[i] - job2_executions[i-1] == timedelta(hours=1)

    # Print execution times for debugging
    print("\nJob 1 execution times:")
    for time in job1_executions:
        print(time)
    print("\nJob 2 execution times:")
    for time in job2_executions:
        print(time)
