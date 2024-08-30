"""
Module for generating motivational advice for completing daily reminders.
"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class GenerateReminderMotivation(dspy.Signature):
    """
    Generate motivational advice for completing daily reminders.
    Creates concise, encouraging messages that are:
    - Specific: Directly related to the tasks at hand.
    - Measurable: Tied to task completion.
    - Achievable: Realistic within the given timeframe.
    - Relevant: Pertinent to the user's day.
    - Time-bound: Clear deadlines with AM/PM times.

    Example outputs:
    - "Finish the report by 2 PM – you've tackled similar tasks quickly!"
    - "Call the client at 3:30 PM – a quick win that moves things forward!"
    - "Gym at 6 PM – a boost for the rest of your week!"
    """
    num_tasks = dspy.InputField(desc="Number of remaining tasks for the day.")
    task_list = dspy.InputField(desc="List of task titles and due times in JSON format, e.g., "
                                     "[{'title': 'Complete project report', 'due_time': '2 PM'}, ...].")
    motivation = dspy.OutputField(desc="Compact motivational message to help with task completion. "
                                       "Focuses on reducing cognitive load while providing SMART tips.")


class ReminderMotivationModule(dspy.Module):
    """ReminderMotivationModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, num_tasks, task_list):
        pred = dspy.Predict(GenerateReminderMotivation)
        self.output = pred(num_tasks=num_tasks, task_list=task_list).motivation
        return self.output

def reminder_motivation_call(num_tasks: int, task_list: str):
    motivation = ReminderMotivationModule()
    return motivation.forward(num_tasks=num_tasks, task_list=task_list)

def main():
    init_dspy()
    num_tasks = 3
    task_list = "1. Complete project report (Due: 14:00)\n2. Call client (Due: 15:30)\n3. Gym session (Due: 18:00)"
    result = reminder_motivation_call(num_tasks=num_tasks, task_list=task_list)
    print(result)

if __name__ == "__main__":
    main()