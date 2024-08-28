import inject
import EventKit
from datetime import datetime, timedelta
from typing import List, Optional
from icalendar import Calendar
import logging
import tempfile
import os
import pandas as pd
import csv  # Add this import

from dspygen.modules.generate_icalendar_module import generate_i_calendar_call
from dspygen.rm.data_retriever import DataRetriever
from dspygen.modules.df_sql_module import dfsql_call

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CalendarApp:
    @inject.autoparams()
    def __init__(self, event_store: EventKit.EKEventStore):
        self.event_store = event_store
        self.default_calendar = self.event_store.defaultCalendarForNewEvents()

    def request_access(self):
        """Request access to calendar."""
        def callback(granted, error):
            if not granted:
                raise PermissionError("Access to calendar denied.")

        self.event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, callback)

    def create_event_from_generated(self, prompt: str) -> str:
        """Generate iCalendar data from a prompt and return it for manual addition."""
        ical_string = generate_i_calendar_call(prompt)
        
        logger.info("Generated iCalendar text:")
        logger.info(ical_string)
        
        # Save the iCalendar data to a file for inspection
        with open('generated_event.ics', 'w') as f:
            f.write(ical_string)
        logger.info("iCalendar content saved to 'generated_event.ics'")
        
        # Validate the iCalendar string
        self._validate_ical(ical_string)
        
        return f"Event data generated from prompt: {prompt}\n\niCalendar data:\n{ical_string}"

    def _validate_ical(self, ical_string: str):
        """Validate the iCalendar string."""
        try:
            cal = Calendar.from_ical(ical_string)
            events = list(cal.walk('VEVENT'))
            if not events:
                raise ValueError("No VEVENT component found in the iCalendar data")
            logger.info("iCalendar data validated successfully")
        except Exception as e:
            logger.error(f"Invalid iCalendar data: {e}")
            raise

    def get_events(self, start_date: datetime, end_date: datetime) -> List[dict]:
        """Get events within a date range."""
        predicate = self.event_store.predicateForEventsWithStartDate_endDate_calendars_(
            start_date, end_date, [self.default_calendar]
        )
        events = self.event_store.eventsMatchingPredicate_(predicate)
        return [self._event_to_dict(event) for event in events]

    def _event_to_dict(self, event: EventKit.EKEvent) -> dict:
        """Convert an EKEvent to a dictionary."""
        attendees = event.attendees()
        return {
            'id': event.eventIdentifier(),
            'title': event.title(),
            'start_date': event.startDate(),
            'end_date': event.endDate(),
            'location': event.location(),
            'notes': event.notes(),
            'attendees': [attendee.name() for attendee in attendees] if attendees else [],
            'organizer': event.organizer().name() if event.organizer() else None,
        }

    def query(self, query: str) -> List[dict]:
        """Perform an advanced search using SQL query and return a list of event dictionaries."""
        data_retriever = DataRetriever(file_path=self.export_events())

        results = data_retriever.forward(query=query)
        
        events = []
        for row in results:
            event = self.event_store.eventWithIdentifier_(row['ID'])
            if event:
                events.append(self._event_to_dict(event))

        return events

    def text_query(self, text: str) -> List[dict]:
        """Perform a natural language query and return a list of event dictionaries."""
        csv_file = self.export_events()
        
        df = pd.read_csv(csv_file)
        
        df_schema = df.columns.tolist()
        df_data = df.values.tolist()
        
        sql_query = dfsql_call(text=text, df_schema=df_schema, df_data=df_data)
        
        events = self.query(sql_query)
        
        os.unlink(csv_file)
        
        return events

    def export_events(self, filename=None, days=30) -> str:
        if filename is None:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
                filename = temp_file.name

        end_date = datetime.now() + timedelta(days=days)
        events = self.get_events(datetime.now(), end_date)

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Title', 'Start Date', 'End Date', 'Location', 'Notes', 'Attendees', 'Organizer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for event in events:
                writer.writerow({
                    'ID': event['id'],
                    'Title': event['title'],
                    'Start Date': event['start_date'],
                    'End Date': event['end_date'],
                    'Location': event['location'],
                    'Notes': event['notes'],
                    'Attendees': ', '.join(event['attendees']),
                    'Organizer': event['organizer']
                })

        logger.info(f"Events exported to: {filename}")
        return filename
