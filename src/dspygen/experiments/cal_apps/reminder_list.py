import EventKit
from typing import List, Optional
from dspygen.experiments.cal_apps import Reminder

class ReminderList:
    def __init__(self, name: str, event_store):
        self.name = name
        self.event_store = event_store
        self.ek_calendar = None
        self.reminders: List[Reminder] = []
        self._load_ek_calendar()

    def _load_ek_calendar(self):
        calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        for calendar in calendars:
            if calendar.title == self.name:
                self.ek_calendar = calendar
                break
        if not self.ek_calendar:
            self.ek_calendar = EventKit.EKCalendar.calendarForEntityType_eventStore_(EventKit.EKEntityTypeReminder, self.event_store)
            # Instead of setting the title directly, we'll pass it to the calendar creation method
            self.ek_calendar = EventKit.EKCalendar.calendarWithTitle_forEntityType_eventStore_(self.name, EventKit.EKEntityTypeReminder, self.event_store)
            self.ek_calendar.source = self.event_store.defaultCalendarForNewReminders().source
            self.event_store.saveCalendar_commit_error_(self.ek_calendar, True, None)

    def add_reminder(self, reminder: Reminder):
        reminder.save(self.event_store)
        self.reminders.append(reminder)

    def remove_reminder(self, reminder: Reminder):
        reminder.remove(self.event_store)
        self.reminders.remove(reminder)

    def get_reminders(self, completed: Optional[bool] = None) -> List[Reminder]:
        predicate = self.event_store.predicateForRemindersInCalendars_([self.ek_calendar])
        reminders = []
        def callback(results):
            for ek_reminder in results:
                if completed is None or ek_reminder.completed == completed:
                    reminders.append(Reminder(
                        title=ek_reminder.title,
                        due_date=self._format_due_date(ek_reminder.dueDateComponents),
                        flagged=ek_reminder.flagged,
                        completed=ek_reminder.completed,
                        ek_reminder=ek_reminder
                    ))
            self.reminders = reminders
        self.event_store.fetchRemindersMatchingPredicate_completion_(predicate, callback)
        return self.reminders

    @staticmethod
    def _format_due_date(date_components):
        if date_components:
            return f"{date_components.year}-{date_components.month:02d}-{date_components.day:02d} {date_components.hour:02d}:{date_components.minute:02d}"
        return None