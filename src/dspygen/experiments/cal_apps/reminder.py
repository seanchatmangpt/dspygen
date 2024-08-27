import objc
import EventKit
from Foundation import NSDateComponents
from datetime import datetime, timedelta
from typing import Optional, List

class ReminderError(Exception):
    pass

class Reminder:
    def __init__(self, event_store: EventKit.EKEventStore):
        self.event_store = event_store
        self.ek_reminder = EventKit.EKReminder.reminderWithEventStore_(event_store)

    @classmethod
    def create(cls, event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar) -> 'Reminder':
        reminder = cls(event_store)
        reminder.set_title(title)
        reminder.set_calendar(calendar)
        return reminder

    def set_title(self, value: str):
        self.ek_reminder.setTitle_(value)

    def get_title(self) -> str:
        return self.ek_reminder.title()

    def set_calendar(self, value: EventKit.EKCalendar):
        self.ek_reminder.setCalendar_(value)

    def get_calendar(self) -> EventKit.EKCalendar:
        return self.ek_reminder.calendar()

    def set_due_date(self, value: Optional[datetime]):
        if value:
            components = NSDateComponents.alloc().init()
            components.setYear_(value.year)
            components.setMonth_(value.month)
            components.setDay_(value.day)
            components.setHour_(value.hour)
            components.setMinute_(value.minute)
            self.ek_reminder.setDueDateComponents_(components)
        else:
            self.ek_reminder.setDueDateComponents_(None)

    def get_due_date(self) -> Optional[datetime]:
        components = self.ek_reminder.dueDateComponents()
        if components:
            return datetime(
                year=components.year(),
                month=components.month(),
                day=components.day(),
                hour=components.hour(),
                minute=components.minute()
            )
        return None

    def set_completed(self, value: bool):
        self.ek_reminder.setCompleted_(value)
        if value:
            self.ek_reminder.setCompletionDate_(EventKit.NSDate.date())
        else:
            self.ek_reminder.setCompletionDate_(None)

    def get_completed(self) -> bool:
        return self.ek_reminder.isCompleted()

    def set_priority(self, value: int):
        self.ek_reminder.setPriority_(value)

    def get_priority(self) -> int:
        return self.ek_reminder.priority()

    def add_alarm(self, alarm: EventKit.EKAlarm):
        self.ek_reminder.addAlarm_(alarm)

    def remove_alarm(self, alarm: EventKit.EKAlarm):
        self.ek_reminder.removeAlarm_(alarm)

    def get_alarms(self) -> List[EventKit.EKAlarm]:
        return self.ek_reminder.alarms()

    def save(self) -> None:
        success, error = self.event_store.saveReminder_commit_error_(self.ek_reminder, True, objc.nil)
        if not success:
            raise ReminderError(f"Failed to save reminder: {error}")

    def remove(self) -> None:
        success, error = self.event_store.removeReminder_commit_error_(self.ek_reminder, True, objc.nil)
        if not success:
            raise ReminderError(f"Failed to remove reminder: {error}")

def create_reminder(event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar,
                    due_date: Optional[datetime] = None) -> Reminder:
    reminder = Reminder.create(event_store, title, calendar)
    if due_date:
        reminder.set_due_date(due_date)
    reminder.save()
    print(f"Reminder '{title}' created successfully.")
    return reminder

def read_reminder(event_store: EventKit.EKEventStore, reminder_id: str) -> Reminder:
    ek_reminder = event_store.calendarItemWithIdentifier_(reminder_id)
    if ek_reminder and isinstance(ek_reminder, EventKit.EKReminder):
        reminder = Reminder(event_store)
        reminder.ek_reminder = ek_reminder
        return reminder
    else:
        raise ReminderError(f"Reminder with id '{reminder_id}' not found.")

def update_reminder(reminder: Reminder, title: Optional[str] = None, due_date: Optional[datetime] = None,
                    completed: Optional[bool] = None, priority: Optional[int] = None) -> None:
    if title:
        reminder.set_title(title)
    if due_date is not None:
        reminder.set_due_date(due_date)
    if completed is not None:
        reminder.set_completed(completed)
    if priority is not None:
        reminder.set_priority(priority)
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

    new_reminder = create_reminder(event_store, "Test Reminder", default_calendar, datetime.now() + timedelta(days=1))

    retrieved_reminder = read_reminder(event_store, new_reminder.ek_reminder.calendarItemIdentifier())
    print(f"Retrieved reminder: {retrieved_reminder.get_title()}, Due: {retrieved_reminder.get_due_date()}")

    update_reminder(retrieved_reminder, title="Updated Test Reminder", completed=False, priority=1)
    print(f"Updated reminder: {retrieved_reminder.get_title()}, Completed: {retrieved_reminder.get_completed()}, Priority: {retrieved_reminder.get_priority()}")


if __name__ == "__main__":
    main()
