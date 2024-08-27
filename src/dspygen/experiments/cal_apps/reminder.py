import objc
import EventKit
from Foundation import NSDateComponents
from datetime import datetime, timedelta
from typing import Optional

from dspygen.experiments.cal_apps.calendar_item import CalendarItemError, CalendarItem


class ReminderError(CalendarItemError):
    pass

class Reminder(CalendarItem):
    def __init__(self, event_store: EventKit.EKEventStore):
        super().__init__(event_store)
        self.ek_item = EventKit.EKReminder.reminderWithEventStore_(event_store)

    @classmethod
    def create(cls, event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar) -> 'Reminder':
        reminder = cls(event_store)
        reminder.title = title
        reminder.calendar = calendar
        return reminder

    @property
    def due_date(self) -> Optional[datetime]:
        components = self.ek_item.dueDateComponents()
        if components:
            return datetime(
                year=components.year(),
                month=components.month(),
                day=components.day(),
                hour=components.hour(),
                minute=components.minute()
            )
        return None

    @due_date.setter
    def due_date(self, value: Optional[datetime]):
        if value:
            components = NSDateComponents.alloc().init()
            components.setYear_(value.year)
            components.setMonth_(value.month)
            components.setDay_(value.day)
            components.setHour_(value.hour)
            components.setMinute_(value.minute)
            self.ek_item.setDueDateComponents_(components)
        else:
            self.ek_item.setDueDateComponents_(None)

    @property
    def completed(self) -> bool:
        return self.ek_item.isCompleted()

    @completed.setter
    def completed(self, value: bool):
        self.ek_item.setCompleted_(value)
        if value:
            self.ek_item.setCompletionDate_(EventKit.NSDate.date())
        else:
            self.ek_item.setCompletionDate_(None)

    @property
    def priority(self) -> int:
        return self.ek_item.priority()

    @priority.setter
    def priority(self, value: int):
        self.ek_item.setPriority_(value)

    @property
    def has_recurrence_rule(self) -> bool:
        return self.ek_item.hasRecurrenceRules()

    @property
    def recurrence_rule(self) -> Optional[EventKit.EKRecurrenceRule]:
        rules = self.ek_item.recurrenceRules()
        return rules[0] if rules else None

    def set_recurrence_rule(self, rule: Optional[EventKit.EKRecurrenceRule]):
        if rule:
            self.ek_item.addRecurrenceRule_(rule)
        else:
            current_rule = self.recurrence_rule
            if current_rule:
                self.ek_item.removeRecurrenceRule_(current_rule)

    def save(self) -> None:
        success, error = self.event_store.saveReminder_commit_error_(self.ek_item, True, objc.nil)
        if not success:
            raise ReminderError(f"Failed to save reminder: {error}")

    def remove(self) -> None:
        success, error = self.event_store.removeReminder_commit_error_(self.ek_item, True, objc.nil)
        if not success:
            raise ReminderError(f"Failed to remove reminder: {error}")

def create_reminder(event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar,
                    due_date: Optional[datetime] = None) -> Reminder:
    reminder = Reminder.create(event_store, title, calendar)
    if due_date:
        reminder.due_date = due_date
    reminder.save()
    print(f"Reminder '{title}' created successfully.")
    return reminder

def read_reminder(event_store: EventKit.EKEventStore, reminder_id: str) -> Reminder:
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

def main():
    event_store = EventKit.EKEventStore.alloc().init()

    def request_access_callback(granted, error):
        if not granted:
            raise PermissionError("Access to reminders denied.")

    event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, request_access_callback)

    default_calendar = event_store.defaultCalendarForNewReminders()

    # Create a new reminder
    new_reminder = create_reminder(event_store, "Test Reminder", default_calendar, datetime.now() + timedelta(days=1))

    # Test calendar item functions
    print(f"Calendar Item Identifier: {new_reminder.calendar_item_identifier}")
    print(f"Calendar Item External Identifier: {new_reminder.calendar_item_external_identifier}")
    print(f"Title: {new_reminder.title}")
    print(f"Calendar: {new_reminder.calendar.title()}")
    print(f"Creation Date: {new_reminder.creation_date}")
    print(f"Last Modified Date: {new_reminder.last_modified_date}")
    print(f"Time Zone: {new_reminder.time_zone}")

    # Test setting and getting location
    new_reminder.location = "Home Office"
    print(f"Location: {new_reminder.location}")

    # Test setting and getting notes
    new_reminder.notes = "This is a test reminder created by the calendar item base class."
    print(f"Notes: {new_reminder.notes}")

    # Test setting and getting URL
    new_reminder.url = "https://example.com/test-reminder"
    print(f"URL: {new_reminder.url}")

    # Test adding and removing alarms
    alarm = EventKit.EKAlarm.alarmWithRelativeOffset_(-3600)  # 1 hour before
    new_reminder.add_alarm(alarm)
    print(f"Alarms count: {len(new_reminder.alarms)}")
    new_reminder.remove_alarm(alarm)
    print(f"Alarms count after removal: {len(new_reminder.alarms)}")

    # Test setting and removing recurrence rule
    # recurrence_rule = EventKit.EKRecurrenceRule.recurrenceWithFrequency_interval_end_(
    #     EventKit.EKRecurrenceFrequencyDaily,
    #     1,
    #     None  # No end date
    # )
    # new_reminder.set_recurrence_rule(recurrence_rule)
    # print(f"Has Recurrence Rule: {new_reminder.has_recurrence_rule}")
    # print(f"Recurrence Rule: {new_reminder.recurrence_rule}")
    #
    # new_reminder.set_recurrence_rule(None)
    # print(f"Has Recurrence Rule after removal: {new_reminder.has_recurrence_rule}")

    # Test reminder-specific functions
    print(f"Due Date: {new_reminder.due_date}")
    print(f"Completed: {new_reminder.completed}")
    print(f"Priority: {new_reminder.priority}")

    # Update the reminder
    update_reminder(new_reminder, title="Updated Test Reminder", completed=False, priority=1)
    print(f"Updated reminder: {new_reminder.title}, Completed: {new_reminder.completed}, Priority: {new_reminder.priority}")

    # Delete the reminder
    delete_reminder(new_reminder)
    print("Reminder deleted successfully.")

if __name__ == "__main__":
    main()
