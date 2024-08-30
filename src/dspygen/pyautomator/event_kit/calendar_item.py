import objc
import EventKit
from Foundation import NSDateComponents, NSURL, NSDate
from datetime import datetime
from typing import Optional, List, Union
import inject
from .alarm import Alarm

class CalendarItemError(Exception):
    pass

class CalendarItem:
    @inject.autoparams()
    def __init__(self, event_store: EventKit.EKEventStore):
        self.event_store = event_store
        self.ek_item = None  # This will be set by subclasses

    @property
    def ci_id(self) -> str:
        return self.ek_item.calendarItemIdentifier()

    @property
    def external_id(self) -> str:
        return self.ek_item.calendarItemExternalIdentifier()

    @property
    def title(self) -> str:
        return self.ek_item.title()

    @title.setter
    def title(self, value: str):
        self.ek_item.setTitle_(value)

    @property
    def calendar(self) -> EventKit.EKCalendar:
        return self.ek_item.calendar()

    @calendar.setter
    def calendar(self, value: EventKit.EKCalendar):
        self.ek_item.setCalendar_(value)

    @property
    def location(self) -> Optional[str]:
        return self.ek_item.location()

    @location.setter
    def location(self, value: Optional[str]):
        self.ek_item.setLocation_(value)

    @property
    def creation_date(self) -> datetime:
        ns_date = self.ek_item.creationDate()
        return datetime.fromtimestamp(ns_date.timeIntervalSince1970())

    @property
    def last_modified_date(self) -> datetime:
        ns_date = self.ek_item.lastModifiedDate()
        return datetime.fromtimestamp(ns_date.timeIntervalSince1970())

    @property
    def time_zone(self) -> str:
        return str(self.ek_item.timeZone())

    @time_zone.setter
    def time_zone(self, value: str):
        self.ek_item.setTimeZone_(EventKit.NSTimeZone.timeZoneWithName_(value))

    @property
    def url(self) -> Optional[str]:
        url = self.ek_item.URL()
        return str(url) if url else None

    @url.setter
    def url(self, value: Optional[str]):
        if value:
            self.ek_item.setURL_(NSURL.URLWithString_(value))
        else:
            self.ek_item.setURL_(None)

    @property
    def notes(self) -> Optional[str]:
        return self.ek_item.notes()

    @notes.setter
    def notes(self, value: str):
        self.ek_item.setNotes_(value)

    @property
    def has_attendees(self) -> bool:
        return self.ek_item.hasAttendees()

    @property
    def attendees(self) -> List[EventKit.EKParticipant]:
        return self.ek_item.attendees()

    def add_recurrence_rule(self, rule: EventKit.EKRecurrenceRule):
        self.ek_item.addRecurrenceRule_(rule)

    def remove_recurrence_rule(self, rule: EventKit.EKRecurrenceRule):
        self.ek_item.removeRecurrenceRule_(rule)

    @property
    def recurrence_rules(self) -> List[EventKit.EKRecurrenceRule]:
        return self.ek_item.recurrenceRules()

    def add_alarm(self, alarm: Alarm):
        """Add an alarm to the calendar item."""
        self.ek_item.addAlarm_(alarm.ek_alarm)

    def remove_alarm(self, alarm: Alarm):
        self.ek_item.removeAlarm_(alarm.ek_alarm)

    @property
    def alarms(self) -> List[Alarm]:
        ek_alarms = self.ek_item.alarms()
        return [Alarm(ek_alarm) for ek_alarm in (ek_alarms or [])]

    def save(self) -> None:
        raise NotImplementedError("Subclasses must implement the save method")

    def remove(self) -> None:
        raise NotImplementedError("Subclasses must implement the remove method")

    @property
    def has_recurrence_rule(self) -> bool:
        return self.ek_item.hasRecurrenceRules()

    @property
    def recurrence_rule(self) -> Optional[EventKit.EKRecurrenceRule]:
        rules = self.ek_item.recurrenceRules()
        return rules[0] if rules else None

    def set_recurrence(self, frequency: EventKit.EKRecurrenceFrequency, interval: int = 1, 
                       end_date: Optional[datetime] = None, occurrences: Optional[int] = None,
                       days_of_week: Optional[List[int]] = None, 
                       days_of_month: Optional[List[int]] = None,
                       months_of_year: Optional[List[int]] = None,
                       weeks_of_year: Optional[List[int]] = None,
                       days_of_year: Optional[List[int]] = None,
                       set_positions: Optional[List[int]] = None) -> None:
        """
        Set a nuanced recurrence rule for the calendar item.

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
            ek_days_of_week = [EventKit.EKRecurrenceDayOfWeek.dayOfWeek_(day+1) for day in days_of_week]

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
        self._set_recurrence_rule(recurrence_rule)

    def _set_recurrence_rule(self, rule: Optional[EventKit.EKRecurrenceRule]):
        if rule:
            self.ek_item.addRecurrenceRule_(rule)
        else:
            current_rule = self.recurrence_rule
            if current_rule:
                self.ek_item.removeRecurrenceRule_(current_rule)

    def remove_recurrence(self) -> None:
        self._set_recurrence_rule(None)


