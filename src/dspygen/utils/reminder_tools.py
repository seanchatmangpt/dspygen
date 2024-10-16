import csv
import os
from pathlib import Path
from re import I
import subprocess
from typing import List, Dict, Any
import json

from pydantic import BaseModel, Field


current_lists = "id:E4A69F9A-BA15-4296-B217-9F735652A0FA, name:Self-care, id:B4B66208-A23D-4E10-B49A-36FF4DA3965A, name:Today, id:15DE35D7-37EF-4E2F-B271-57ADB4B71E18, name:Six Item List, id:378C4398-75DC-418F-B77C-558137394A66, name:Social Groups, id:93280B69-3D37-4FD4-91D0-83CFFD7D74E1, name:To Read List, id:129F5F6F-2749-4ECD-8983-C4A64400C6AE, name:New List 3, id:8CD4A536-5615-4C38-A3C3-FFA8F4BDAC8B, name:Test Reminders List"


def run_applescript(script: str) -> str:
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        raise RuntimeError(f"AppleScript Error: {error.decode('utf-8')}")
    
    return output.decode('utf-8').strip()


def get_all_lists() -> List[str]:
    script = '''
    tell application "Reminders"
        set allLists to lists
    end tell

    -- Output the lists
    allLists
    '''
    raw_output = run_applescript(script)
    list_ids = raw_output.split(", ")
    ids = [list_id.split(" ")[2] for list_id in list_ids]

    return ids


def get_all_list_names() -> str:
    script = '''
    tell application "Reminders"
        set allLists to every list
        set listInfo to {}
        repeat with aList in allLists
            set end of listInfo to {id:id of aList, name:name of aList}
        end repeat
    end tell
    return listInfo
    '''
    raw_output = run_applescript(script)
    return raw_output

def get_reminders_for_list_by_id(list_id: str) -> List[str]:
    script = f'''set listID to "{list_id}"

      tell application "Reminders"
          set targetList to first list whose id is listID
          set remindersInList to reminders of targetList
      end tell

      -- Output the reminders
      remindersInList
    '''
    raw_output = run_applescript(script)
    reminder_ids = raw_output.split(', ')
    ids = [reminder_id.split(' ')[2] for reminder_id in reminder_ids]

    return ids


def get_reminders_for_list_by_name(list_name: str) -> List[str]:
    script = f'''set listID to "{list_name}"

      tell application "Reminders"
          set targetList to first list whose name is listID
          set remindersInList to reminders of targetList
      end tell

      -- Output the reminders
      remindersInList
    '''
    raw_output = run_applescript(script)
    reminder_ids = raw_output.split(', ')
    ids = [reminder_id.split(' ')[2] for reminder_id in reminder_ids]

    return ids


class Reminder(BaseModel):
    id: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    body: str = Field(None, min_length=1, max_length=1000)
    due_date: str = Field(None, min_length=1, max_length=255)
    completed: bool = Field(False)


def get_reminder_by_id(reminder_id: str) -> Reminder:
    script = f'''
-- Extract the reminder ID from the URL
set reminderID to "{reminder_id}"

-- Use Reminders app to get the reminder data
tell application "Reminders"
    set theReminder to (first reminder whose id is reminderID)
    set reminderName to name of theReminder
    set reminderBody to body of theReminder
    set reminderDueDate to due date of theReminder
    set reminderCompleted to completed of theReminder
end tell

-- Convert the reminder data to a comma-separated list
set csvOutput to reminderID & ", " & ¬
                 reminderName & ", " & ¬
                 reminderBody & ", " & ¬
                 reminderDueDate & ", " & ¬
                 (reminderCompleted as string)

-- Output the comma-separated list
return csvOutput
''' 
    raw_output = run_applescript(script)
    reminder_data = raw_output.split(", ")
    instance = Reminder(id=reminder_data[0], name=reminder_data[1], body=reminder_data[2], due_date=reminder_data[3], completed=reminder_data[4])
    return instance


