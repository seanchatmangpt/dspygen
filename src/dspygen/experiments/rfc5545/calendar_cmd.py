from textwrap import dedent

import typer
from datetime import datetime
from dateutil import parser
from dataclasses import dataclass
from typing import Optional

from dspygen.experiments.rfc5545.ical_models import Event
from dspygen.utils.date_tools import TODAY, TOMORROW_MORNING_8AM, SATURDAY, SUNDAY, MONDAY_8AM, MONDAY_9AM

app = typer.Typer(help="Advanced Calendar Assistant")

@dataclass
class VEvent:
    dtstart: datetime = None
    dtend: Optional[datetime] = None
    duration: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    def __str__(self):
        dtstart_str = self.dtstart.strftime("%I:%M%p on %A, %B %d, %Y")
        dtend_str = (
            self.dtend.strftime("%I:%M%p on %A, %B %d, %Y") if self.dtend else ""
        )
        return (
            f"Summary:\t{self.summary}\n"
            f"Start:\t\t{dtstart_str}\n"
            f"End:\t\t{dtend_str}\n"
            f"Description:\t{self.description}\n"
            f"Location:\t{self.location}"
        )

    def to_event_kwargs(self):
        return {
            "dtstart": str(self.dtstart),
            "dtend": str(self.dtend) if self.dtend else None,
            "duration": self.duration,
            "summary": self.summary,
            "description": self.description,
            "location": self.location,
        }

def get_vevent(prompt: str) -> VEvent:
    assistant_prompt = dedent(
        f"""You are a ICalendar Assistant.
You are very careful to make sure the start and end times are perfect.
Pay close attention to the start and end times. The user may not provide clear information.
Do your best to extract the start and end times.



Today is {TODAY}.
Tomorrow morning is {TOMORROW_MORNING_8AM}.
This Saturday is {SATURDAY} (Default to this Saturday).
This Sunday is {SUNDAY} (Default to this Sunday). 


ICalendar Assistant: How can I assist you today?

User: {prompt}. Please make sure the start and end times are correct. Remember, this Saturday is {SATURDAY} and this Sunday is {SUNDAY}.

ICalendar Assistant: I will turn that into the perfect icalendar VEVENT. I will pay close attention to the
start and end times. I will also make sure the summary, description, and location are correct. You are creative
and can use your imagination to fill in the gaps. You gave me the following information: {prompt}

```vevent
BEGIN:VEVENT
DTSTAMP:{TODAY}
SUMMARY:Morning meeting
DESCRIPTION:Mandatory morning meeting with the team
DTSTART:{MONDAY_8AM}
DTEND:{MONDAY_9AM}
LOCATION:Main conference room
END:VEVENT
```

ICalendar Assistant: Please confirm the details are correct. I made sure to follow your instructions to the letter.

User: {prompt}. Please make sure the start and end times are correct. 

ICalendar Assistant: I turned {prompt} into the perfect icalendar VEVENT. I paid close attention.

```vevent
BEGIN:VEVENT
DTSTAMP:{TODAY}"""
    )

    vevent = ""

    kwargs = {
        line.split(":")[0].lower(): line.split(":")[1]
        for line in vevent.split("\n")
        if line != "END:VEVENT"
    }

    kwargs["dtstart"] = parser.parse(kwargs["dtstart"])
    kwargs["dtend"] = parser.parse(kwargs["dtend"]) if kwargs["dtend"] else None

    event = VEvent(**kwargs)
    return event

def create_event_logic(user_input: str) -> VEvent:
    event = get_vevent(user_input)
    
    while True:
        print(f"Event Details:\n{event}")
        confirm = typer.prompt("Are these details correct? [y/N]")
        if confirm.lower() in ['y', 'yes']:
            break
        event = get_vevent(f"{event}\nPlease provide the correct details for the event\n{confirm}")

    Event.create(**event.to_event_kwargs())
    return event

