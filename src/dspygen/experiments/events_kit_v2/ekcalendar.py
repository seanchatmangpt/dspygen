import EventKit

from dspygen.experiments.events_kit_v2.ekeventstore import EventStore
from dspygen.experiments.events_kit_v2.ekobject import EKObject


class Calendar(EKObject):
    def __init__(self, inst):
        super().__init__(inst)

    @property
    def title(self):
        """Get or set the calendar's title."""
        return self.inst.title

    @title.setter
    def title(self, value):
        self.inst.title = value

    @property
    def type(self):
        """Get the type of the calendar."""
        return self.inst.type

    @property
    def calendar_identifier(self):
        """Get the calendar's unique identifier."""
        return self.inst.calendarIdentifier

    @property
    def allows_content_modifications(self):
        """Check if the calendar allows content modifications."""
        return self.inst.allowsContentModifications

    @property
    def color(self):
        """Get or set the calendar's color."""
        return self.inst.color

    @color.setter
    def color(self, value):
        self.inst.color = value

    @property
    def source(self):
        """Get the source of the calendar."""
        return self.inst.source

    @property
    def events(self):
        """Fetch all events in this calendar."""
        # You would typically need to specify a date range for fetching events
        return self.inst.events

    def add_event(self, event):
        """Add an event to the calendar."""
        event.calendar = self.inst

    def remove_event(self, event, span=EventKit.EKSpanThisEvent, commit=True):
        """Remove an event from the calendar."""
        store = EventStore()
        store.remove_event(event, span, commit)

    def save(self):
        """Save the calendar."""
        store = EventStore()
        store.save_calendar(self)

    def remove(self):
        """Remove the calendar."""
        store = EventStore()
        store.remove_calendar(self)

    @staticmethod
    def create_new(title, source):
        """Create a new calendar with the specified title and source."""
        new_calendar = EventKit.EKCalendar.calendarForEntityType_eventStore_(EventKit.EKEntityTypeEvent, EventStore().inst)
        new_calendar.title = title
        new_calendar.source = source
        return Calendar(new_calendar)

    @classmethod
    def get_calendar_by_name(cls, name, entity_type=EventKit.EKEntityTypeEvent):
        """Fetches a calendar by its name."""
        calendars = self.inst.calendarsForEntityType_(entity_type)
        for calendar in calendars:
            if calendar.title == name:
                return Calendar(calendar)
        raise Exception(f"Calendar with name '{name}' not found")


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    print(Calendar.get_calendar_by_name("Today", EventKit.EKEntityTypeReminder))

if __name__ == '__main__':
    main()