def create_reminders_tsv():
    script = f'''-- Get the current date and time for versioning
set currentDate to current date
set formattedDate to (year of currentDate) & "-" & text -2 through -1 of ("0" & (month of currentDate as integer)) & "-" & text -2 through -1 of ("0" & day of currentDate) & "_" & text -2 through -1 of ("0" & hours of currentDate) & "-" & text -2 through -1 of ("0" & minutes of currentDate) & "-" & text -2 through -1 of ("0" & seconds of currentDate)

-- Specify the file path for the TSV with versioning
set desktopPath to (path to desktop as text)
set filePath to desktopPath & "Reminders_" & formattedDate & ".tsv"

-- Open the TSV file for writing
set fileID to open for access (POSIX path of filePath) with write permission
set eof of fileID to 0 -- Clear existing file content

-- Write the TSV header
write "ID" & tab & "List" & tab & "Title" & tab & "Due Date" & tab & "Completed" & tab & "Completion Date" & tab & "Priority" & tab & "Notes" & linefeed to fileID

-- Get all reminders lists
tell application "Reminders"
    set reminderLists to lists
    repeat with aList in reminderLists
        set listName to name of aList
        set remindersList to reminders of aList
        
        repeat with aReminder in remindersList
            -- Extract reminder details
            set reminderID to "x-apple-reminder://" & id of aReminder
            set reminderTitle to name of aReminder
            set reminderDueDate to due date of aReminder
            set reminderCompleted to completed of aReminder
            set reminderCompletionDate to completion date of aReminder
            set reminderPriority to priority of aReminder
            set reminderNotes to body of aReminder
            
            -- Handle potential missing values
            if reminderDueDate is missing value then
                set reminderDueDate to ""
            else
                set reminderDueDate to reminderDueDate as string
            end if
            
            if reminderCompletionDate is missing value then
                set reminderCompletionDate to ""
            else
                set reminderCompletionDate to reminderCompletionDate as string
            end if
            
            if reminderNotes is missing value then
                set reminderNotes to ""
            end if
            
            -- Write reminder details to TSV
            write (reminderID & tab & listName & tab & reminderTitle & tab & reminderDueDate & tab & reminderCompleted & tab & reminderCompletionDate & tab & reminderPriority & tab & reminderNotes) & linefeed to fileID
        end repeat
    end repeat
end tell

-- Close the file
close access fileID

-- Notify user of completion
display notification "Reminders exported to TSV successfully!" with title "Export Complete"
'''


def tsv_to_csv(tsv_filepath):
    """Converts a TSV file to a CSV file."""
    csv_filepath = tsv_filepath.with_suffix('.csv')

    with open(tsv_filepath, 'r') as tsvfile, open(csv_filepath, 'w', newline='') as csvfile:
        tsv_reader = csv.reader(tsvfile, delimiter='\t')
        csv_writer = csv.writer(csvfile)

        for row in tsv_reader:
            csv_writer.writerow(row)

    print(f"CSV file saved as {csv_filepath}")


def get_latest_file(directory, extension):
    """Gets the latest file with the given extensions from the specified directory."""
    files = list(Path(directory).glob(f"*{extension}"))
    if not files:
        raise FileNotFoundError(f"No files with extensions {extension} found in {directory}")
    latest_file = max(files, key=os.path.getctime)
    return latest_file


import EventKit
import objc

store = EventKit.EKEventStore.new()


# Request access to Reminders
def request_access():
    granted, error = objc.var(True), objc.var(None)
    
    def handler(granted_local, error_local):
        granted.assign(granted_local)
        error.assign(error_local)
    
    store.requestAccessToEntityType_completion(EventKit.EKEntityTypeReminder, handler)
    if not granted.value:
        raise PermissionError("Access to reminders was not granted")

# Fetch and list all reminder lists
def list_reminder_lists():
    calendars = store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)

    for calendar in calendars:
        print(f"List Name: {calendar}")


def fetch_reminders():
    predicate = store.predicateForRemindersInCalendars_(None)
    reminders = store.remindersMatchingPredicate_(predicate)

    for reminder in reminders:
        print(reminder)
        print(f"Title: {reminder.title()}")
        try:
            print(f"Due Date: {reminder.dueDateComponents().date()}")
        except Exception as e:
            print(f"Error: {e}")  

    list_reminder_lists()


def main():
    """Main function"""
    # from dspygen.utils.dspy_tools import init_ol
    # init_ol()
    # list_id = get_all_lists()[0]
    # reminder_id = get_reminders_for_list_by_id(list_id)[0]
    # print(get_reminder_by_id(reminder_id))
    # # print(get_all_list_names())
    # print(get_reminders_for_list_by_name("Today"))
    fetch_reminders()


if __name__ == '__main__':
    main()
