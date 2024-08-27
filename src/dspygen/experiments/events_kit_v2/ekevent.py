import objc
from ekobject import EKObject

class EKEvent(EKObject):
    def __init__(self, event_store):
        super().__init__()
        EventKit = objc.importFramework("EventKit")
        self.inst = EventKit.EKEvent.eventWithEventStore_(event_store)

    @property
    def title(self):
        return self.inst.title()

    @title.setter
    def title(self, value):
        self.inst.setTitle_(value)

    @property
    def start_date(self):
        return self.inst.startDate()

    @start_date.setter
    def start_date(self, value):
        self.inst.setStartDate_(value)

    @property
    def end_date(self):
        return self.inst.endDate()

    @end_date.setter
    def end_date(self, value):
        self.inst.setEndDate_(value)

    @property
    def calendar(self):
        return self.inst.calendar()

    @calendar.setter
    def calendar(self, value):
        self.inst.setCalendar_(value)

    @property
    def alarms(self):
        return self.inst.alarms()

    @alarms.setter
    def alarms(self, value):
        self.inst.setAlarms_(value)

    @property
    def recurrence_rules(self):
        return self.inst.recurrenceRules()

    @recurrence_rules.setter
    def recurrence_rules(self, value):
        self.inst.setRecurrenceRules_(value)

    def save_event(self, event_store, span, commit):
        success = event_store.saveEvent_span_commit_error_(self.inst, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to save event")

    def remove_event(self, event_store, span, commit):
        success = event_store.removeEvent_span_commit_error_(self.inst, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove event")

