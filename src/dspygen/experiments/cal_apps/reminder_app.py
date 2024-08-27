import EventKit
from typing import List, Optional
from dspygen.experiments.cal_apps import ReminderList

class ReminderApp:
    def __init__(self):
        self.event_store = EventKit.EKEventStore.new()
        self.lists: List[ReminderList] = []
        self.selected_list: Optional[ReminderList] = None
        self._load_existing_lists()

    def _load_existing_lists(self):
        calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        for calendar in calendars:
            self.lists.append(ReminderList(calendar.title, self.event_store))

    def request_access(self):
        """Request access to reminders."""
        def callback(granted, error):
            if not granted:
                raise PermissionError("Access to reminders denied.")
        self.event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, callback)

    def add_list(self, reminder_list: ReminderList):
        self.lists.append(reminder_list)

    def remove_list(self, reminder_list: ReminderList):
        if reminder_list.ek_calendar:
            self.event_store.removeCalendar_commit_error_(reminder_list.ek_calendar, True, None)
        self.lists.remove(reminder_list)

    def select_list(self, list_name: str):
        for lst in self.lists:
            if lst.name == list_name:
                self.selected_list = lst
                return
        raise ValueError(f"List '{list_name}' not found")

    def add_reminder_to_selected(self, reminder):
        if self.selected_list:
            self.selected_list.add_reminder(reminder)
        else:
            raise ValueError("No list selected")

    def get_reminders(self, completed: Optional[bool] = None):
        if self.selected_list:
            return self.selected_list.get_reminders(completed)
        else:
            raise ValueError("No list selected")

    def clear_completed_reminders(self):
        if self.selected_list:
            completed_reminders = self.selected_list.get_reminders(completed=True)
            for reminder in completed_reminders:
                self.selected_list.remove_reminder(reminder)
        else:
            raise ValueError("No list selected")