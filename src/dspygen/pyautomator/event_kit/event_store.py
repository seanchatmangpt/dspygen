#!/usr/bin/env python3
"""
This script exports all events from all calendars to a CSV file named 'events_export.csv'.

Usage:
    python export_events.py
"""

import csv
from datetime import datetime, timedelta

import inject
import objc
import EventKit


class EventStore:
    @inject.autoparams()
    def __init__(self, event_store: EventKit.EKEventStore):
        self.instance = event_store

    def request_access(self, entity_type, callback):
        """Requests access to the specified entity type (e.g., events or reminders)."""
        self.instance.requestAccessToEntityType_completion_(entity_type, callback)

    def request_access_and_handle_event(self):
        """Requests access and handles the response with a default callback for events."""
        def access_callback(granted, error):
            if granted:
                print("Access granted for events.")
            else:
                print(f"Access denied for events. Error: {error}")
        self.request_access(EventKit.EKEntityTypeEvent, access_callback)

    def request_access_and_handle_reminder(self):
        """Requests access and handles the response with a default callback for reminders."""
        def access_callback(granted, error):
            if granted:
                print("Access granted for reminders.")
            else:
                print(f"Access denied for reminders. Error: {error}")
        self.request_access(EventKit.EKEntityTypeReminder, access_callback)

    def get_all_calendars_event(self):
        """Fetches all event calendars available."""
        return self.instance.calendarsForEntityType_(EventKit.EKEntityTypeEvent)

    def get_all_calendars_reminder(self):
        """Fetches all reminder calendars available."""
        return self.instance.calendarsForEntityType_(EventKit.EKEntityTypeReminder)

    def fetch_items_event(self, start_date, end_date, calendars):
        """Fetches events within a specific date range."""
        predicate = self.instance.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date,
                                                                                     calendars or objc.nil)
        return self.instance.eventsMatchingPredicate_(predicate)

    def fetch_items_reminder(self, start_date, end_date, calendars):
        """Fetches reminders within a specific date range and those without a due date."""
        # Fetch all reminders, including completed ones
        predicate = self.instance.predicateForRemindersInCalendars_(calendars or objc.nil)
        reminders = self.instance.remindersMatchingPredicate_(predicate)
        
        # Filter reminders based on due date or include if no due date
        filtered_reminders = [
            reminder for reminder in reminders
            if not reminder.dueDate() or start_date <= reminder.dueDate() <= end_date
        ]
        
        print(f"Total reminders: {len(reminders)}")
        print(f"Filtered reminders: {len(filtered_reminders)}")
        
        return filtered_reminders

    def export_items_to_csv_event(self, filename, days=14):
        """Exports all events from all calendars to a CSV file."""
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        calendars = self.get_all_calendars_event()
        events = self.fetch_items_event(start_date, end_date, calendars)

        field_names = ["ID", "Calendar", "Title", "StartDate", "EndDate", "Location", "Notes"]

        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            for event in events:
                writer.writerow([
                    event.calendarItemIdentifier(),  # Event ID
                    event.calendar().title(),  # Calendar name
                    event.title(),  # Event title
                    event.startDate(),  # Start date
                    event.endDate(),  # End date
                    event.location() or "",  # Location
                    event.notes() or "",  # Notes
                ])
        print(f"Exported {len(events)} events to {filename}")

    def export_items_to_csv_reminder(self, filename, days=7):
        """Exports reminders from all calendars to a CSV file."""
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        calendars = self.get_all_calendars_reminder()
        reminders = self.fetch_items_reminder(start_date, end_date, calendars)

        field_names = ["ID", "Calendar", "Title", "DueDate", "Priority", "Completed", "Notes"]

        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            today = datetime.now().date()
            for reminder in reminders:
                writer.writerow([
                    reminder.calendarItemIdentifier(),  # Reminder ID
                    reminder.calendar().title(),
                    reminder.title(),
                    reminder.dueDate() if reminder.dueDate() else today,  # Use today's date if no due date
                    reminder.priority(),
                    1 if reminder.isCompleted() else 0,  # Use 1 for completed, 0 for not completed
                    reminder.notes() or "",
                ])
        print(f"Exported {len(reminders)} reminders to {filename}")


def main():
    store = EventStore(event_store=EventKit.EKEventStore.alloc().init())

    # Request access for both events and reminders
    store.request_access_and_handle_event()
    store.request_access_and_handle_reminder()

    # Export events to CSV (7 days by default)
    store.export_items_to_csv_event(store, "events_export.csv")

    # Export reminders to CSV (7 days by default)
    store.export_items_to_csv_reminder(store, "reminders_export.csv")

if __name__ == '__main__':
    main()
