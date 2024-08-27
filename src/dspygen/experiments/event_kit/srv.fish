#!/usr/bin/env fish

# Directory where the files will be created
set directory /Users/sac/dev/dspygen/src/dspygen/experiments/events_kit_v2

# Ensure the directory exists
mkdir -p $directory

# Create and write the EKObject class
echo 'import objc
from Foundation import NSObject

class EKObject(NSObject):
    def __init__(self):
        EventKit = objc.importFramework("EventKit")
        self._ekobject = EventKit.EKObject.alloc().init()

    def has_changes(self):
        return self._ekobject.hasChanges()

    def is_new(self):
        return self._ekobject.isNew()

    def refresh(self):
        self._ekobject.refresh()

    def reset(self):
        self._ekobject.reset()

    def rollback(self):
        self._ekobject.rollback()
' > $directory/ekobject.py

# Create and write the EKEvent class
echo 'import objc
from Foundation import NSObject
from ekobject import EKObject

class EKEvent(EKObject):
    def __init__(self, event_store):
        super().__init__()
        EventKit = objc.importFramework("EventKit")
        self._ekevent = EventKit.EKEvent.eventWithEventStore_(event_store)

    @property
    def title(self):
        return self._ekevent.title()

    @title.setter
    def title(self, value):
        self._ekevent.setTitle_(value)

    @property
    def start_date(self):
        return self._ekevent.startDate()

    @start_date.setter
    def start_date(self, value):
        self._ekevent.setStartDate_(value)

    @property
    def end_date(self):
        return self._ekevent.endDate()

    @end_date.setter
    def end_date(self, value):
        self._ekevent.setEndDate_(value)

    @property
    def calendar(self):
        return self._ekevent.calendar()

    @calendar.setter
    def calendar(self, value):
        self._ekevent.setCalendar_(value)

    @property
    def alarms(self):
        return self._ekevent.alarms()

    @alarms.setter
    def alarms(self, value):
        self._ekevent.setAlarms_(value)

    @property
    def recurrence_rules(self):
        return self._ekevent.recurrenceRules()

    @recurrence_rules.setter
    def recurrence_rules(self, value):
        self._ekevent.setRecurrenceRules_(value)

    def save_event(self, event_store, span, commit):
        success = event_store.saveEvent_span_commit_error_(self._ekevent, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to save event")

    def remove_event(self, event_store, span, commit):
        success = event_store.removeEvent_span_commit_error_(self._ekevent, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove event")
' > $directory/ekevent.py

# Create and write the EKReminder class
echo 'import objc
from Foundation import NSObject
from ekobject import EKObject

class EKReminder(EKObject):
    def __init__(self, event_store):
        super().__init__()
        EventKit = objc.importFramework("EventKit")
        self._ekreminder = EventKit.EKReminder.reminderWithEventStore_(event_store)

    @property
    def title(self):
        return self._ekreminder.title()

    @title.setter
    def title(self, value):
        self._ekreminder.setTitle_(value)

    @property
    def calendar(self):
        return self._ekreminder.calendar()

    @calendar.setter
    def calendar(self, value):
        self._ekreminder.setCalendar_(value)

    @property
    def start_date_components(self):
        return self._ekreminder.startDateComponents()

    @start_date_components.setter
    def start_date_components(self, value):
        self._ekreminder.setStartDateComponents_(value)

    @property
    def due_date_components(self):
        return self._ekreminder.dueDateComponents()

    @due_date_components.setter
    def due_date_components(self, value):
        self._ekreminder.setDueDateComponents_(value)

    @property
    def completed(self):
        return self._ekreminder.completed()

    @completed.setter
    def completed(self, value):
        self._ekreminder.setCompleted_(value)

    def save_reminder(self, event_store, commit):
        success = event_store.saveReminder_commit_error_(self._ekreminder, commit, objc.nil)
        if not success:
            raise Exception("Failed to save reminder")

    def remove_reminder(self, event_store, commit):
        success = event_store.removeReminder_commit_error_(self._ekreminder, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove reminder")
' > $directory/ekreminder.py

# Create and write the EKEventStore class
echo 'import objc
from Foundation import NSObject

class EKEventStore(NSObject):
    def __init__(self):
        EventKit = objc.importFramework("EventKit")
        self._ekeventstore = EventKit.EKEventStore.alloc().init()

    def request_access(self, entity_type, callback):
        self._ekeventstore.requestAccessToEntityType_completion_(entity_type, callback)

    def save_event(self, event, span, commit):
        success = self._ekeventstore.saveEvent_span_commit_error_(event._ekevent, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to save event")

    def remove_event(self, event, span, commit):
        success = self._ekeventstore.removeEvent_span_commit_error_(event._ekevent, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove event")

    def save_reminder(self, reminder, commit):
        success = self._ekeventstore.saveReminder_commit_error_(reminder._ekreminder, commit, objc.nil)
        if not success:
            raise Exception("Failed to save reminder")

    def remove_reminder(self, reminder, commit):
        success = self._ekeventstore.removeReminder_commit_error_(reminder._ekreminder, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove reminder")
' > $directory/ekeventstore.py

echo "Files created successfully in $directory"
