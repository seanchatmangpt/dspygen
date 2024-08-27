from datetime import datetime, timedelta

import objc
import EventKit


class EventStore:
    def __init__(self):
        self.inst = EventKit.EKEventStore.new()

    def request_access(self, entity_type, callback):
        """Requests access to the specified entity type (e.g., events or reminders)."""
        self.inst.requestAccessToEntityType_completion_(entity_type, callback)

    def request_access_and_handle(self, entity_type):
        """Requests access and handles the response with a default callback."""
        def access_callback(granted, error):
            if granted:
                print("Access granted.")
            else:
                print(f"Access denied. Error: {error}")
        self.request_access(entity_type, access_callback)

    def get_all_event_calendars(self):
        """Fetches all event calendars available."""
        return self.inst.calendarsForEntityType_(EventKit.EKEntityTypeEvent)

    def save_event(self, event, span=EventKit.EKSpanThisEvent, commit=True):
        """Saves an event to the calendar."""
        success = self.inst.saveEvent_span_commit_error_(event.inst, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to save event")

    def remove_event(self, event, span=EventKit.EKSpanThisEvent, commit=True):
        """Removes an event from the calendar."""
        success = self.inst.removeEvent_span_commit_error_(event.inst, span, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove event")

    def save_reminder(self, reminder, commit=True):
        """Saves a reminder to the reminders list."""
        success = self.inst.saveReminder_commit_error_(reminder.inst, commit, objc.nil)
        if not success:
            raise Exception("Failed to save reminder")

    def remove_reminder(self, reminder, commit=True):
        """Removes a reminder from the reminders list."""
        success = self.inst.removeReminder_commit_error_(reminder.inst, commit, objc.nil)
        if not success:
            raise Exception("Failed to remove reminder")

    def get_event(self, identifier):
        """Fetches an event by its identifier."""
        event = self.inst.eventWithIdentifier_(identifier)
        if event:
            return event
        else:
            raise Exception("Event not found")

    def get_reminder(self, identifier):
        """Fetches a reminder by its identifier."""
        reminder = self.inst.calendarItemWithIdentifier_(identifier)
        if reminder and isinstance(reminder, EventKit.EKReminder):
            return reminder
        else:
            raise Exception("Reminder not found")

    def get_all_reminder_lists(self):
        """Fetches all reminder lists (calendars) available."""
        return self.inst.calendarsForEntityType_(EventKit.EKEntityTypeReminder)

    def fetch_events(self, start_date, end_date, calendars=None):
        """Fetches events within a specific date range."""
        predicate = self.inst.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, calendars or objc.nil)
        return self.inst.eventsMatchingPredicate_(predicate)

    def fetch_reminders(self, calendars=None):
        """Fetches reminders in the specified calendars."""
        predicate = self.inst.predicateForRemindersInCalendars_(calendars or objc.nil)
        def reminders_callback(reminders):
            return reminders

        self.inst.fetchRemindersMatchingPredicate_completion_(predicate, reminders_callback)

    def modify_event(self, event, **kwargs):
        """Modifies an existing event."""
        for key, value in kwargs.items():
            setattr(event, key, value)
        self.save_event(event)

    def modify_reminder(self, reminder, **kwargs):
        """Modifies an existing reminder."""
        for key, value in kwargs.items():
            setattr(reminder, key, value)
        self.save_reminder(reminder)

    def reset(self):
        """Resets the event store to clear any cached data."""
        self.inst.reset()

    def save_events(self, events, span=EventKit.EKSpanThisEvent, commit=True):
        """Saves multiple events."""
        for event in events:
            self.save_event(event, span, commit)

    def remove_events(self, events, span=EventKit.EKSpanThisEvent, commit=True):
        """Removes multiple events."""
        for event in events:
            self.remove_event(event, span, commit)

    def save_reminders(self, reminders, commit=True):
        """Saves multiple reminders."""
        for reminder in reminders:
            self.save_reminder(reminder, commit)

    def remove_reminders(self, reminders, commit=True):
        """Removes multiple reminders."""
        for reminder in reminders:
            self.remove_reminder(reminder, commit)

def main():
    store = EventStore()

    # Get all event calendars
    lists = store.get_all_reminder_lists()
    print(lists)




if __name__ == '__main__':
    main()
