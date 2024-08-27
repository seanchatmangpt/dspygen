
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID

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

    def add_reminder(self, reminder: Reminder):
        self.reminders.append(reminder)

    def remove_reminder(self, reminder_id: UUID):
        self.reminders = [r for r in self.reminders if r.id != reminder_id]

