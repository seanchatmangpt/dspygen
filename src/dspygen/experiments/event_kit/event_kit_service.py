import EventKit
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

store = EventKit.EKEventStore.new()


class Reminder(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    due_date: Optional[datetime] = None
    completed: bool = False
    notes: Optional[str] = None
    calendar_id: UUID


class Calendar(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    reminders: List[Reminder] = Field(default_factory=list)


class EventKitService:
    def __init__(self):
        self.store = store
        self.request_access()
        
        # Uncomment the following line when you want to print the EKEventStore info
        # print_ekeventstore_info()

    def request_access(self):
        def handler(granted, error):
            if not granted:
                raise PermissionError("Access to reminders was not granted")

        # Update this line to use the correct method
        self.store.requestAccessToEntityType(EventKit.EKEntityTypeReminder, completionHandler=handler)

    def get_calendars(self) -> List[Calendar]:
        calendars = self.store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        return [Calendar(id=UUID(calendar.calendarIdentifier()), title=calendar.title()) for calendar in calendars]

    def get_reminders(self, calendar_id: UUID) -> List[Reminder]:
        calendar = next(c for c in self.store.calendarsForEntityType_(EventKit.EKEntityTypeReminder) if UUID(c.calendarIdentifier()) == calendar_id)
        predicate = self.store.predicateForRemindersInCalendars_([calendar])
        reminders = self.store.remindersMatchingPredicate_(predicate)

        return [
            Reminder(
                id=UUID(reminder.calendarItemIdentifier()),
                title=reminder.title(),
                due_date=reminder.dueDateComponents().date() if reminder.dueDateComponents() else None,
                completed=reminder.isCompleted(),
                notes=reminder.notes(),
                calendar_id=calendar_id,
            ) for reminder in reminders
        ]

    def add_reminder(self, calendar_id: UUID, reminder_data: Reminder) -> Reminder:
        calendar = next(c for c in self.store.calendarsForEntityType_(EventKit.EKEntityTypeReminder) if UUID(c.calendarIdentifier()) == calendar_id)
        reminder = EventKit.EKReminder.reminderWithEventStore_(self.store)
        reminder.title = reminder_data.title
        reminder.calendar = calendar

        if reminder_data.due_date:
            reminder_due_date = EventKit.EKAlarm.alarmWithAbsoluteDate_(reminder_data.due_date)
            reminder.addAlarm_(reminder_due_date)

        reminder.notes = reminder_data.notes
        reminder.setCompleted_(reminder_data.completed)
        self.store.saveReminder_commit_error_(reminder, True, None)

        return Reminder(
            id=UUID(reminder.calendarItemIdentifier()),
            title=reminder.title(),
            due_date=reminder.dueDateComponents().date() if reminder.dueDateComponents() else None,
            completed=reminder.isCompleted(),
            notes=reminder.notes(),
            calendar_id=calendar_id,
        )

    def update_reminder(self, calendar_id: UUID, reminder_id: UUID, reminder_data: Reminder) -> Reminder:
        reminders = self.get_reminders(calendar_id)
        reminder = next(r for r in reminders if r.id == reminder_id)

        reminder.title = reminder_data.title
        reminder.due_date = reminder_data.due_date
        reminder.completed = reminder_data.completed
        reminder.notes = reminder_data.notes

        self.add_reminder(calendar_id, reminder)

        return reminder

    def delete_reminder(self, calendar_id: UUID, reminder_id: UUID):
        reminders = self.get_reminders(calendar_id)
        reminder = next(r for r in reminders if r.id == reminder_id)

        reminder_to_delete = self.store.calendarItemWithIdentifier_(str(reminder.id))
        self.store.removeReminder_commit_error_(reminder_to_delete, True, None)

def print_ekeventstore_info():
    print("EKEventStore Methods and Properties:")
    print("====================================")
    
    # Get all attributes of EKEventStore
    attributes = dir(EventKit.EKEventStore)
    
    # Separate methods and properties
    methods = []
    properties = []
    
    for attr in attributes:
        # Skip private attributes (those starting with underscore)
        if attr.startswith('_'):
            continue
        
        # Get the attribute
        attr_value = getattr(EventKit.EKEventStore, attr)
        
        # Check if it's a method or a property
        if callable(attr_value):
            methods.append(attr)
        else:
            properties.append(attr)
    
    # Print methods
    print("\nMethods:")
    for method in sorted(methods):
        print(f"- {method}")
    
    # Print properties
    print("\nProperties:")
    for prop in sorted(properties):
        print(f"- {prop}")

# You can call this function to print the info
print_ekeventstore_info()