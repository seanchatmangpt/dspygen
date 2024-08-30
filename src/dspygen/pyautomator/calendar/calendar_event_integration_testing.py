from datetime import datetime, timedelta
import inject
import EventKit

import subprocess
import tempfile
import os

from dspygen.pyautomator.event_kit.alarm import Alarm
from dspygen.pyautomator.event_kit.calendar_event import CalendarEvent


@inject.autoparams()
def create_event(event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar,
                 start_date: datetime, end_date: datetime):
    event = CalendarEvent.create(event_store, title, calendar)
    event.set_span(start_date, end_date)
    event.save()
    print(f"Event '{title}' created successfully.")
    return event


@inject.autoparams()
def read_event(event_store: EventKit.EKEventStore, event_id: str):
    ek_event = event_store.calendarItemWithIdentifier_(event_id)
    if ek_event and isinstance(ek_event, EventKit.EKEvent):
        event = CalendarEvent(event_store)
        event.ek_item = ek_event
        return event
    else:
        raise ValueError(f"Event with id '{event_id}' not found.")


def update_event(event: CalendarEvent, title: str = None, start_date: datetime = None,
                 end_date: datetime = None):
    if title:
        event.title = title
    if start_date and end_date:
        event.set_span(start_date, end_date)
    event.save()
    print(f"Event updated successfully.")


def delete_event(event: CalendarEvent):
    event.remove()
    print("Event deleted successfully.")


def eval_event_properties(event: CalendarEvent):
    print(f"Event ID: {event.ci_id}")
    print(f"Title: {event.title}")
    print(f"Start Date: {event.start_date}")
    print(f"End Date: {event.end_date}")
    print(f"Calendar: {event.calendar.title()}")
    print(f"Time Zone: {event.time_zone}")
    print(f"Has Attendees: {event.has_attendees}")
    print(f"Availability: {event.availability}")


def eval_alarms(event: CalendarEvent):
    # Add absolute date alarm
    absolute_alarm = Alarm.with_absolute_date(event.start_date - timedelta(hours=1))
    event.add_alarm(absolute_alarm)

    # Add relative offset alarm
    relative_alarm = Alarm.with_relative_offset(timedelta(minutes=-30))
    event.add_alarm(relative_alarm)

    event.save()
    print(f"Number of alarms: {len(event.alarms)}")

    # Remove an alarm
    event.remove_alarm(relative_alarm)
    event.save()
    print(f"Number of alarms after removal: {len(event.alarms)}")


def eval_attendees(event: CalendarEvent):
    attendees = event.attendees
    if attendees is None:
        print("No attendees found or unable to retrieve attendees.")
        return

    print(f"Number of attendees: {len(attendees)}")
    for attendee in attendees:
        details = event.get_attendee_details(attendee)
        print(f"Attendee: {details['name']} ({details['email']})")
        print(f"  Role: {details['role']}")
        print(f"  Status: {details['status']}")
        print(f"  Type: {details['type']}")
        print(f"  Is Current User: {details['is_current_user']}")

    print("Note: EventKit does not allow adding or removing attendees programmatically.")


def eval_recurrence(event: CalendarEvent):
    event.set_recurrence(
        frequency=EventKit.EKRecurrenceFrequencyWeekly,
        interval=2,
        end_date=event.start_date + timedelta(days=60),
        days_of_week=[0, 2, 4]  # Sunday, Tuesday, Thursday
    )
    event.save()
    print(f"Recurrence rule: {event.recurrence_rule}")


def eval_rfc5545(event: CalendarEvent):
    rfc5545_string = event.to_rfc5545()
    print("RFC 5545 representation of the event:")
    print(rfc5545_string)
    
    # Optionally, you can add more detailed checks here
    # For example, checking if specific components are present in the string
    assert "BEGIN:VCALENDAR" in rfc5545_string
    assert "BEGIN:VEVENT" in rfc5545_string
    assert f"SUMMARY:{event.title}" in rfc5545_string
    assert "DTSTART:" in rfc5545_string
    assert "DTEND:" in rfc5545_string
    assert "UID:" in rfc5545_string
    assert "END:VEVENT" in rfc5545_string
    assert "END:VCALENDAR" in rfc5545_string

    print("RFC 5545 string validation passed.")


@inject.autoparams()
def main(event_store: EventKit.EKEventStore):
    def request_access_callback(granted, error):
        if not granted:
            raise PermissionError("Access to calendar denied.")

    event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, request_access_callback)

    default_calendar = event_store.defaultCalendarForNewEvents()

    # Create a new event
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(hours=2)
    new_event = create_event(event_store, "eval Event", default_calendar, start_date, end_date)
    event_id = new_event.ci_id

    # Read the created event
    read_event_obj = read_event(event_store, event_id)
    eval_event_properties(read_event_obj)

    # Update the event
    update_event(read_event_obj, title="Updated eval Event")
    eval_event_properties(read_event_obj)

    # eval alarms
    eval_alarms(read_event_obj)

    # eval attendees
    eval_attendees(read_event_obj)

    # eval recurrence
    eval_recurrence(read_event_obj)

    # Evaluate RFC 5545 string
    eval_rfc5545(read_event_obj)

    # Delete the event
    delete_event(read_event_obj)

    # Try to read the deleted event (should raise an exception)
    try:
        read_event(event_store, event_id)
    except ValueError as e:
        print(f"Expected error: {e}")


if __name__ == "__main__":
    main()
