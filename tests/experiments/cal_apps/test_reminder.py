import pytest
from datetime import datetime, timedelta
from dspygen.experiments.cal_apps.reminder import (
    Reminder, create_reminder, read_reminder, update_reminder, delete_reminder, ReminderError
)
from dspygen.experiments.cal_apps.eventkit_mocks import MockEKEventStore, MockEKCalendar, MockEventKit

@pytest.fixture
def event_store():
    return MockEKEventStore()

@pytest.fixture
def calendar():
    return MockEKCalendar("Test Calendar")

def test_create_reminder(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar, datetime.now() + timedelta(days=1))
    assert reminder.title == "Test Reminder"
    assert reminder.calendar.title() == "Test Calendar"
    assert reminder.due_date is not None

def test_read_reminder(event_store, calendar):
    created_reminder = create_reminder(event_store, "Test Reminder", calendar)
    read_reminder_obj = read_reminder(event_store, created_reminder.calendar_item_identifier)
    assert read_reminder_obj.title == "Test Reminder"
    assert read_reminder_obj.calendar.title() == "Test Calendar"

def test_update_reminder(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    new_due_date = datetime.now() + timedelta(days=2)
    update_reminder(reminder, title="Updated Reminder", due_date=new_due_date, completed=True, priority=2)
    assert reminder.title == "Updated Reminder"
    assert reminder.due_date == new_due_date
    assert reminder.completed is True
    assert reminder.priority == 2

def test_delete_reminder(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    identifier = reminder.calendar_item_identifier
    delete_reminder(reminder)
    with pytest.raises(ReminderError):
        read_reminder(event_store, identifier)

def test_reminder_properties(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    reminder.location = "Home"
    reminder.notes = "Test notes"
    reminder.url = "https://example.com"

    assert reminder.location == "Home"
    assert reminder.notes == "Test notes"
    assert reminder.url == "https://example.com"
    assert reminder.creation_date is not None
    assert reminder.last_modified_date is not None
    assert reminder.time_zone is not None

def test_reminder_alarms(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    alarm = MockEventKit.EKAlarm.alarmWithRelativeOffset_(-3600)
    reminder.add_alarm(alarm)
    assert len(reminder.alarms) == 1
    reminder.remove_alarm(alarm)
    assert len(reminder.alarms) == 0

def test_reminder_recurrence(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    rule = MockEventKit.EKRecurrenceRule(
        MockEventKit.EKRecurrenceFrequencyDaily,
        interval=1,
        end=None
    )
    reminder.set_recurrence_rule(rule)
    assert reminder.has_recurrence_rule is True
    assert reminder.recurrence_rule is not None
    reminder.set_recurrence_rule(None)
    assert reminder.has_recurrence_rule is False
    assert reminder.recurrence_rule is None

def test_create_reminder_without_due_date(event_store, calendar):
    reminder = create_reminder(event_store, "No Due Date", calendar)
    assert reminder.due_date is None

def test_update_reminder_partial(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    original_due_date = reminder.due_date
    update_reminder(reminder, title="Updated Title")
    assert reminder.title == "Updated Title"
    assert reminder.due_date == original_due_date

def test_reminder_completed_date(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    assert reminder.completed is False
    reminder.completed = True
    assert reminder.completed is True
    # In a real implementation, we'd check for the actual completion date

def test_reminder_priority_range(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    reminder.priority = 0
    assert reminder.priority == 0
    reminder.priority = 9
    assert reminder.priority == 9
    # In a real implementation, we might want to test out-of-range values

def test_create_multiple_reminders(event_store, calendar):
    reminders = [create_reminder(event_store, f"Reminder {i}", calendar) for i in range(5)]
    assert len(reminders) == 5
    for i, reminder in enumerate(reminders):
        assert reminder.title == f"Reminder {i}"

def test_read_non_existent_reminder(event_store):
    with pytest.raises(ReminderError):
        read_reminder(event_store, "non-existent-id")

def test_update_non_existent_reminder(event_store, calendar):
    non_existent_reminder = Reminder(event_store)
    non_existent_reminder.ek_item.calendarItemIdentifier = lambda: "non-existent-id"
    with pytest.raises(ReminderError):
        update_reminder(non_existent_reminder, title="Should Fail")

def test_delete_non_existent_reminder(event_store, calendar):
    non_existent_reminder = Reminder(event_store)
    non_existent_reminder.ek_item.calendarItemIdentifier = lambda: "non-existent-id"
    with pytest.raises(ReminderError):
        delete_reminder(non_existent_reminder)

def test_reminder_attendees(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    assert reminder.has_attendees is False
    assert len(reminder.attendees) == 0
    # In a real implementation, we'd test adding and removing attendees

def test_reminder_time_zone_change(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    original_tz = reminder.time_zone
    reminder.time_zone = "America/New_York"
    assert reminder.time_zone != original_tz
    assert reminder.time_zone == "America/New_York"

def test_reminder_url_clearing(event_store, calendar):
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    reminder.url = "https://example.com"
    assert reminder.url == "https://example.com"
    reminder.url = None
    assert reminder.url is None

def test_reminder_notes_long_text(event_store, calendar):
    long_text = "A" * 1000  # 1000 character string
    reminder = create_reminder(event_store, "Test Reminder", calendar)
    reminder.notes = long_text
    assert reminder.notes == long_text

def test_reminder_creation_with_all_properties(event_store, calendar):
    due_date = datetime.now() + timedelta(days=1)
    reminder = create_reminder(event_store, "Full Test", calendar, due_date)
    reminder.location = "Office"
    reminder.notes = "Important meeting"
    reminder.url = "https://meeting.com"
    reminder.priority = 1
    alarm = MockEventKit.EKAlarm.alarmWithRelativeOffset_(-1800)  # 30 minutes before
    reminder.add_alarm(alarm)

    assert reminder.title == "Full Test"
    assert reminder.calendar.title() == "Test Calendar"
    assert reminder.due_date == due_date
    assert reminder.location == "Office"
    assert reminder.notes == "Important meeting"
    assert reminder.url == "https://meeting.com"
    assert reminder.priority == 1
    assert len(reminder.alarms) == 1

# Add more edge cases and integration tests as needed
