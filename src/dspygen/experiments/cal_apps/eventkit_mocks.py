from datetime import datetime, timedelta
from typing import List, Optional
from unittest.mock import MagicMock

class MockNSDate:
    @classmethod
    def date(cls):
        return cls()

    def timeIntervalSince1970(self):
        return datetime.now().timestamp()

class MockNSDateComponents:
    def __init__(self, year=2023, month=1, day=1, hour=0, minute=0):
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute

    def year(self): return self._year
    def month(self): return self._month
    def day(self): return self._day
    def hour(self): return self._hour
    def minute(self): return self._minute

    def setYear_(self, value): self._year = value
    def setMonth_(self, value): self._month = value
    def setDay_(self, value): self._day = value
    def setHour_(self, value): self._hour = value
    def setMinute_(self, value): self._minute = value

class MockEKAlarm:
    @classmethod
    def alarmWithRelativeOffset_(cls, offset):
        alarm = cls()
        alarm.relativeOffset = offset
        return alarm

class MockEKRecurrenceRule:
    def __init__(self, frequency, interval, end):
        self.frequency = frequency
        self.interval = interval
        self.recurrenceEnd = end

class MockEKCalendar:
    def __init__(self, title):
        self._title = title

    def title(self):
        return self._title

class MockEKReminder:
    @classmethod
    def reminderWithEventStore_(cls, event_store):
        return cls(event_store.reminderStore)  # Use reminderStore here

    def __init__(self, reminder_store):
        self.reminder_store = reminder_store
        self.title = ""
        self.calendar = None
        self.location = ""
        self.notes = ""
        self.url = None
        self.alarms = []
        self.recurrenceRules = []
        self.completed = False
        self.priority = 0
        self.dueDateComponents = None
        self.creationDate = MockNSDate()
        self.lastModifiedDate = MockNSDate()
        self._identifier = f"reminder-{id(self)}"

    def setTitle_(self, title):
        self.title = title

    def setCalendar_(self, calendar):
        self.calendar = calendar

    def setLocation_(self, location):
        self.location = location

    def setNotes_(self, notes):
        self.notes = notes

    def setURL_(self, url):
        self.url = url

    def addAlarm_(self, alarm):
        self.alarms.append(alarm)

    def removeAlarm_(self, alarm):
        self.alarms.remove(alarm)

    def addRecurrenceRule_(self, rule):
        self.recurrenceRules = [rule]  # Only one rule is supported

    def removeRecurrenceRule_(self, rule):
        self.recurrenceRules = []

    def setCompleted_(self, completed):
        self.completed = completed

    def setPriority_(self, priority):
        self.priority = priority

    def setDueDateComponents_(self, components):
        self.dueDateComponents = components

    def calendarItemIdentifier(self):
        return self._identifier

    def calendarItemExternalIdentifier(self):
        return self._identifier

    def isCompleted(self):
        return self.completed

    def hasRecurrenceRules(self):
        return len(self.recurrenceRules) > 0

class MockEKEventStore:
    def __init__(self):
        self.reminders = {}
        self.default_calendar = MockEKCalendar("Default")
        self.reminderStore = self  # Add this line

    def saveReminder_commit_error_(self, reminder, commit, error):
        self.reminders[reminder.calendarItemIdentifier()] = reminder
        return True, None

    def removeReminder_commit_error_(self, reminder, commit, error):
        del self.reminders[reminder.calendarItemIdentifier()]
        return True, None

    def calendarItemWithIdentifier_(self, identifier):
        return self.reminders.get(identifier)

    def defaultCalendarForNewReminders(self):
        return self.default_calendar

    def requestAccessToEntityType_completion_(self, entity_type, completion):
        completion(True, None)

class MockEventKit:
    EKEventStore = MockEKEventStore
    EKReminder = MockEKReminder
    EKAlarm = MockEKAlarm
    EKRecurrenceRule = MockEKRecurrenceRule
    NSDate = MockNSDate
    EKEntityTypeReminder = 1
    EKRecurrenceFrequencyDaily = 0

    @classmethod
    def patch(cls):
        return patch.multiple(
            'EventKit',
            EKEventStore=cls.EKEventStore,
            EKReminder=cls.EKReminder,
            EKAlarm=cls.EKAlarm,
            EKRecurrenceRule=cls.EKRecurrenceRule,
            NSDate=cls.NSDate,
            EKEntityTypeReminder=cls.EKEntityTypeReminder,
            EKRecurrenceFrequencyDaily=cls.EKRecurrenceFrequencyDaily
        )
