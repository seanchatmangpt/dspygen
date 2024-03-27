import asyncio
import datetime
from textwrap import dedent

from dateutil import parser
from dataclasses import field, dataclass
from typing import Optional, Any

import typer

from dspygen.experiments.rfc5545.ical_models import Event
from dspygen.utils.date_tools import *

app = typer.Typer(help="Advanced Calendar Assistant")


@dataclass
class VEvent:
    dtstart: datetime.datetime = None
    dtend: Optional[datetime.datetime] = None
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


@app.command("create")
def create_event():
    user_input = typer.prompt("Please provide details for the new event")
    asyncio.run(_create_event(user_input))


async def _create_event(user_input):
    event = await get_vevent(user_input)

    # Display event details and ask for confirmation
    confirmed = False
    while not confirmed:
        print(f"Event Details:\n{event}")

        confirm = typer.prompt("Are these details correct? [y/N]")
        if confirm == "y" or confirm == "Y" or confirm == "yes" or confirm == "Yes":
            confirmed = True
        else:
            # Re-prompt for details
            event = await get_vevent(
                f"{event}\nPlease provide the correct details for the event\n{confirm}"
            )

    # Create the event
    Event.create(**event.to_event_kwargs())
    print(f"Created Event:\n{event}")


@app.command("update")
def update_event():
    user_input = typer.prompt("Which event would you like to update?")
    asyncio.run(_update_event(user_input))


async def _update_event(user_input):
    correct_event = False
    chosen_event = None

    while not correct_event:
        # Retrieve events based on user input

        events = Event.query(user_input)[:3]

        # print(events)

        if not events:
            print("No events found with the provided keyword. Please try again.")
            return

        # Display events and ask user to select one
        for i, event in enumerate(events):
            print(f"[{i + 1}] {event}")

        event_number = typer.prompt(
            "Please choose the event number to update (or enter '0' to search again)"
        )

        # Allow user to re-enter search keyword
        if event_number == "0":
            user_input = typer.prompt("Which event would you like to update?")
            return await _update_event(user_input)

        # Validate selection
        try:
            chosen_event = events[int(event_number) - 1]
            correct_event = True
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")
            continue

    # Proceed with event update logic
    await _update_chosen_event(chosen_event)


async def _update_chosen_event(chosen_event):
    print(f"Updating event: {chosen_event}")
    event = Event.read(chosen_event.id)

    # Display event details and ask for confirmation
    confirmed = False
    while not confirmed:
        print(f"Event Details:\n{event}")

        confirm = typer.prompt("Are these details correct? [y/N]")
        if confirm == "y" or confirm == "Y" or confirm == "yes" or confirm == "Yes":
            confirmed = True
        else:
            # Re-prompt for details
            event = await get_vevent(
                f"{event}\nPlease provide the CORRECT DETAILS for the event\n{confirm}"
            )

    # Create the event
    Event.update(event_id=chosen_event.id, **event.to_event_kwargs())
    print(f"Updated Event: {event}")


@app.command("delete")
def delete_event():
    user_input = typer.prompt("Which event would you like to delete?")
    asyncio.run(_delete_event(user_input))


async def _delete_event(user_input):
    correct_event = False
    chosen_event = None

    while not correct_event:
        # Retrieve events based on user input

        events = Event.query(user_input)[:3]

        # print(events)

        if not events:
            print("No events found with the provided keyword. Please try again.")
            return

        # Display events and ask user to select one
        for i, event in enumerate(events):
            print(f"[{i + 1}] {event}")

        event_number = typer.prompt(
            "Please choose the event number to delete (or enter '0' to search again)"
        )

        # Allow user to re-enter search keyword
        if event_number == "0":
            user_input = typer.prompt("Which event would you like to delete?")
            return await _delete_event(user_input)

        # Validate selection
        try:
            chosen_event = events[int(event_number) - 1]
            print(f"Deleting event:\n{chosen_event}")
            Event.delete(chosen_event.id)
            correct_event = True
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")
            continue


@app.command("list")
def list_events(
    page: int = 0, per_page: int = 3, sort: str = "dtstart", asc: bool = True
):
    asyncio.run(_list_events(page=page, per_page=per_page, sort=sort, asc=asc))


async def _list_events(
    page: int = 0, per_page: int = 3, sort: str = "dtstart", asc: bool = True
):
    events = Event.get_by_page(page=page, per_page=per_page, sort=sort, asc=asc)
    for event in events:
        print(event)


async def get_vevent(prompt):
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

    # vevent = await acreate(
    #     prompt=assistant_prompt, stop="\nEND:VEVENT", max_tokens=1000
    # )

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


@app.command("export")
def export_event(
    file_path: str = typer.Option(
        ".", "--file-path", "-f", help="The path to save the exported event"
    )
):
    user_input = typer.prompt("Which event would you like to export?")
    asyncio.run(_export_event(user_input, file_path=file_path))


async def _export_event(user_input, file_path=None):
    correct_event = False
    chosen_event = None

    while not correct_event:
        # Retrieve events based on user input

        events = Event.query(user_input)[:3]

        if not events:
            print("No events found with the provided keyword. Please try again.")
            return

        # Display events and ask user to select one for export
        for i, event in enumerate(events):
            print(f"[{i + 1}] {event}")

        event_number = typer.prompt(
            "Please choose the event number to export (or enter '0' to cancel)"
        )

        # Allow user to cancel the export
        if event_number == "0":
            print("Export canceled.")
            return

        # Validate selection
        try:
            chosen_event = events[int(event_number) - 1]
            print(f"Exporting event:\n{chosen_event}")
            ics_content = chosen_event.to_ics()  # Export the chosen event to ICS format

            if file_path:
                chosen_event.to_ics(file_path)
            else:
                # Prompt user for the export file path
                export_file_path = typer.prompt(
                    "Please enter the export file path. If it is a directory, the filename will be the event summary and start time."
                )
                # Prompt user for the export file path
                with open(export_file_path, "w") as f:
                    f.write(ics_content)
                print(f"Event exported to:\n{export_file_path}")
            correct_event = True
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")
            continue


@app.command("import")
def create_5_events_to_db() -> None:
    events = [
        {
            "dtstart": str(datetime.datetime.now()),
            "dtend": str(datetime.datetime.now()),
            "duration": "1h",
            "summary": "Event 1",
            "description": "Description of Event 1",
            "location": "Location of Event 1",
        },
        {
            "dtstart": str(datetime.datetime.now()),
            "dtend": str(datetime.datetime.now()),
            "duration": "1h",
            "summary": "Event 2",
            "description": "Description of Event 2",
            "location": "Location of Event 2",
        },
        {
            "dtstart": str(datetime.datetime.now()),
            "dtend": str(datetime.datetime.now()),
            "duration": "1h",
            "summary": "Event 3",
            "description": "Description of Event 3",
            "location": "Location of Event 3",
        },
        {
            "dtstart": str(datetime.datetime.now()),
            "dtend": str(datetime.datetime.now()),
            "duration": "1h",
            "summary": "Event 4",
            "description": "Description of Event 4",
            "location": "Location of Event 4",
        },
        {
            "dtstart": str(datetime.datetime.now()),
            "dtend": str(datetime.datetime.now()),
            "duration": "1h",
            "summary": "Event 5",
            "description": "Description of Event 5",
            "location": "Location of Event 5",
        },
    ]

    for event in events:
        event = Event.create(**event)
        print(f"Created Event:\n{event}")
