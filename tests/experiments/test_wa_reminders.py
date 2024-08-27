import pytest
from typer.testing import CliRunner
import subprocess
import csv
import tempfile
import os
import pyperclip

from dspygen.experiments.wa_reminders import app, import_reminders_from_file, import_reminders_from_clipboard

runner = CliRunner()

def run_applescript(script):
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise Exception(f"AppleScript Error: {error.decode('utf-8')}")
    return output.decode('utf-8').strip()

def clear_reminders(list_name):
    script = f'''
    tell application "Reminders"
        if not (exists list "{list_name}") then
            make new list with properties {{name:"{list_name}"}}
        end if
        delete every reminder of list "{list_name}"
    end tell
    '''
    run_applescript(script)

def get_reminders(list_name):
    script = f'''
    tell application "Reminders"
        if not (exists list "{list_name}") then
            make new list with properties {{name:"{list_name}"}}
        end if
        set reminderList to list "{list_name}"
        set reminderNames to name of every reminder in reminderList
        return reminderNames
    end tell
    '''
    return run_applescript(script).split(", ")

@pytest.fixture(scope="function")
def temp_csv_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(['title', 'notes', 'due_date'])
        writer.writerow(['Test Reminder 1', 'Test Notes 1', '2023-05-01'])
        writer.writerow(['Test Reminder 2', 'Test Notes 2', '2023-05-02'])
    yield temp_file.name
    os.unlink(temp_file.name)

@pytest.fixture(scope="function")
def clean_test_list():
    list_name = "Test Reminders List"
    clear_reminders(list_name)
    yield list_name
    clear_reminders(list_name)

def test_import_reminders(temp_csv_file, clean_test_list):
    result = runner.invoke(app, ['import-reminders', temp_csv_file, '--list-name', clean_test_list])
    assert result.exit_code == 0
    assert "Successfully imported 2 reminders." in result.stdout

    reminders = get_reminders(clean_test_list)
    assert "Test Reminder 1" in reminders
    assert "Test Reminder 2" in reminders

def test_import_from_clipboard(clean_test_list):
    csv_data = "title,notes,due_date\nClipboard Reminder,Clipboard Notes,2023-05-03"
    pyperclip.copy(csv_data)

    result = runner.invoke(app, ['import-from-clipboard', '--list-name', clean_test_list])
    assert result.exit_code == 0
    assert "Successfully imported 1 reminders from clipboard." in result.stdout

    reminders = get_reminders(clean_test_list)
    assert "Clipboard Reminder" in reminders

def test_import_reminders_file_not_found():
    result = runner.invoke(app, ['import-reminders', 'non_existent_file.csv'])
    assert result.exit_code != 0

def test_import_reminders_invalid_csv(temp_csv_file, clean_test_list):
    with open(temp_csv_file, 'w') as f:
        f.write("invalid,csv,data\n1,2,3")

    result = runner.invoke(app, ['import-reminders', temp_csv_file, '--list-name', clean_test_list])
    assert result.exit_code != 0

def test_import_from_clipboard_invalid_csv(clean_test_list):
    invalid_csv_data = "invalid,csv,data\n1,2,3"
    pyperclip.copy(invalid_csv_data)

    result = runner.invoke(app, ['import-from-clipboard', '--list-name', clean_test_list])
    assert result.exit_code != 0

# Add new tests for the core functions if needed
def test_import_reminders_from_file(temp_csv_file, clean_test_list):
    reminders = import_reminders_from_file(temp_csv_file, clean_test_list)
    assert len(reminders) == 2
    assert reminders[0].title == "Test Reminder 1"
    assert reminders[1].title == "Test Reminder 2"

def test_import_reminders_from_clipboard(clean_test_list):
    csv_data = "title,notes,due_date\nClipboard Reminder,Clipboard Notes,2023-05-03"
    pyperclip.copy(csv_data)
    reminders = import_reminders_from_clipboard(clean_test_list)
    assert len(reminders) == 1
    assert reminders[0].title == "Clipboard Reminder"