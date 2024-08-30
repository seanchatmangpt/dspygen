from __future__ import annotations

import objc
import EventKit
from Foundation import NSDateComponents
from datetime import datetime, timedelta
from typing import Optional, List
import inject

from dspygen.modules.generate_icalendar_module import generate_i_calendar_call
from icalendar import Calendar
import logging

from dspygen.pyautomator.event_kit.calendar_item import CalendarItemError, CalendarItem

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReminderError(CalendarItemError):
    pass


class Reminder(CalendarItem):
    @inject.autoparams()
    def __init__(self, event_store: EventKit.EKEventStore):
        super().__init__(event_store)
        self.ek_item = EventKit.EKReminder.reminderWithEventStore_(event_store)

    @classmethod
    @inject.autoparams()
    def create(cls, event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar):
        reminder = cls(event_store)
        reminder.title = title
        reminder.calendar = calendar
        return reminder

    @classmethod
    @inject.autoparams()
    def from_ek_reminder(cls, event_store: EventKit.EKEventStore, ek_reminder: EventKit.EKReminder):
        reminder = cls(event_store)
        reminder.ek_item = ek_reminder
        return reminder

    @classmethod
    @inject.autoparams()
    def from_id(cls, event_store: EventKit.EKEventStore, reminder_id: str):
        ek_reminder = event_store.calendarItemWithIdentifier_(reminder_id)
        if ek_reminder is None or not isinstance(ek_reminder, EventKit.EKReminder):
            raise ValueError(f"Invalid reminder ID: {reminder_id}")
        return cls.from_ek_reminder(event_store, ek_reminder)

    @classmethod
    def create_from_rfc5545(cls, event_store: EventKit.EKEventStore, ical_string: str, calendar: EventKit.EKCalendar):
        """Create a reminder from RFC5545 iCalendar data and add it to the calendar."""
        logger.info("Received iCalendar text:")
        logger.info(ical_string)

        # Validate the iCalendar string
        cls._validate_ical(ical_string)

        # Parse the iCalendar data
        cal = Calendar.from_ical(ical_string)
        event = list(cal.walk('VEVENT'))[0]

        # Create a new reminder
        reminder = cls.create(event_store, event.get('summary'), calendar)
        reminder.notes = event.get('description')
        reminder.due_date = event.get('dtstart').dt

        # Set other properties if available
        if 'rrule' in event:
            # Parse and set recurrence rule
            # This would require additional logic to convert iCal RRULE to EKRecurrenceRule
            pass

        # Save the reminder
        reminder.save()

        return reminder

    @staticmethod
    def _validate_ical(ical_string: str):
        """Validate the iCalendar string."""
        try:
            cal = Calendar.from_ical(ical_string)
            events = list(cal.walk('VEVENT'))
            if not events:
                raise ValueError("No VEVENT component found in the iCalendar data")
            logger.info("iCalendar data validated successfully")
        except Exception as e:
            logger.error(f"Invalid iCalendar data: {e}")
            raise

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

    def save(self) -> None:
        success, error = self.event_store.saveReminder_commit_error_(self.ek_item, True, objc.nil)
        if not success:
            raise ReminderError(f"Failed to save reminder: {error}")

    def remove(self) -> None:
        success, error = self.event_store.removeReminder_commit_error_(self.ek_item, True, objc.nil)
        if not success:
            raise ReminderError(f"Failed to remove reminder: {error}")

    def __str__(self):
        recurrence = self.recurrence_rule
        recurrence_str = str(recurrence) if recurrence else "None"

        return (
            f"Reminder: {self.title}\n"
            f"ID: {self.ci_id}\n"
            f"Calendar: {self.calendar.title()}\n"
            f"Due Date: {self.due_date}\n"
            f"Completed: {self.completed}\n"
            f"Priority: {self.priority}\n"
            f"Has Recurrence Rule: {self.has_recurrence_rule}\n"
            f"Recurrence Rule: {recurrence_str}\n"
            f"Notes: {self.notes}"
        )

    def set_recurrence(self, frequency: EventKit.EKRecurrenceFrequency, interval: int = 1,
                       end_date: Optional[datetime] = None, occurrences: Optional[int] = None,
                       days_of_week: Optional[List[int]] = None,
                       days_of_month: Optional[List[int]] = None,
                       months_of_year: Optional[List[int]] = None,
                       weeks_of_year: Optional[List[int]] = None,
                       days_of_year: Optional[List[int]] = None,
                       set_positions: Optional[List[int]] = None) -> None:
        """
        Set a nuanced recurrence rule for the reminder.

        :param frequency: EKRecurrenceFrequency (Daily, Weekly, Monthly, or Yearly)
        :param interval: How often the rule repeats (default: 1)
        :param end_date: Optional end date for the recurrence
        :param occurrences: Optional number of occurrences
        :param days_of_week: Optional list of days of the week (0 = Sunday, 1 = Monday, etc.)
        :param days_of_month: Optional list of days of the month (1 to 31, or -1 to -31 for last day of month)
        :param months_of_year: Optional list of months (1 to 12)
        :param weeks_of_year: Optional list of weeks of the year (1 to 53, or -1 to -53 for last week)
        :param days_of_year: Optional list of days of the year (1 to 366, or -1 to -366 for last day)
        :param set_positions: Optional list of set positions (-366 to 366, excluding 0)
        """
        # Create recurrence end if specified
        recurrence_end = None
        if end_date:
            recurrence_end = EventKit.EKRecurrenceEnd.recurrenceEndWithEndDate_(end_date)
        elif occurrences:
            recurrence_end = EventKit.EKRecurrenceEnd.recurrenceEndWithOccurrenceCount_(occurrences)

        # Create days of week array if specified
        ek_days_of_week = None
        if days_of_week:
            ek_days_of_week = [EventKit.EKRecurrenceDayOfWeek.dayOfWeek_(day) for day in days_of_week]

        # Create recurrence rule
        recurrence_rule = EventKit.EKRecurrenceRule.alloc().initRecurrenceWithFrequency_interval_daysOfTheWeek_daysOfTheMonth_monthsOfTheYear_weeksOfTheYear_daysOfTheYear_setPositions_end_(
            frequency,
            interval,
            ek_days_of_week,
            days_of_month,
            months_of_year,
            weeks_of_year,
            days_of_year,
            set_positions,
            recurrence_end
        )

        # Set the recurrence rule
        self.set_recurrence_rule(recurrence_rule)