@app.command("create")
def create_event():
    user_input = typer.prompt("Please provide details for the new event")
    event = create_event_logic(user_input)
    print(f"Created Event:\n{event}")

def update_event_logic(user_input: str) -> Optional[VEvent]:
    events = Event.query(user_input)[:3]

    if not events:
        print("No events found with the provided keyword. Please try again.")
        return None

    while True:
        for i, event in enumerate(events):
            print(f"[{i + 1}] {event}")

        event_number = typer.prompt(
            "Please choose the event number to update (or enter '0' to search again)"
        )

        if event_number == "0":
            return None

        try:
            chosen_event = events[int(event_number) - 1]
            break
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")

    event = Event.read(chosen_event.ci_id)
    
    while True:
        print(f"Event Details:\n{event}")
        confirm = typer.prompt("Are these details correct? [y/N]")
        if confirm.lower() in ['y', 'yes']:
            break
        event = get_vevent(f"{event}\nPlease provide the CORRECT DETAILS for the event\n{confirm}")

    Event.update(event_id=chosen_event.ci_id, **event.to_event_kwargs())
    return event

@app.command("update")
def update_event():
    user_input = typer.prompt("Which event would you like to update?")
    event = update_event_logic(user_input)
    if event:
        print(f"Updated Event: {event}")

def delete_event_logic(user_input: str) -> bool:
    events = Event.query(user_input)[:3]

    if not events:
        print("No events found with the provided keyword. Please try again.")
        return False

    while True:
        for i, event in enumerate(events):
            print(f"[{i + 1}] {event}")

        event_number = typer.prompt(
            "Please choose the event number to delete (or enter '0' to search again)"
        )

        if event_number == "0":
            return False

        try:
            chosen_event = events[int(event_number) - 1]
            print(f"Deleting event:\n{chosen_event}")
            Event.delete(chosen_event.ci_id)
            return True
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")

@app.command("delete")
def delete_event():
    user_input = typer.prompt("Which event would you like to delete?")
    if delete_event_logic(user_input):
        print("Event deleted successfully.")

@app.command("list")
def list_events(
    page: int = 0, per_page: int = 3, sort: str = "dtstart", asc: bool = True
):
    events = Event.get_by_page(page=page, per_page=per_page, sort=sort, asc=asc)
    for event in events:
        print(event)

def export_event_logic(user_input: str, file_path: Optional[str] = None) -> bool:
    events = Event.query(user_input)[:3]

    if not events:
        print("No events found with the provided keyword. Please try again.")
        return False

    while True:
        for i, event in enumerate(events):
            print(f"[{i + 1}] {event}")

        event_number = typer.prompt(
            "Please choose the event number to export (or enter '0' to cancel)"
        )

        if event_number == "0":
            print("Export canceled.")
            return False

        try:
            chosen_event = events[int(event_number) - 1]
            print(f"Exporting event:\n{chosen_event}")
            ics_content = chosen_event.to_ics()

            if file_path:
                chosen_event.to_ics(file_path)
            else:
                export_file_path = typer.prompt(
                    "Please enter the export file path. If it is a directory, the filename will be the event summary and start time."
                )
                with open(export_file_path, "w") as f:
                    f.write(ics_content)
                print(f"Event exported to:\n{export_file_path}")
            return True
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")

@app.command("export")
def export_event(
    file_path: str = typer.Option(
        ".", "--file-path", "-f", help="The path to save the exported event"
    )
):
    user_input = typer.prompt("Which event would you like to export?")
    export_event_logic(user_input, file_path=file_path)

@app.command("import")
def create_5_events_to_db():
    events = [
        {
            "dtstart": str(datetime.now()),
            "dtend": str(datetime.now()),
            "duration": "1h",
            "summary": f"Event {i}",
            "description": f"Description of Event {i}",
            "location": f"Location of Event {i}",
        }
        for i in range(1, 6)
    ]

    for event_data in events:
        event = Event.create(**event_data)
        print(f"Created Event:\n{event}")

if __name__ == "__main__":
    app()
