"""Integration tests for the EventKit service layer.

These tests exercise the high-level service patterns used by the EventKit
integration (calendars, reminders CRUD) via mock objects so the tests run
on any platform without requiring macOS EventKit access.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, call
from uuid import UUID, uuid4


# ---------------------------------------------------------------------------
# Lightweight stand-ins for the macOS-only EventKit models
# ---------------------------------------------------------------------------

class _Calendar:
    """Minimal Calendar model matching the EventKit service contract."""

    def __init__(self, cal_id, title):
        self.cal_id = cal_id
        self.title = title


class _Reminder:
    """Minimal Reminder model matching the EventKit service contract."""

    def __init__(self, reminder_id, title, due_date=None, completed=False,
                 notes="", calendar_id=None):
        self.reminder_id = reminder_id
        self.title = title
        self.due_date = due_date
        self.completed = completed
        self.notes = notes
        self.calendar_id = calendar_id


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_calendar_id():
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def sample_reminder_id():
    return UUID("87654321-4321-8765-4321-876543210987")


@pytest.fixture
def sample_calendar(sample_calendar_id):
    return _Calendar(cal_id=sample_calendar_id, title="Test Calendar")


@pytest.fixture
def sample_reminder(sample_reminder_id, sample_calendar_id):
    return _Reminder(
        reminder_id=sample_reminder_id,
        title="Test Reminder",
        due_date=datetime.now() + timedelta(days=1),
        completed=False,
        notes="Test notes",
        calendar_id=sample_calendar_id,
    )


@pytest.fixture
def mock_store():
    """A mock object that simulates an EKEventStore."""
    store = MagicMock()
    return store


# ---------------------------------------------------------------------------
# Calendar tests
# ---------------------------------------------------------------------------

def test_get_calendars_returns_list(mock_store, sample_calendar):
    """Fetching calendars from the store should return a list."""
    mock_cal = MagicMock()
    mock_cal.calendarIdentifier.return_value = str(sample_calendar.cal_id)
    mock_cal.title.return_value = sample_calendar.title
    mock_store.calendarsForEntityType_.return_value = [mock_cal]

    raw_calendars = mock_store.calendarsForEntityType_("EKEntityTypeReminder")
    assert len(raw_calendars) == 1
    assert raw_calendars[0].title() == "Test Calendar"


def test_get_calendars_empty_store(mock_store):
    """An empty store should return an empty calendar list."""
    mock_store.calendarsForEntityType_.return_value = []

    raw_calendars = mock_store.calendarsForEntityType_("EKEntityTypeReminder")
    assert raw_calendars == []


def test_calendar_title_is_preserved(mock_store, sample_calendar):
    """Calendar titles should survive a round-trip through the mock store."""
    mock_cal = MagicMock()
    mock_cal.title.return_value = sample_calendar.title
    mock_store.calendarsForEntityType_.return_value = [mock_cal]

    calendars = mock_store.calendarsForEntityType_("EKEntityTypeReminder")
    titles = [c.title() for c in calendars]
    assert sample_calendar.title in titles


# ---------------------------------------------------------------------------
# Reminder read tests
# ---------------------------------------------------------------------------

def test_get_reminders_returns_reminders(mock_store, sample_calendar, sample_reminder):
    """Fetching reminders for a known calendar should return the right items."""
    mock_reminder = MagicMock()
    mock_reminder.calendarItemIdentifier.return_value = str(sample_reminder.reminder_id)
    mock_reminder.title.return_value = sample_reminder.title
    mock_reminder.isCompleted.return_value = sample_reminder.completed
    mock_reminder.notes.return_value = sample_reminder.notes
    mock_store.remindersMatchingPredicate_.return_value = [mock_reminder]

    reminders = mock_store.remindersMatchingPredicate_("predicate")
    assert len(reminders) == 1
    assert reminders[0].title() == "Test Reminder"
    assert reminders[0].isCompleted() is False


def test_get_reminders_empty_calendar(mock_store):
    """Fetching reminders from an empty calendar should return an empty list."""
    mock_store.remindersMatchingPredicate_.return_value = []

    reminders = mock_store.remindersMatchingPredicate_("predicate")
    assert reminders == []


# ---------------------------------------------------------------------------
# Reminder create / save tests
# ---------------------------------------------------------------------------

def test_save_reminder_is_called(mock_store, sample_calendar, sample_reminder):
    """Saving a new reminder should invoke the store's save method."""
    mock_new_ek_reminder = MagicMock()
    mock_new_ek_reminder.calendarItemIdentifier.return_value = str(
        sample_reminder.reminder_id
    )
    mock_store.saveReminder_commit_error_.return_value = (True, None)

    success, error = mock_store.saveReminder_commit_error_(
        mock_new_ek_reminder, True, None
    )
    assert success is True
    assert error is None
    mock_store.saveReminder_commit_error_.assert_called_once_with(
        mock_new_ek_reminder, True, None
    )


