import threading
import EventKit
from typing import List, Optional
import inject

from dspygen.pyautomator.event_kit.calendar_event import CalendarEvent


class CalendarEventList:
    @inject.autoparams()
    def __init__(self, name: str, event_store: EventKit.EKEventStore):
        self.name = name
        self.event_store = event_store
        self.ek_calendar = None
        self._load_ek_calendar()

    def _load_ek_calendar(self):
        calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeEvent)
        for calendar in calendars:
            if calendar.title() == self.name:
                self.ek_calendar = calendar
                break
        if not self.ek_calendar:
            raise ValueError(f"Calendar '{self.name}' not found")

    def get_calendar(self):
        return self.ek_calendar

    def get_all_events(self) -> List[CalendarEvent]:
        """Fetch all events in this calendar."""
        predicate = self.event_store.predicateForEventsWithStartDate_endDate_calendars_(
            EventKit.NSDate.distantPast(),
            EventKit.NSDate.distantFuture(),
            [self.ek_calendar]
        )
        ek_events = self.event_store.eventsMatchingPredicate_(predicate)
        return [CalendarEvent(self.event_store, ek_event) for ek_event in ek_events]

@inject.autoparams()
def main(event_store: EventKit.EKEventStore):
    try:
        # Request access to calendar
        access_granted = [False]

        def request_access_callback(granted, error):
            if not granted:
                print(f"Access to calendar denied. Error: {error}")
            else:
                access_granted[0] = True

        event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, request_access_callback)

        # Wait for access to be granted
        import time
        timeout = 5
        while not access_granted[0] and timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5

        if not access_granted[0]:
            raise PermissionError("Access to calendar not granted in time.")

        # Get the default calendar
        default_calendar = event_store.defaultCalendarForNewEvents()
        calendar_list = CalendarEventList(default_calendar.title(), event_store)
        print(f"Using calendar: {calendar_list.name}")

        # Test get_all_events
        all_events = calendar_list.get_all_events()
        print(f"Fetched {len(all_events)} events from the calendar")
        for event in all_events:
            print(f"Event: {event.title} - Start: {event.start_date}")

        # Debug: Print all calendars
        calendars = event_store.calendarsForEntityType_(EventKit.EKEntityTypeEvent)
        print(f"Total calendars: {len(calendars)}")
        for calendar in calendars:
            print(f"Calendar: {calendar.title()}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()