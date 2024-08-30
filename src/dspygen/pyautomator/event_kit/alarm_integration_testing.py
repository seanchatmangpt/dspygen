from datetime import datetime, timedelta
import inject
import EventKit

from dspygen.pyautomator.event_kit.alarm import Alarm
from dspygen.pyautomator.event_kit.reminder import Reminder


@inject.autoparams()
def create_reminder_with_alarms(event_store: EventKit.EKEventStore, title: str, calendar: EventKit.EKCalendar):
    reminder = Reminder.create(event_store, title, calendar)
    reminder.due_date = datetime.now() + timedelta(days=1)
    reminder.save()
    return reminder


def eval_alarms(reminder: Reminder):
    # Test absolute date alarm
    absolute_alarm = Alarm.with_absolute_date(datetime.now() + timedelta(hours=2))
    reminder.add_alarm(absolute_alarm)
    print(f"Added absolute date alarm: {absolute_alarm.absolute_date}")

    # Test relative offset alarm
    relative_alarm = Alarm.with_relative_offset(timedelta(minutes=-30))
    reminder.add_alarm(relative_alarm)
    print(f"Added relative offset alarm: {relative_alarm.relative_offset}")

    # Test setting alarm properties
    sound_alarm = Alarm()
    sound_alarm.type = EventKit.EKAlarmTypeAudio
    sound_alarm.sound_name = "Bells"
    reminder.add_alarm(sound_alarm)
    print(f"Added sound alarm with sound: {sound_alarm.sound_name}")

    # Test email alarm
    email_alarm = Alarm()
    email_alarm.type = EventKit.EKAlarmTypeEmail
    email_alarm.email_address = "test@example.com"
    reminder.add_alarm(email_alarm)
    print(f"Added email alarm with address: {email_alarm.email_address}")

    # Save the reminder with alarms
    reminder.save()

    # Verify alarms
    print(f"Number of alarms: {len(reminder.alarms)}")
    for i, alarm in enumerate(reminder.alarms):
        print(f"Alarm {i + 1}:")
        print(f"  Type: {alarm.type}")
        print(f"  Absolute Date: {alarm.absolute_date}")
        print(f"  Relative Offset: {alarm.relative_offset}")
        print(f"  Sound Name: {alarm.sound_name}")
        print(f"  Email Address: {alarm.email_address}")

    # Test removing an alarm
    reminder.remove_alarm(relative_alarm)
    reminder.save()
    print(f"Number of alarms after removal: {len(reminder.alarms)}")


@inject.autoparams()
def main(event_store: EventKit.EKEventStore):
    def request_access_callback(granted, error):
        if not granted:
            raise PermissionError("Access to reminders denied.")

    event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, request_access_callback)

    default_calendar = event_store.defaultCalendarForNewReminders()

    # Create a reminder with alarms
    reminder = create_reminder_with_alarms(event_store, "Test Reminder with Alarms", default_calendar)

    # Test alarm functionality
    eval_alarms(reminder)

    # Clean up
    # reminder.remove()
    print("Reminder deleted successfully.")


if __name__ == "__main__":
    main()
