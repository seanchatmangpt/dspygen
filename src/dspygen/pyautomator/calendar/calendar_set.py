# import objc
# import EventKit
# from Foundation import NSDateComponents, NSCalendar
#
# # Initialize the Event Store
# event_store = EventKit.EKEventStore.alloc().init()
#
# # Request access to reminders
# def request_access_callback(granted, error):
#     if not granted:
#         raise PermissionError("Access to reminders denied.")
#
# event_store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeReminder, request_access_callback)
#
# # Get the default calendar for new reminders
# default_calendar = event_store.defaultCalendarForNewReminders()
#
# # Create a new reminder
# reminder = EventKit.EKReminder.reminderWithEventStore_(event_store)
#
# # Set the reminder properties using the appropriate setter methods or properties
# reminder.setTitle_("New Reminder")
# reminder.setNotes_("This is a test reminder.")
# reminder.setCalendar_(default_calendar)  # Set the calendar
#
# # Set the due date using NSDateComponents
# due_date = NSDateComponents.alloc().init()
# due_date.setYear_(2024)
# due_date.setMonth_(8)
# due_date.setDay_(28)
# due_date.setHour_(7)
#
# reminder.setDueDateComponents_(due_date)
#
# # Save the reminder
# success, error = event_store.saveReminder_commit_error_(reminder, True, objc.nil)
# if not success:
#     raise Exception("Failed to save reminder:", error)
#
# print(f"Reminder '{reminder.title()}' set in calendar '{reminder.calendar().title()}'")