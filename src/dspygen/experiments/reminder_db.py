from Foundation import *
from EventKit import *


def request_access_to_reminders():
    event_store = EKEventStore.alloc().init()

    def completion_handler(granted, error):
        if granted:
            print("Access to Reminders granted.")
            fetch_reminders(event_store)
            create_reminder(event_store)
        else:
            print("Access to Reminders denied.")

    event_store.requestAccessToEntityType_completion_(EKEntityTypeReminder, completion_handler)
    return event_store


def fetch_reminders(event_store):
    reminder_predicate = event_store.predicateForRemindersInCalendars_(None)

    def completion_handler(reminders):
        for reminder in reminders:
            print(f"Title: {reminder.title()}")
            print(f"Completed: {reminder.isCompleted()}")
            print(f"Due Date: {reminder.dueDateComponents()}\n")

    event_store.fetchRemindersMatchingPredicate_completion_(reminder_predicate, completion_handler)


def create_reminder(event_store):
    reminder = EKReminder.reminderWithEventStore_(event_store)
    reminder.setTitle_("New Reminder from PyObjC")
    reminder.setCalendar_(event_store.defaultCalendarForNewReminders())

    due_date = NSDateComponents.alloc().init()
    due_date.setYear_(2024)
    due_date.setMonth_(8)
    due_date.setDay_(25)

    reminder.setDueDateComponents_(due_date)

    error = None
    event_store.saveReminder_commit_error_(reminder, True, error)

    if error:
        print(f"Failed to save reminder: {error}")
    else:
        print("Reminder saved successfully.")


if __name__ == "__main__":
    request_access_to_reminders()
