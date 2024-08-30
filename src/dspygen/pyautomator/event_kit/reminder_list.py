import threading

import EventKit
from typing import Optional, List
import inject
from faker import Faker

from dspygen.pyautomator.event_kit.reminder import Reminder


class ReminderList:
    @inject.autoparams()
    def __init__(self, name: str, event_store: EventKit.EKEventStore):
        self.name = name
        self.event_store = event_store
        self.ek_calendar = None
        self._load_ek_calendar()

    def _load_ek_calendar(self):
        calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        for calendar in calendars:
            if calendar.title() == self.name:
                self.ek_calendar = calendar
                break
        if not self.ek_calendar:
            self.ek_calendar = EventKit.EKCalendar.calendarForEntityType_eventStore_(EventKit.EKEntityTypeReminder,
                                                                                     self.event_store)
            self.ek_calendar.setTitle_(self.name)
            self.ek_calendar.setSource_(self.event_store.defaultCalendarForNewReminders().source())
            self.event_store.saveCalendar_commit_error_(self.ek_calendar, True, None)

    def rename(self, new_name: str):
        self.ek_calendar.setTitle_(new_name)
        self.event_store.saveCalendar_commit_error_(self.ek_calendar, True, None)
        self.name = new_name

    def delete(self):
        self.event_store.removeCalendar_commit_error_(self.ek_calendar, True, None)

    def get_calendar(self):
        return self.ek_calendar

    def get_all_reminders(self) -> List[Reminder]:
        """Fetch all reminders in this list."""
        predicate = self.event_store.predicateForRemindersInCalendars_([self.ek_calendar])
        ek_reminders = []
        condition = threading.Condition()

        def callback(fetched_reminders):
            with condition:
                if fetched_reminders is not None:
                    ek_reminders.extend(fetched_reminders)
                else:
                    print("Error fetching reminders: fetched_reminders is None")
                condition.notify_all()

        with condition:
            self.event_store.fetchRemindersMatchingPredicate_completion_(predicate, callback)
            condition.wait()  # Wait until the callback notifies that it's done

        # Convert EKReminder objects to Reminder objects
        return [Reminder.from_ek_reminder(ek_reminder=ek_reminder) for ek_reminder in ek_reminders]


@inject.autoparams()
def main(event_store: EventKit.EKEventStore):
    fake = Faker()
    test_list = None

    try:
        # Request access to reminders
        access_granted = [False]

        def request_access_callback(granted, error):
            if not granted:
                print(f"Access to reminders denied. Error: {error}")
            else:
                access_granted[0] = True

        event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, request_access_callback)

        # Wait for access to be granted
        import time
        timeout = 5
        while not access_granted[0] and timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5

        if not access_granted[0]:
            raise PermissionError("Access to reminders not granted in time.")

        # Create a new ReminderList
        list_name = f"Test List: {fake.word().capitalize()}"
        test_list = ReminderList(list_name, event_store)
        print(f"Created ReminderList: {test_list.name}")

        # Rename the list
        new_name = f"Renamed List: {fake.word().capitalize()}"
        test_list.rename(new_name)
        print(f"Renamed list to: {test_list.name}")

        # Create a reminder in the list
        reminder = Reminder.create(event_store, fake.sentence(nb_words=4), test_list.get_calendar())
        reminder.save()
        print(f"Created reminder: {reminder.title}")

        # Wait for a moment to ensure changes are propagated
        time.sleep(0.01)

        # Test get_all_reminders
        all_reminders = test_list.get_all_reminders()
        print(f"Fetched {len(all_reminders)} reminders from the list")
        for reminder in all_reminders:
            print(f"Reminder: {reminder.title}")

        # Debug: Print all calendars
        calendars = event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        print(f"Total calendars: {len(calendars)}")
        for calendar in calendars:
            print(f"Calendar: {calendar.title()}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if test_list:
            try:
                # Delete the reminder
                for reminder in test_list.get_all_reminders():
                    event_store.removeReminder_commit_error_(reminder.ek_item, True, None)

                # Delete the test list
                test_list.delete()
                print(f"Deleted test list: {test_list.name}")
            except Exception as e:
                print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    main()
