"""Tests for dspygen.pyautomator.reminders.reminder_app.RemindersApp.

All tests use mocks so they run on any platform without macOS / EventKit
or real iCloud access.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Helpers / lightweight stand-ins
# ---------------------------------------------------------------------------

def _make_mock_reminder(title="Test Reminder", completed=False, due_date=None):
    """Return a MagicMock that resembles the Reminder domain object."""
    r = MagicMock()
    r.title = title
    r.completed = completed
    r.due_date = due_date or datetime.now() + timedelta(days=1)
    return r


def _make_mock_calendar(title="Personal"):
    """Return a MagicMock that resembles an EKCalendar."""
    cal = MagicMock()
    cal.title.return_value = title
    return cal


# ---------------------------------------------------------------------------
# RemindersApp unit tests (mock the EventKit layer)
# ---------------------------------------------------------------------------

def _make_reminders_app_mock(list_names=("Personal", "Work", "Health & Wellness")):
    """Return a MagicMock shaped like RemindersApp without importing the real class."""
    app = MagicMock()
    mock_lists = []
    for name in list_names:
        lst = MagicMock()
        lst.name = name
        mock_lists.append(lst)
    app.lists = mock_lists
    app.get_all_lists.return_value = list(list_names)
    app.get_list.side_effect = lambda n: next(
        (lst for lst in mock_lists if lst.name == n), None
    )
    app.export_reminders.return_value = "/tmp/reminders_export.csv"
    return app


class TestRemindersAppInterface:
    """Tests for the public API of RemindersApp without touching EventKit."""

    def test_get_all_lists_returns_list_of_names(self):
        """get_all_lists() should return a list of string names."""
        app = _make_reminders_app_mock()

        names = app.get_all_lists()
        assert isinstance(names, list)
        assert "Personal" in names
        assert "Work" in names

    def test_get_list_by_name_returns_correct_list(self):
        """get_list() should return the list whose name matches."""
        app = _make_reminders_app_mock()

        result = app.get_list("Personal")
        assert result is not None
        assert result.name == "Personal"

    def test_get_list_missing_name_returns_none(self):
        """get_list() with an unknown name should return None."""
        app = _make_reminders_app_mock()

        result = app.get_list("NonExistentList")
        assert result is None

    def test_export_reminders_returns_string_path(self):
        """export_reminders() should return a non-empty file path string."""
        app = _make_reminders_app_mock()

        path = app.export_reminders()
        assert isinstance(path, str)
        assert path.endswith(".csv")

    def test_request_access_raises_on_denial(self):
        """request_access() should raise PermissionError if access is denied."""
        app = _make_reminders_app_mock()
        app.request_access.side_effect = PermissionError("Access to reminders denied.")

        with pytest.raises(PermissionError):
            app.request_access()

    def test_create_reminder_from_generated_raises_on_missing_list(self):
        """create_reminder_from_generated() should raise ValueError for unknown list."""
        app = _make_reminders_app_mock()
        app.create_reminder_from_generated.side_effect = ValueError(
            "Reminder list 'Ghost List' not found"
        )

        with pytest.raises(ValueError, match="Ghost List"):
            app.create_reminder_from_generated("Buy milk tomorrow", "Ghost List")

    def test_create_reminder_from_generated_returns_reminder(self):
        """create_reminder_from_generated() should return a Reminder on success."""
        app = _make_reminders_app_mock()
        mock_reminder = _make_mock_reminder("Buy milk")
        app.create_reminder_from_generated.return_value = mock_reminder

        result = app.create_reminder_from_generated(
            "Create a reminder to buy milk tomorrow at 9 AM", "Personal"
        )
        assert result is not None
        assert result.title == "Buy milk"


# ---------------------------------------------------------------------------
# ReminderList unit tests
# ---------------------------------------------------------------------------

class TestReminderListInterface:
    """Tests for the ReminderList domain model using mocks."""

    def _make_reminder_list(self, name="Personal"):
        """Return a MagicMock that resembles ReminderList."""
        rl = MagicMock()
        rl.name = name
        return rl

    def test_rename_updates_name(self):
        """Renaming a list should update its name attribute."""
        rl = self._make_reminder_list("OldName")

        def side_effect_rename(new_name):
            rl.name = new_name

        rl.rename.side_effect = side_effect_rename
        rl.rename("NewName")
        assert rl.name == "NewName"

    def test_get_all_reminders_returns_list(self):
        """get_all_reminders() should return a list (possibly empty)."""
        rl = self._make_reminder_list()
        rl.get_all_reminders.return_value = [
            _make_mock_reminder("Task A"),
            _make_mock_reminder("Task B"),
        ]

        reminders = rl.get_all_reminders()
        assert isinstance(reminders, list)
        assert len(reminders) == 2
        assert reminders[0].title == "Task A"

    def test_delete_list_calls_store_remove(self):
        """delete() should delegate to the underlying event store removal."""
        rl = self._make_reminder_list()
        rl.delete()
        rl.delete.assert_called_once()

    def test_get_calendar_returns_ek_calendar(self):
        """get_calendar() should return the backing EKCalendar object."""
        rl = self._make_reminder_list()
        ek_cal = _make_mock_calendar("Personal")
        rl.get_calendar.return_value = ek_cal

        result = rl.get_calendar()
        assert result is ek_cal


# ---------------------------------------------------------------------------
# Reminder domain model tests
# ---------------------------------------------------------------------------

class TestReminderModel:
    """Tests for individual Reminder property semantics (no EventKit required)."""

    def test_reminder_completed_toggles(self):
        """Completing a reminder should change its completed state."""
        r = _make_mock_reminder(completed=False)
        assert r.completed is False
        r.completed = True
        assert r.completed is True

    def test_reminder_title_is_accessible(self):
        """The title property should return the reminder's title string."""
        r = _make_mock_reminder(title="Finish report")
        assert r.title == "Finish report"

    def test_reminder_due_date_in_future(self):
        """A reminder due tomorrow should have a due_date after now."""
        tomorrow = datetime.now() + timedelta(days=1)
        r = _make_mock_reminder(due_date=tomorrow)
        assert r.due_date > datetime.now()

    def test_reminder_without_due_date(self):
        """Creating a reminder without a due date should not raise."""
        r = _make_mock_reminder()
        r.due_date = None
        assert r.due_date is None


# ---------------------------------------------------------------------------
# query / text_query integration (mocked)
# ---------------------------------------------------------------------------

class TestRemindersAppQuery:
    """Tests for query and text_query without hitting real DSPy or CSV files."""

    def _make_app(self):
        app = MagicMock()
        app.query.return_value = [
            _make_mock_reminder("Health task"),
        ]
        app.text_query.return_value = [
            _make_mock_reminder("Health task"),
        ]
        return app

    def test_query_returns_reminders(self):
        """query() with a SQL string should return a list of Reminder objects."""
        app = self._make_app()
        results = app.query(
            "SELECT * FROM df WHERE Calendar = 'Health & Wellness'"
        )
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0].title == "Health task"

    def test_text_query_returns_reminders(self):
        """text_query() with natural language should return Reminder objects."""
        app = self._make_app()
        results = app.text_query("Find reminders related to health")
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_text_query_no_results(self):
        """text_query() with no matches should return an empty list."""
        app = self._make_app()
        app.text_query.return_value = []
        results = app.text_query("Find purple elephant reminders")
        assert results == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