def test_save_reminder_failure_propagates(mock_store):
    """A failed save should surface the error from the store."""
    mock_store.saveReminder_commit_error_.return_value = (False, "disk full")
    mock_reminder = MagicMock()

    success, error = mock_store.saveReminder_commit_error_(mock_reminder, True, None)
    assert success is False
    assert error == "disk full"


# ---------------------------------------------------------------------------
# Reminder update tests
# ---------------------------------------------------------------------------

def test_update_reminder_modifies_title(sample_reminder):
    """Updating a reminder's title should reflect the new value."""
    original_title = sample_reminder.title
    sample_reminder.title = "Updated Title"
    assert sample_reminder.title == "Updated Title"
    assert sample_reminder.title != original_title


def test_update_reminder_marks_complete(sample_reminder):
    """Completing a reminder should flip its completed flag."""
    assert sample_reminder.completed is False
    sample_reminder.completed = True
    assert sample_reminder.completed is True


# ---------------------------------------------------------------------------
# Reminder delete tests
# ---------------------------------------------------------------------------

def test_remove_reminder_is_called(mock_store, sample_reminder):
    """Removing a reminder should invoke the store's remove method."""
    mock_ek_reminder = MagicMock()
    mock_store.removeReminder_commit_error_.return_value = (True, None)

    success, error = mock_store.removeReminder_commit_error_(
        mock_ek_reminder, True, None
    )
    assert success is True
    mock_store.removeReminder_commit_error_.assert_called_once()


def test_remove_nonexistent_reminder_returns_error(mock_store):
    """Attempting to remove a reminder that doesn't exist should return an error."""
    mock_store.removeReminder_commit_error_.return_value = (False, "not found")
    mock_reminder = MagicMock()

    success, error = mock_store.removeReminder_commit_error_(
        mock_reminder, True, None
    )
    assert success is False
    assert "not found" in error


# ---------------------------------------------------------------------------
# Access / permission tests
# ---------------------------------------------------------------------------

def test_request_access_granted(mock_store):
    """A granted access callback should not raise any exception."""
    results = {}

    def callback(granted, error):
        results["granted"] = granted
        results["error"] = error

    mock_store.requestAccessToEntityType_completion_.side_effect = (
        lambda entity_type, cb: cb(True, None)
    )
    mock_store.requestAccessToEntityType_completion_(
        "EKEntityTypeReminder", callback
    )
    assert results["granted"] is True
    assert results["error"] is None


def test_request_access_denied_raises(mock_store):
    """A denied access callback should trigger a PermissionError."""
    def callback(granted, error):
        if not granted:
            raise PermissionError("Access to reminders denied.")

    mock_store.requestAccessToEntityType_completion_.side_effect = (
        lambda entity_type, cb: cb(False, None)
    )
    with pytest.raises(PermissionError):
        mock_store.requestAccessToEntityType_completion_(
            "EKEntityTypeReminder", callback
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
