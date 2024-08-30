import pytest
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dspygen.workflow.workflow_models import Workflow, Job, Action, CronTrigger
from dspygen.workflow.workflow_executor import schedule_workflow
import pytz

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

def test_cron_trigger_simulation(scheduler, mock_clock):
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

def test_daily_trigger_simulation(scheduler, mock_clock):
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
