import inject
from datetime import datetime, timedelta
from typing import Optional, List
import EventKit
from .calendar_item import CalendarItem
from .alarm import Alarm
from uuid import uuid4
from .recurrence_rule import RecurrenceRule


class CalendarEventError(Exception):
    pass


class CalendarEvent(CalendarItem):
    @inject.autoparams()
    def __init__(self, event_store: EventKit.EKEventStore):
        super().__init__(event_store)
        self.ek_item = EventKit.EKEvent.eventWithEventStore_(event_store)

    @classmethod
    @inject.autoparams()
    def create(cls, event_store: EventKit.EKEventStore, title: str, calendar: Optional[EventKit.EKCalendar] = None):
        event = cls(event_store)
        event.title = title
        if calendar is None:
            calendar = event_store.defaultCalendarForNewEvents()
        event.calendar = calendar
        return event

    @property
    def start_date(self) -> datetime:
        ns_date = self.ek_item.startDate()
        return datetime.fromtimestamp(ns_date.timeIntervalSince1970())

    @start_date.setter
    def start_date(self, value: datetime):
        ns_date = EventKit.NSDate.dateWithTimeIntervalSince1970_(value.timestamp())
        self.ek_item.setStartDate_(ns_date)

    @property
    def end_date(self) -> datetime:
        ns_date = self.ek_item.endDate()
        return datetime.fromtimestamp(ns_date.timeIntervalSince1970())

    @end_date.setter
    def end_date(self, value: datetime):
        ns_date = EventKit.NSDate.dateWithTimeIntervalSince1970_(value.timestamp())
        self.ek_item.setEndDate_(ns_date)

    @property
    def organizer(self) -> Optional[EventKit.EKParticipant]:
        return self.ek_item.organizer()

    @property
    def availability(self) -> EventKit.EKEventAvailability:
        return self.ek_item.availability()

    @availability.setter
    def availability(self, value: EventKit.EKEventAvailability):
        self.ek_item.setAvailability_(value)

    def save(self, span: EventKit.EKSpan = EventKit.EKSpanThisEvent) -> bool:
        return self.event_store.saveEvent_span_commit_error_(self.ek_item, span, True, None)

    def remove(self, span: EventKit.EKSpan = EventKit.EKSpanThisEvent) -> bool:
        return self.event_store.removeEvent_span_commit_error_(self.ek_item, span, True, None)

    @property
    def attendees(self) -> List[EventKit.EKParticipant]:
        attendees = self.ek_item.attendees()
        return attendees if attendees is not None else []

    def get_attendee_details(self, attendee: EventKit.EKParticipant) -> dict:
        return {
            'name': attendee.name(),
            'email': attendee.emailAddress(),
            'is_current_user': attendee.currentUser(),
            'role': attendee.participantRole(),
            'status': attendee.participantStatus(),
            'type': attendee.participantType(),
            'url': attendee.URL(),
        }

    def set_span(self, start_date: datetime, end_date: datetime) -> None:
        self.start_date = start_date
        self.end_date = end_date

    def to_rfc5545(self) -> str:
        """
        Convert the calendar event to an RFC 5545 compliant string.
        """
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//dspygen//CalendarEvent//EN",
            "BEGIN:VEVENT",
            f"SUMMARY:{self.title}",
            f"DTSTART:{self.start_date.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{self.end_date.strftime('%Y%m%dT%H%M%SZ')}",
            f"UID:{self.ci_id or str(uuid4())}",
        ]

        if self.location:
            lines.append(f"LOCATION:{self.location}")
        if self.notes:
            lines.append(f"DESCRIPTION:{self.notes}")

        for attendee in self.attendees:
            details = self.get_attendee_details(attendee)
            lines.append(f"ATTENDEE:mailto:{details['email']}")

        for alarm in self.alarms:
            lines.extend(alarm.to_rfc5545_lines())

        recurrence_rule = self.recurrence_rule
        if recurrence_rule:
            lines.append(f"RRULE:{recurrence_rule.to_string()}")

        lines.extend([
            "END:VEVENT",
            "END:VCALENDAR"
        ])

        return "\r\n".join(lines)

    @property
    def recurrence_rule(self) -> Optional[RecurrenceRule]:
        ek_rule = self.ek_item.recurrenceRule()
        return RecurrenceRule(ek_rule) if ek_rule else None

    def set_recurrence(self, frequency: EventKit.EKRecurrenceFrequency, interval: int = 1,
                       end_date: Optional[datetime] = None, occurrences: Optional[int] = None,
                       days_of_week: Optional[List[int]] = None,
                       days_of_month: Optional[List[int]] = None,
                       months_of_year: Optional[List[int]] = None,
                       weeks_of_year: Optional[List[int]] = None,
                       days_of_year: Optional[List[int]] = None,
                       set_positions: Optional[List[int]] = None) -> None:
        recurrence_rule = RecurrenceRule.create(
            frequency, interval, end_date, occurrences, days_of_week, days_of_month,
            months_of_year, weeks_of_year, days_of_year, set_positions
        )
        self.ek_item.setRecurrenceRule_(recurrence_rule.ek_recurrence_rule)
