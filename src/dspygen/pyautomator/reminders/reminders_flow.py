import json
from prefect import flow, task
from datetime import datetime, timedelta
from dspygen.pyautomator.reminders.reminder_app import RemindersApp
from dspygen.modules.reminder_motivation_module import reminder_motivation_call
from dspygen.utils.dspy_tools import init_dspy

@task
def get_pending_reminders(app: RemindersApp):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    query = f"SELECT * FROM df WHERE DueDate >= '{today}' AND DueDate < '{tomorrow}' AND Completed = 0 ORDER BY DueDate"
    reminders = app.query(query)
    
    task_list = [
        {"title": r.title, "due_time": r.due_date.strftime('%I:%M %p') if r.due_date else 'No due time'}
        for r in reminders
    ]
    
    return len(reminders), json.dumps(task_list)

@task
def create_reminder_with_motivation(app: RemindersApp, list_name: str, num_tasks: int, task_list_json: str):
    init_dspy()
    current_time = datetime.now()
    next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    # Generate motivational advice
    motivation = reminder_motivation_call(num_tasks=num_tasks, task_list=task_list_json)

    prompt = (f"Create a reminder for the next hour at {next_hour.strftime('%Y-%m-%d %H:%M:%S')} called "
              f"'Motivation for (next hour)' and replace (next hour) with the time. Notes: {motivation}")

    new_reminder = app.create_reminder_from_generated(prompt, list_name)
    print(f"Created new reminder: {new_reminder}")

@flow(log_prints=True)
def hourly_reminder_flow():
    app = RemindersApp()
    app.request_access()
    
    list_name = app.get_all_lists()[0]  # Use the first available list
    print(f"Using reminder list: {list_name}")
    
    num_tasks, task_list_json = get_pending_reminders(app)
    print(f"Number of pending tasks: {num_tasks}")
    
    create_reminder_with_motivation(app, list_name, num_tasks, task_list_json)

if __name__ == "__main__":
    hourly_reminder_flow.serve(
        name="hourly-reminders-deployment",
        tags=["reminders", "motivation"],
        interval=3600  # Run every 3600 seconds (1 hour)
    )
    # hourly_reminder_flow()
