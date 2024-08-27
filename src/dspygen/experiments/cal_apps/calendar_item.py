import objc
import EventKit
from Foundation import NSDateComponents, NSURL, NSDate
from datetime import datetime
from typing import Optional, List

class CalendarItemError(Exception):
    pass

class CalendarItem:
    def __init__(self, event_store: EventKit.EKEventStore):
        self.event_store = event_store
        self.ek_item = None  # This will be set by subclasses

    @property
    def calendar_item_identifier(self) -> str:
        return self.ek_item.calendarItemIdentifier()

    @property
    def calendar_item_external_identifier(self) -> str:
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
    def notes(self, value: Optional[str]):
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

    def add_alarm(self, alarm: EventKit.EKAlarm):
        self.ek_item.addAlarm_(alarm)

    def remove_alarm(self, alarm: EventKit.EKAlarm):
        self.ek_item.removeAlarm_(alarm)

    @property
    def alarms(self) -> List[EventKit.EKAlarm]:
        alarms = self.ek_item.alarms()
        return alarms if alarms is not None else []

    def save(self) -> None:
        raise NotImplementedError("Subclasses must implement the save method")

    def remove(self) -> None:
        raise NotImplementedError("Subclasses must implement the remove method")
