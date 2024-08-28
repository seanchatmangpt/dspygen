from datetime import datetime
from typing import Optional, List
import EventKit

class RecurrenceRule:
    def __init__(self, ek_recurrence_rule: EventKit.EKRecurrenceRule):
        self.ek_recurrence_rule = ek_recurrence_rule

    @classmethod
    def create(cls, frequency: EventKit.EKRecurrenceFrequency, interval: int = 1,
               end_date: Optional[datetime] = None, occurrences: Optional[int] = None,
               days_of_week: Optional[List[int]] = None, 
               days_of_month: Optional[List[int]] = None,
               months_of_year: Optional[List[int]] = None,
               weeks_of_year: Optional[List[int]] = None,
               days_of_year: Optional[List[int]] = None,
               set_positions: Optional[List[int]] = None):
        
        recurrence_end = None
        if end_date:
            recurrence_end = EventKit.EKRecurrenceEnd.recurrenceEndWithEndDate_(end_date)
        elif occurrences:
            recurrence_end = EventKit.EKRecurrenceEnd.recurrenceEndWithOccurrenceCount_(occurrences)

        ek_days_of_week = None
        if days_of_week:
            ek_days_of_week = [EventKit.EKRecurrenceDayOfWeek.dayOfWeek_(day+1) for day in days_of_week]

        ek_recurrence_rule = EventKit.EKRecurrenceRule.alloc().initRecurrenceWithFrequency_interval_daysOfTheWeek_daysOfTheMonth_monthsOfTheYear_weeksOfTheYear_daysOfTheYear_setPositions_end_(
            frequency,
            interval,
            ek_days_of_week,
            days_of_month,
            months_of_year,
            weeks_of_year,
            days_of_year,
            set_positions,
            recurrence_end
        )

        return cls(ek_recurrence_rule)

    @classmethod
    def from_string(cls, rrule_string: str):
        ek_recurrence_rule = EventKit.EKRecurrenceRule.recurrenceWithString_(rrule_string)
        return cls(ek_recurrence_rule)

    def to_string(self) -> str:
        components = []
        
        # Frequency
        freq_map = {
            EventKit.EKRecurrenceFrequencyDaily: "DAILY",
            EventKit.EKRecurrenceFrequencyWeekly: "WEEKLY",
            EventKit.EKRecurrenceFrequencyMonthly: "MONTHLY",
            EventKit.EKRecurrenceFrequencyYearly: "YEARLY"
        }
        components.append(f"FREQ={freq_map.get(self.ek_recurrence_rule.frequency(), 'DAILY')}")
        
        # Interval
        if self.ek_recurrence_rule.interval() != 1:
            components.append(f"INTERVAL={self.ek_recurrence_rule.interval()}")
        
        # End
        if self.ek_recurrence_rule.recurrenceEnd():
            end = self.ek_recurrence_rule.recurrenceEnd()
            if end.endDate():
                end_date = datetime.fromtimestamp(end.endDate().timeIntervalSince1970())
                components.append(f"UNTIL={end_date.strftime('%Y%m%dT%H%M%SZ')}")
            elif end.occurrenceCount():
                components.append(f"COUNT={end.occurrenceCount()}")
        
        # Days of the week
        if self.ek_recurrence_rule.daysOfTheWeek():
            days = [day.dayOfTheWeek() for day in self.ek_recurrence_rule.daysOfTheWeek()]
            day_map = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}
            components.append(f"BYDAY={','.join(day_map[day] for day in days)}")
        
        # Other components
        if self.ek_recurrence_rule.daysOfTheMonth():
            components.append(f"BYMONTHDAY={','.join(map(str, self.ek_recurrence_rule.daysOfTheMonth()))}")
        if self.ek_recurrence_rule.monthsOfTheYear():
            components.append(f"BYMONTH={','.join(map(str, self.ek_recurrence_rule.monthsOfTheYear()))}")
        if self.ek_recurrence_rule.weeksOfTheYear():
            components.append(f"BYWEEKNO={','.join(map(str, self.ek_recurrence_rule.weeksOfTheYear()))}")
        if self.ek_recurrence_rule.daysOfTheYear():
            components.append(f"BYYEARDAY={','.join(map(str, self.ek_recurrence_rule.daysOfTheYear()))}")
        if self.ek_recurrence_rule.setPositions():
            components.append(f"BYSETPOS={','.join(map(str, self.ek_recurrence_rule.setPositions()))}")
        
        return ";".join(components)

    def __str__(self):
        return self.to_string()