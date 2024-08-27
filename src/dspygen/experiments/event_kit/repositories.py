
from typing import List, Optional
from uuid import UUID

from dspygen.experiments.event_kit.models import Calendar, Reminder


class CalendarRepository:
    def __init__(self):
        self._calendars = []

    def add(self, calendar: Calendar):
        self._calendars.append(calendar)

    def get(self, calendar_id: UUID) -> Optional[Calendar]:
        return next((c for c in self._calendars if c.id == calendar_id), None)

    def list(self) -> List[Calendar]:
        return self._calendars

    def update(self, updated_calendar: Calendar):
        for i, calendar in enumerate(self._calendars):
            if calendar.id == updated_calendar.id:
                self._calendars[i] = updated_calendar
                return

    def delete(self, calendar_id: UUID):
        self._calendars = [c for c in self._calendars if c.id != calendar_id]

class ReminderRepository:
    def __init__(self, calendar_repo: CalendarRepository):
        self.calendar_repo = calendar_repo

    def add(self, reminder: Reminder):
        calendar = self.calendar_repo.get(reminder.calendar_id)
        if calendar:
            calendar.add_reminder(reminder)

    def get(self, calendar_id: UUID, reminder_id: UUID) -> Optional[Reminder]:
        calendar = self.calendar_repo.get(calendar_id)
        if calendar:
            return next((r for r in calendar.reminders if r.id == reminder_id), None)
        return None

    def update(self, calendar_id: UUID, updated_reminder: Reminder):
        calendar = self.calendar_repo.get(calendar_id)
        if calendar:
            calendar.remove_reminder(updated_reminder.id)
            calendar.add_reminder(updated_reminder)

    def delete(self, calendar_id: UUID, reminder_id: UUID):
        calendar = self.calendar_repo.get(calendar_id)
        if calendar:
            calendar.remove_reminder(reminder_id)

