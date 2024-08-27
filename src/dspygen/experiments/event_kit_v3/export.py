#!/usr/bin/env python3
"""
This script exports all events from all calendars to a CSV file named 'events_export.csv'.

Usage:
    python export_events.py
"""

import csv
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

    def fetch_events(self, start_date, end_date, calendars=None):
        """Fetches events within a specific date range."""
        predicate = self.inst.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date,
                                                                                 calendars or objc.nil)
        return self.inst.eventsMatchingPredicate_(predicate)


def export_events_to_csv(store, filename="events_export.csv"):
    """Exports all events from all calendars to a CSV file."""

    # Define the date range: start from today to one year in the future
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)

    # Fetch all event calendars
    calendars = store.get_all_event_calendars()

    # Fetch events from all calendars
    events = store.fetch_events(start_date, end_date, calendars)

    # Define the fields to be exported
    field_names = ["Calendar", "Title", "Start Date", "End Date", "Location", "Notes"]

    # Write events to CSV
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(field_names)

        for event in events:
            writer.writerow([
                event.calendar().title(),  # Calendar name
                event.title(),  # Event title
                event.startDate(),  # Start date
                event.endDate(),  # End date
                event.location() or "",  # Location
                event.notes() or "",  # Notes
            ])

    print(f"Exported {len(events)} events to {filename}")


def main():
    store = EventStore()

    # Request access to the calendar events
    store.request_access_and_handle(EventKit.EKEntityTypeEvent)

    # Export events to CSV
    export_events_to_csv(store)


if __name__ == '__main__':
    main()
