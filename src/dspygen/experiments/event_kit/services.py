
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from dspygen.experiments.event_kit.models import Calendar, Reminder
from dspygen.experiments.event_kit.repositories import CalendarRepository, ReminderRepository


class CalendarService:
    def __init__(self, calendar_repo: CalendarRepository):
        self.calendar_repo = calendar_repo

    def create_calendar(self, title: str) -> Calendar:
        calendar = Calendar(title=title)
        self.calendar_repo.add(calendar)
        return calendar

    def get_calendar(self, calendar_id: UUID) -> Optional[Calendar]:
        return self.calendar_repo.get(calendar_id)

    def list_calendars(self) -> List[Calendar]:
        return self.calendar_repo.list()

    def update_calendar(self, calendar_id: UUID, title: str) -> Optional[Calendar]:
        calendar = self.calendar_repo.get(calendar_id)
        if calendar:
            calendar.title = title
            self.calendar_repo.update(calendar)
            return calendar
        return None

    def delete_calendar(self, calendar_id: UUID):
        self.calendar_repo.delete(calendar_id)

class ReminderService:
    def __init__(self, reminder_repo: ReminderRepository):
        self.reminder_repo = reminder_repo

    def create_reminder(self, calendar_id: UUID, title: str, due_date: Optional[datetime] = None, notes: Optional[str] = None) -> Reminder:
        reminder = Reminder(title=title, due_date=due_date, notes=notes, calendar_id=calendar_id)
        self.reminder_repo.add(reminder)
        return reminder

    def get_reminder(self, calendar_id: UUID, reminder_id: UUID) -> Optional[Reminder]:
        return self.reminder_repo.get(calendar_id, reminder_id)

    def update_reminder(self, calendar_id: UUID, reminder_id: UUID, title: Optional[str] = None, due_date: Optional[datetime] = None, notes: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Reminder]:
        reminder = self.reminder_repo.get(calendar_id, reminder_id)
        if reminder:
            if title:
                reminder.title = title
            if due_date:
                reminder.due_date = due_date
            if notes:
                reminder.notes = notes
            if completed is not None:
                reminder.completed = completed
            self.reminder_repo.update(calendar_id, reminder)
            return reminder
        return None

    def delete_reminder(self, calendar_id: UUID, reminder_id: UUID):
        self.reminder_repo.delete(calendar_id, reminder_id)

