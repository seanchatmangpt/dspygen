import pytest
from unittest.mock import Mock, patch
from uuid import UUID
from datetime import datetime, timedelta
from src.dspygen.experiments.event_kit.event_kit_service import EventKitService, Calendar, Reminder

@pytest.fixture
def mock_event_kit():
    with patch('src.dspygen.experiments.event_kit.event_kit_service.EventKit') as mock_ek:
        yield mock_ek

@pytest.fixture
def event_kit_service(mock_event_kit):
    return EventKitService()

@pytest.fixture
def sample_calendar():
    return Calendar(id=UUID('12345678-1234-5678-1234-567812345678'), title='Test Calendar')

@pytest.fixture
def sample_reminder():
    return Reminder(
        id=UUID('87654321-4321-8765-4321-876543210987'),
        title='Test Reminder',
        due_date=datetime.now() + timedelta(days=1),
        completed=False,
        notes='Test notes',
        calendar_id=UUID('12345678-1234-5678-1234-567812345678')
    )

def test_request_access(event_kit_service, mock_event_kit):
    # Test successful access request
    mock_event_kit.EKEntityTypeReminder = 'reminder'
    event_kit_service.store.requestAccessToEntityType.side_effect = lambda entity_type, completionHandler: completionHandler(True, None)
    event_kit_service.request_access()

    # Test access denied
    event_kit_service.store.requestAccessToEntityType.side_effect = lambda entity_type, completionHandler: completionHandler(False, None)
    with pytest.raises(PermissionError):
        event_kit_service.request_access()

def test_get_calendars(event_kit_service, mock_event_kit, sample_calendar):
    mock_calendar = Mock()
    mock_calendar.calendarIdentifier.return_value = str(sample_calendar.ci_id)
    mock_calendar.title.return_value = sample_calendar.title
    event_kit_service.store.calendarsForEntityType_.return_value = [mock_calendar]

    calendars = event_kit_service.get_calendars()
    assert len(calendars) == 1
    assert calendars[0].ci_id == sample_calendar.ci_id
    assert calendars[0].title == sample_calendar.title

def test_get_reminders(event_kit_service, mock_event_kit, sample_calendar, sample_reminder):
    mock_calendar = Mock()
    mock_calendar.calendarIdentifier.return_value = str(sample_calendar.ci_id)
    event_kit_service.store.calendarsForEntityType_.return_value = [mock_calendar]

    mock_reminder = Mock()
    mock_reminder.calendarItemIdentifier.return_value = str(sample_reminder.ci_id)
    mock_reminder.title.return_value = sample_reminder.title
    mock_reminder.dueDateComponents.return_value.date.return_value = sample_reminder.due_date
    mock_reminder.isCompleted.return_value = sample_reminder.completed
    mock_reminder.notes.return_value = sample_reminder.notes

    event_kit_service.store.remindersMatchingPredicate_.return_value = [mock_reminder]

    reminders = event_kit_service.get_reminders(sample_calendar.ci_id)
    assert len(reminders) == 1
    assert reminders[0].ci_id == sample_reminder.ci_id
    assert reminders[0].title == sample_reminder.title
    assert reminders[0].due_date == sample_reminder.due_date
    assert reminders[0].completed == sample_reminder.completed
    assert reminders[0].notes == sample_reminder.notes
    assert reminders[0].calendar_id == sample_calendar.ci_id

def test_add_reminder(event_kit_service, mock_event_kit, sample_calendar, sample_reminder):
    mock_calendar = Mock()
    mock_calendar.calendarIdentifier.return_value = str(sample_calendar.ci_id)
    event_kit_service.store.calendarsForEntityType_.return_value = [mock_calendar]

    mock_new_reminder = Mock()
    mock_new_reminder.calendarItemIdentifier.return_value = str(sample_reminder.ci_id)
    mock_new_reminder.title.return_value = sample_reminder.title
    mock_new_reminder.dueDateComponents.return_value.date.return_value = sample_reminder.due_date
    mock_new_reminder.isCompleted.return_value = sample_reminder.completed
    mock_new_reminder.notes.return_value = sample_reminder.notes

    mock_event_kit.EKReminder.reminderWithEventStore_.return_value = mock_new_reminder

    added_reminder = event_kit_service.add_reminder(sample_calendar.ci_id, sample_reminder)
    assert added_reminder.ci_id == sample_reminder.ci_id
    assert added_reminder.title == sample_reminder.title
    assert added_reminder.due_date == sample_reminder.due_date
    assert added_reminder.completed == sample_reminder.completed
    assert added_reminder.notes == sample_reminder.notes
    assert added_reminder.calendar_id == sample_calendar.ci_id

    event_kit_service.store.saveReminder_commit_error_.assert_called_once()

def test_update_reminder(event_kit_service, mock_event_kit, sample_calendar, sample_reminder):
    event_kit_service.get_reminders = Mock(return_value=[sample_reminder])
    event_kit_service.add_reminder = Mock(return_value=sample_reminder)

    updated_reminder_data = sample_reminder.copy()
    updated_reminder_data.title = "Updated Title"
    updated_reminder_data.completed = True

    updated_reminder = event_kit_service.update_reminder(sample_calendar.ci_id, sample_reminder.ci_id, updated_reminder_data)
    
    assert updated_reminder.ci_id == sample_reminder.ci_id
    assert updated_reminder.title == "Updated Title"
    assert updated_reminder.completed == True
    event_kit_service.add_reminder.assert_called_once()

def test_delete_reminder(event_kit_service, mock_event_kit, sample_calendar, sample_reminder):
    event_kit_service.get_reminders = Mock(return_value=[sample_reminder])
    mock_reminder_to_delete = Mock()
    event_kit_service.store.calendarItemWithIdentifier_.return_value = mock_reminder_to_delete

    event_kit_service.delete_reminder(sample_calendar.ci_id, sample_reminder.ci_id)

    event_kit_service.store.removeReminder_commit_error_.assert_called_once_with(mock_reminder_to_delete, True, None)

def test_reminder_not_found(event_kit_service, sample_calendar):
    event_kit_service.get_reminders = Mock(return_value=[])
    
    with pytest.raises(StopIteration):
        event_kit_service.update_reminder(sample_calendar.ci_id, UUID('00000000-0000-0000-0000-000000000000'), Reminder(title="Non-existent Reminder", calendar_id=sample_calendar.ci_id))

    with pytest.raises(StopIteration):
        event_kit_service.delete_reminder(sample_calendar.ci_id, UUID('00000000-0000-0000-0000-000000000000'))

def test_calendar_not_found(event_kit_service, mock_event_kit):
    event_kit_service.store.calendarsForEntityType_.return_value = []
    
    with pytest.raises(StopIteration):
        event_kit_service.get_reminders(UUID('00000000-0000-0000-0000-000000000000'))

    with pytest.raises(StopIteration):
        event_kit_service.add_reminder(UUID('00000000-0000-0000-0000-000000000000'), Reminder(title="Test Reminder", calendar_id=UUID('00000000-0000-0000-0000-000000000000')))