import pytest
import os
from dspygen.modules.create_row_module import create_row_call
from dspygen.utils.dspy_tools import init_dspy
from dspygen.pyautomator.reminders.reminder_app import RemindersApp
from dspygen.rm.data_retriever import DataRetriever

@pytest.fixture
def setup_dspy():
    init_dspy()

@pytest.fixture
def reminders_app():
    app = RemindersApp()
    app.request_access()
    return app

@pytest.fixture
def csv_file(reminders_app):
    csv_path = reminders_app.export_reminders()
    yield csv_path
    os.remove(csv_path)  # Clean up the file after the test

def test_create_row_integration(setup_dspy, reminders_app, csv_file):
    # Load the initial data
    data_retriever = DataRetriever(file_path=csv_file)
    initial_data = data_retriever.forward()

    # Prepare the request
    request = "Add a new task to buy groceries for the weekend, due on 2024-09-05, with high priority to Today"

    # Call the create_row_call function
    updated_data = create_row_call(data=initial_data, request=request)

    # Assertions
    assert len(updated_data) == len(initial_data) + 1
    new_row = updated_data[-1]
    assert new_row['Title'] == 'Buy groceries for the weekend'
    assert new_row['DueDate'] == '2024-09-05'
    assert 'ID' in new_row  # Ensure an ID is generated
    assert new_row['Calendar'] == 'Today'  # Assuming new tasks are added to 'Today' calendar


def test_create_row_with_notes(setup_dspy, reminders_app, csv_file):
    data_retriever = DataRetriever(file_path=csv_file)
    initial_data = data_retriever.forward()

    request = "Add a task to call Alice about the project meeting, due tomorrow, medium priority, and add a note to prepare agenda items"

    updated_data = create_row_call(data=initial_data, request=request)

    new_row = updated_data[-1]
    assert new_row['Title'] == 'Call Alice about the project meeting'
    assert 'prepare agenda items' in new_row['Notes'].lower()

    # Verify the new reminder is added to the app
    new_reminders = reminders_app.text_query("Find reminders about calling Alice")
    assert len(new_reminders) > 0
    assert any(r.title == 'Call Alice about the project meeting' for r in new_reminders)

def test_create_row_with_existing_calendar(setup_dspy, reminders_app, csv_file):
    data_retriever = DataRetriever(file_path=csv_file)
    initial_data = data_retriever.forward()

    request = "Add a new health task to drink more water, due in 3 days, low priority"

    updated_data = create_row_call(data=initial_data, request=request)

    new_row = updated_data[-1]
    assert new_row['Title'] == 'Drink more water'
    assert new_row['Calendar'] == 'Health & Wellness'
    assert str(new_row['Priority']) == '0'  # Convert to string for comparison

    # Verify the new reminder is added to the app
    new_reminders = reminders_app.text_query("Find reminders about drinking water in Health & Wellness calendar")
    assert len(new_reminders) > 0
    assert any(r.title == 'Drink more water' for r in new_reminders)
