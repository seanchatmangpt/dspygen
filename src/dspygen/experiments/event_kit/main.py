
from datetime import datetime

from dspygen.experiments.event_kit.repositories import ReminderRepository, CalendarRepository
from dspygen.experiments.event_kit.services import CalendarService, ReminderService

calendar_repo = CalendarRepository()
reminder_repo = ReminderRepository(calendar_repo)

calendar_service = CalendarService(calendar_repo)
reminder_service = ReminderService(reminder_repo)

# Create a calendar
work_calendar = calendar_service.create_calendar(title="Work")

# Create a reminder in the calendar
reminder = reminder_service.create_reminder(calendar_id=work_calendar.id, title="Finish report", due_date=datetime(2024, 8, 30))

# List calendars
calendars = calendar_service.list_calendars()
for cal in calendars:
    print(f"Calendar: {cal.title}, ID: {cal.id}")

# Get a specific calendar
retrieved_calendar = calendar_service.get_calendar(work_calendar.id)
print(f"Retrieved Calendar: {retrieved_calendar.title}")

# Update a reminder
updated_reminder = reminder_service.update_reminder(work_calendar.id, reminder.id, completed=True)
print(f"Updated Reminder: {updated_reminder.title}, Completed: {updated_reminder.completed}")

# Delete a reminder
reminder_service.delete_reminder(work_calendar.id, reminder.id)

# Delete a calendar
calendar_service.delete_calendar(work_calendar.id)

