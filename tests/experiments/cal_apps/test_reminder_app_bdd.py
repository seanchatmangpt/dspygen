import EventKit
import pytest
from pytest_bdd import scenario, given, when, then
from dspygen.pyautomator.reminders.reminder_app import RemindersApp
from dspygen.pyautomator.event_kit.reminder_list import ReminderList
from dspygen.pyautomator.event_kit.reminder import Reminder


@pytest.fixture
def reminder_app():
    app = RemindersApp()
    app.event_store = MockEventStore()
    # Mock the EventKit.EKCalendar class
    EventKit.EKCalendar = MockCalendar
    return app


class MockEventStore:
    def __init__(self):
        self.calendars = []

    def calendarsForEntityType_(self, entity_type):
        return self.calendars

    def removeCalendar_commit_error_(self, calendar, commit, error):
        self.calendars.remove(calendar)

    def saveCalendar_commit_error_(self, calendar, commit, error):
        self.calendars.append(calendar)

    def saveReminder_commit_error_(self, reminder, commit, error):
        pass

    def removeReminder_commit_error_(self, reminder, commit, error):
        pass

    def defaultCalendarForNewReminders(self):
        return MockCalendar(source=MockSource())


class MockCalendar:
    def __init__(self, title=None, source=None):
        self.title = title
        self.source = source

    @classmethod
    def calendarWithTitle_forEntityType_eventStore_(cls, title, entity_type, event_store):
        return cls(title=title)


class MockSource:
    pass


@scenario('reminder_app.feature', 'Create a new reminder list')
def test_create_new_reminder_list():
    pass


@scenario('reminder_app.feature', 'Add a reminder to a list')
def test_add_reminder_to_list():
    pass


@scenario('reminder_app.feature', 'Mark a reminder as completed')
def test_mark_reminder_as_completed():
    pass


@scenario('reminder_app.feature', 'Remove a reminder list')
def test_remove_reminder_list():
    pass


@scenario('reminder_app.feature', 'Clear completed reminders')
def test_clear_completed_reminders():
    pass


@given('the Reminder App is initialized')
def reminder_app_initialized(reminder_app):
    assert isinstance(reminder_app, RemindersApp)


@when('I add a new reminder list called "{list_name}"')
def add_new_reminder_list(reminder_app, list_name):
    new_list = ReminderList(list_name, reminder_app.event_store)
    reminder_app.add_list(new_list)


@then('the "{list_name}" list should be in the app\'s lists')
def check_list_in_app_lists(reminder_app, list_name):
    assert any(lst.name == list_name for lst in reminder_app.lists)


@given('a reminder list called "{list_name}" exists')
def reminder_list_exists(reminder_app, list_name):
    new_list = ReminderList(list_name, reminder_app.event_store)
    reminder_app.add_list(new_list)


@when('I select the "{list_name}" list')
def select_reminder_list(reminder_app, list_name):
    reminder_app.select_list(list_name)


@when('I add a reminder "{title}" with due date "{due_date}"')
def add_reminder_to_list(reminder_app, title, due_date):
    reminder = Reminder(title, due_date)
    reminder_app.add_reminder_to_selected(reminder)


@then('the "{list_name}" list should contain the reminder "{title}"')
def check_reminder_in_list(reminder_app, list_name, title):
    reminders = reminder_app.get_reminders()
    assert any(r.title == title for r in reminders)


@given('the list "{list_name}" has a reminder "{title}"')
def list_has_reminder(reminder_app, list_name, title):
    reminder_app.select_list(list_name)
    reminder = Reminder(title)
    reminder_app.add_reminder_to_selected(reminder)


@when('I mark the reminder "{title}" as completed')
def mark_reminder_completed(reminder_app, title):
    reminders = reminder_app.get_reminders()
    for reminder in reminders:
        if reminder.title == title:
            reminder.mark_as_completed()
            break


@then('the reminder "{title}" should be marked as completed')
def check_reminder_completed(reminder_app, title):
    reminders = reminder_app.get_reminders(completed=True)
    assert any(r.title == title for r in reminders)


@when('I remove the "{list_name}" list')
def remove_reminder_list(reminder_app, list_name):
    for lst in reminder_app.lists:
        if lst.name == list_name:
            reminder_app.remove_list(lst)
            break


@then('the "{list_name}" list should not be in the app\'s lists')
def check_list_not_in_app_lists(reminder_app, list_name):
    assert all(lst.name != list_name for lst in reminder_app.lists)


@given('the list "{list_name}" has a completed reminder "{title}"')
def list_has_completed_reminder(reminder_app, list_name, title):
    reminder_app.select_list(list_name)
    reminder = Reminder(title, completed=True)
    reminder_app.add_reminder_to_selected(reminder)


@given('the list "{list_name}" has an incomplete reminder "{title}"')
def list_has_incomplete_reminder(reminder_app, list_name, title):
    reminder_app.select_list(list_name)
    reminder = Reminder(title)
    reminder_app.add_reminder_to_selected(reminder)


@when('I clear completed reminders')
def clear_completed_reminders(reminder_app):
    reminder_app.clear_completed_reminders()


@then('the "{list_name}" list should not contain the reminder "{title}"')
def check_reminder_not_in_list(reminder_app, list_name, title):
    reminders = reminder_app.get_reminders()
    assert all(r.title != title for r in reminders)
