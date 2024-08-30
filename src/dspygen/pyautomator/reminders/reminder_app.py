import inject
import EventKit
from typing import List, Optional
import tempfile
import os
import csv
import pandas as pd

from dspygen.pyautomator.base_app import BaseApp
from dspygen.pyautomator.event_kit.event_store import EventStore
from dspygen.pyautomator.event_kit.reminder import Reminder
from dspygen.pyautomator.event_kit.reminder_list import ReminderList
from dspygen.rm.data_retriever import DataRetriever
from datetime import datetime, timedelta
from dspygen.modules.df_sql_module import dfsql_call
from dspygen.modules.generate_icalendar_module import generate_i_calendar_call


class RemindersApp(BaseApp):
    @inject.autoparams()
    def __init__(self, event_store: EventKit.EKEventStore):
        super().__init__("Reminders")
        self.event_store = event_store
        self.lists: List[ReminderList] = []
        self._load_existing_lists()

    def _load_existing_lists(self):
        calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        for calendar in calendars:
            self.lists.append(ReminderList(calendar.title(), self.event_store))

    def request_access(self):
        """Request access to reminders."""

        def callback(granted, error):
            if not granted:
                raise PermissionError("Access to reminders denied.")

        self.event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, callback)

    def get_list(self, name: str) -> Optional[ReminderList]:
        """Get a reminder list by name."""
        for lst in self.lists:
            if lst.name == name:
                return lst
        return None

    def get_all_lists(self) -> List[str]:
        """Get names of all reminder lists."""
        return [lst.name for lst in self.lists]

    def query(self, query: str) -> List[Reminder]:
        """Perform an advanced search using SQL query and return a list of Reminder objects."""
        data_retriever = DataRetriever(file_path=self.export_reminders())

        results = data_retriever.forward(query=query)

        reminders = []
        for row in results:
            reminder = Reminder.from_id(self.event_store, row['ID'])
            if reminder:
                reminders.append(reminder)

        return reminders

    def text_query(self, text: str) -> List[Reminder]:
        """Perform a natural language query and return a list of Reminder objects."""
        # Export reminders to a temporary CSV file
        csv_file = self.export_reminders()

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Get the DataFrame schema and data
        df_schema = df.columns.tolist()
        df_data = df.values.tolist()

        # Use DFSQLModule to convert natural language to SQL
        sql_query = dfsql_call(text=text, df_schema=df_schema, df_data=df_data)

        # Use the generated SQL query to fetch reminders
        reminders = self.query(sql_query)

        # Clean up the temporary CSV file
        os.unlink(csv_file)

        return reminders

    def export_reminders(self, filename=None, days=7) -> str:
        if filename is None:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
                filename = temp_file.name

        store = EventStore()
        store.export_items_to_csv_reminder(filename, days)

        print(f"Reminders exported to: {filename}")
        return filename

    def create_reminder_from_generated(self, prompt: str, list_name: str) -> Reminder:
        """Generate a reminder from a prompt and add it to the specified list."""
        reminder_list = self.get_list(list_name)
        if not reminder_list:
            raise ValueError(f"Reminder list '{list_name}' not found")

        # Generate iCalendar data from the prompt
        ical_string = generate_i_calendar_call(prompt)

        # Create the reminder using the generated iCalendar data
        reminder = Reminder.create_from_rfc5545(self.event_store, ical_string, reminder_list.ek_calendar)
        return reminder


def main():
    app = RemindersApp()
    app.request_access()

    try:
        # Test creating a reminder from generated data
        prompt = "Create a reminder to buy groceries tomorrow at 5 PM"
        list_name = app.get_all_lists()[0]  # Use the first available list
        new_reminder = app.create_reminder_from_generated(prompt, list_name)
        print(f"Created new reminder: {new_reminder}")

        # Test get_all_lists
        print("Existing lists:", app.get_all_lists())

        # Test get_list
        list_name = app.get_all_lists()[0] if app.get_all_lists() else "Test List"
        reminder_list = app.get_list(list_name)
        print(f"Got list '{list_name}': {reminder_list is not None}")

        # Test creating a new list
        new_list_name = "New Test List"
        new_list = ReminderList(new_list_name, app.event_store)
        app.lists.append(new_list)
        print(f"Created new list: {new_list_name}")

        # Verify the new list was added
        print("Updated lists:", app.get_all_lists())

        # Test get_list with the new list
        retrieved_list = app.get_list(new_list_name)
        print(f"Retrieved new list: {retrieved_list is not None}")

        # Test advanced search
        search_results = app.query("SELECT * FROM df WHERE Calendar = 'Health & Wellness'")
        print("Advanced search results:")
        for reminder in search_results:
            print(f"- {reminder.title} (Due: {reminder.due_date})")

        # Test export
        export_file = app.export_reminders()
        print(f"Reminders exported to: {export_file}")

        # Optionally, you can read and print the contents of the exported file
        with open(export_file, 'r') as f:
            print("Exported data:")
            print(f.read())

    finally:
        # Clean up: Delete the created list
        if new_list:
            app.event_store.removeCalendar_commit_error_(new_list.ek_calendar, True, None)
            app.lists.remove(new_list)
            print(f"Deleted list: {new_list.name}")

        # Clean up temporary file if it was created
        if app.data_retriever:
            os.unlink(app.data_retriever.file_path)

        # Remove the exported file if it was created
        if 'export_file' in locals():
            os.unlink(export_file)
            print(f"Deleted exported file: {export_file}")

        # Verify the list was removed
        print("Final lists:", app.get_all_lists())


def main2():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()
    app = RemindersApp()

    # Test natural language query
    # search_results = app.text_query("Find all reminders")
    search_results = app.text_query("Find reminders related to health and wellness")
    print("Natural language query results:")
    for reminder in search_results:
        print(reminder)


if __name__ == "__main__":
    main2()
    # main()
