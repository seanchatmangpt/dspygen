from textwrap import dedent

import dspy
from dspygen.utils.date_tools import TODAY, TOMORROW_MORNING_8AM, SATURDAY, SUNDAY, SATURDAY_STR, SUNDAY_STR
import datetime


# Import or define the GenerateICalendarEvent class
class GenerateICalendarEvent(dspy.Signature):
    """
    Generate a perfect iCalendar VEVENT with precise start and end times, along with accurate summary, description, and location details.
    """
    today = dspy.InputField(desc="Current date in YYYYMMDD format.")
    tomorrow_morning = dspy.InputField(desc="8 AM on the day following the current date.")
    this_saturday = dspy.InputField(desc="Date of the upcoming Saturday.")
    this_sunday = dspy.InputField(desc="Date of the upcoming Sunday.")
    prod_id = dspy.InputField(desc="Product ID of the calendar.")
    prompt = dspy.InputField(desc="User's input regarding the event details.")

    icalendar_vevent = dspy.OutputField(
        desc=(
            "Generated iCalendar VEVENT with precise times and details. The VEVENT is crafted carefully "
            "to ensure that the start and end times are accurate, and the summary, description, and location "
            "are filled in based on the provided context."
        ),
        prefix=dedent(
            """\
            ICalendar Assistant: I turned the input into the perfect iCalendar VEVENT. I paid close attention to the start and end times.
            ```vevent
            """
        )
    )


class GenerateICalendarModule(dspy.Module):
    """GenerateICalendarModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, today, tomorrow_morning, this_saturday, this_sunday, prod_id, prompt):
        # Using the GenerateICalendarEvent class in the prediction
        pred = dspy.Predict(GenerateICalendarEvent)
        self.output = pred(today=today, tomorrow_morning=tomorrow_morning, this_saturday=this_saturday,
                           this_sunday=this_sunday, prod_id=prod_id, prompt=prompt).icalendar_vevent
        self.output = self.output.replace("```vevent", "").replace("```", "")
        return self.output.strip()


def generate_i_calendar_call(prompt, prod_id="-//dspygen//CalendarEvent//EN"):
    generate_i_calendar = GenerateICalendarModule()
    return generate_i_calendar.forward(
        today=TODAY.strftime("%Y%m%d"),
        tomorrow_morning=TOMORROW_MORNING_8AM.strftime("%Y-%m-%d %H:%M:%S"),
        this_saturday=SATURDAY_STR,
        this_sunday=SUNDAY_STR,
        prod_id=prod_id,
        prompt=prompt
    )


def main():
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy()  # Ensure dspy is initialized

    # Enhanced test prompt
    test_prompt = (
        "Schedule a team meeting titled 'Quarterly Project Review' for next Saturday at 2 PM for 1.5 hours. "
        "The topic is 'Project Review and Planning'. Location: Conference Room A. "
        "Attendees: Alice Smith (alice@example.com), Bob Johnson (bob@example.com), Charlie Brown (charlie@example.com). "
        "Organizer: David Miller (david@example.com). "
        "Please add a reminder 15 minutes before the event."
    )

    result = generate_i_calendar_call(test_prompt)
    print(result)


if __name__ == "__main__":
    main()
