import objc
from Foundation import NSObject
from ekobject import EKObject
import EventKit

class EKReminder(EKObject):
    def __init__(self, event_store):
        super().__init__()
        self.inst = EventKit.EKReminder.reminderWithEventStore_(event_store)

    @property
    def title(self):
        return self.inst.title()

    @title.setter
    def title(self, value):
        self.inst.setTitle_(value)

    @property
    def calendar(self):
        return self.inst.calendar()

    @calendar.setter
    def calendar(self, value):
        self.inst.setCalendar_(value)

    @property
    def start_date_components(self):
        return self.inst.startDateComponents()

    @start_date_components.setter
    def start_date_components(self, value):
        self.inst.setStartDateComponents_(value)

    @property
    def due_date_components(self):
        return self.inst.dueDateComponents()

    @due_date_components.setter
    def due_date_components(self, value):
        self.inst.setDueDateComponents_(value)

    @property
    def completed(self):
        return self.inst.completed()

    @completed.setter
    def completed(self, value):
        self.inst.setCompleted_(value)

    def save_reminder(self, event_store, commit):
        success = event_store.saveReminder_commit_error_(self.inst, commit, objc.nil)
        if not success:
            raise Exception("Failed to save reminder")

    def remove_reminder(self, event_store, commit):
        success = event_store.removeReminder_commit_error_(self.inst, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove reminder")

