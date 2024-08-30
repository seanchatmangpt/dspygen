from datetime import datetime, timedelta
from typing import Optional

import inject


import EventKit

from dspygen.pyautomator.event_kit.alarm import Alarm
from dspygen.pyautomator.event_kit.reminder import Reminder, ReminderError


@inject.autoparams()
def create_reminder(event_store:EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar,
                    due_date: Optional[datetime] = None):
    reminder = Reminder.create(event_store, title, calendar)
    if due_date:
        reminder.due_date = due_date
    reminder.save()
    print(f"Reminder '{title}' created successfully.")
    return reminder

@inject.autoparams()
def read_reminder(event_store: EventKit.EKEventStore, reminder_id: str):
    ek_reminder = event_store.calendarItemWithIdentifier_(reminder_id)
    if ek_reminder and isinstance(ek_reminder, EventKit.EKReminder):
        reminder = Reminder(event_store)
        reminder.ek_item = ek_reminder
        return reminder
    else:
        raise ReminderError(f"Reminder with id '{reminder_id}' not found.")

def update_reminder(reminder: Reminder, title: Optional[str] = None, due_date: Optional[datetime] = None,
                    completed: Optional[bool] = None, priority: Optional[int] = None) -> None:
    if title is not None:
        reminder.title = title
    if due_date is not None:
        reminder.due_date = due_date
    if completed is not None:
        reminder.completed = completed
    if priority is not None:
        reminder.priority = priority
    reminder.save()

def delete_reminder(reminder: Reminder) -> None:
    reminder.remove()

@inject.autoparams()
def eval_recurrence(event_store: EventKit.EKEventStore):
    default_calendar = event_store.defaultCalendarForNewReminders()

    # Test various recurrence patterns
    recurrence_patterns = [
        ("Daily Reminder", EventKit.EKRecurrenceFrequencyDaily, 1, None, None, None, None, None),
        ("Weekly Monday Meeting", EventKit.EKRecurrenceFrequencyWeekly, 1, None, None, [1], None, None),
        ("Monthly Team Lunch", EventKit.EKRecurrenceFrequencyMonthly, 1, None, None, None, [15], None),
        ("Quarterly Review", EventKit.EKRecurrenceFrequencyYearly, 1, None, None, None, None, [1, 4, 7, 10]),
        ("Last Day of Month Task", EventKit.EKRecurrenceFrequencyMonthly, 1, None, None, None, [-1], None),
        ("First Monday of Quarter", EventKit.EKRecurrenceFrequencyYearly, 1, None, None, [1], None, [1, 4, 7, 10], [1]),
    ]

    for title, freq, interval, end_date, occurrences, days_of_week, days_of_month, months_of_year in recurrence_patterns:
        reminder = create_reminder(title=title, calendar=default_calendar, due_date=datetime.now() + timedelta(days=1))
        reminder.set_recurrence(
            frequency=freq,
            interval=interval,
            end_date=end_date,
            occurrences=occurrences,
            days_of_week=days_of_week,
            days_of_month=days_of_month,
            months_of_year=months_of_year
        )
        reminder.save()
        print(f"Created recurring reminder: {reminder}")
        print(f"Recurrence rule: {reminder.recurrence_rule}")
        print("---")

        # Clean up
        delete_reminder(reminder)

@inject.autoparams()
def main(event_store: EventKit.EKEventStore):
    def request_access_callback(granted, error):
        if not granted:
            raise PermissionError("Access to reminders denied.")

    event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, request_access_callback)

    default_calendar = event_store.defaultCalendarForNewReminders()

    # Existing code remains unchanged
    # Create a new reminder
    new_reminder = create_reminder(title="Test Reminder", calendar=default_calendar, due_date=datetime.now() + timedelta(days=1))
    reminder_id = new_reminder.ci_id

    # Read the created reminder
    read_reminder_obj = read_reminder(event_store, reminder_id)
    print(f"Read reminder title: {read_reminder_obj.title}")
    print(f"Read reminder due date: {read_reminder_obj.due_date}")

    # Test calendar item functions
    print(f"Calendar Item Identifier: {read_reminder_obj.ci_id}")
    print(f"Calendar Item External Identifier: {read_reminder_obj.external_id}")
    print(f"Title: {read_reminder_obj.title}")
    print(f"Calendar: {read_reminder_obj.calendar.title()}")
    print(f"Creation Date: {read_reminder_obj.creation_date}")
    print(f"Last Modified Date: {read_reminder_obj.last_modified_date}")
    print(f"Time Zone: {read_reminder_obj.time_zone}")

    # Test setting and getting location
    read_reminder_obj.location = "Home Office"
    print(f"Location: {read_reminder_obj.location}")

    # Test setting and getting notes
    read_reminder_obj.notes = "This is a test reminder created by the calendar item base class."
    print(f"Notes: {read_reminder_obj.notes}")

    # Test setting and getting URL
    read_reminder_obj.url = "https://example.com/test-reminder"
    print(f"URL: {read_reminder_obj.url}")

    # Test adding and removing alarms
    alarm = Alarm.with_relative_offset(timedelta(hours=-1))  # 1 hour before
    read_reminder_obj.add_alarm(alarm)
    print(f"Alarms count: {len(read_reminder_obj.alarms)}")
    read_reminder_obj.remove_alarm(alarm)
    print(f"Alarms count after removal: {len(read_reminder_obj.alarms)}")

    # Test reminder-specific functions
    print(f"Due Date: {read_reminder_obj.due_date}")
    print(f"Completed: {read_reminder_obj.completed}")
    print(f"Priority: {read_reminder_obj.priority}")

    # Update the reminder
    update_reminder(read_reminder_obj, title="Updated Test Reminder", completed=False, priority=1)
    print(f"Updated reminder: {read_reminder_obj.title}, Completed: {read_reminder_obj.completed}, Priority: {read_reminder_obj.priority}")

    # Delete the reminder
    delete_reminder(read_reminder_obj)
    print("Reminder deleted successfully.")

    # Try to read the deleted reminder (should raise an exception)
    try:
        read_reminder(event_store, reminder_id)
    except ReminderError as e:
        print(f"Expected error: {e}")



if __name__ == "__main__":
    main()
