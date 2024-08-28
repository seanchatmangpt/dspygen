import EventKit
from Foundation import NSDate
from datetime import datetime, timedelta
from typing import Optional, Union


class Alarm:
    def __init__(self, ek_alarm: Optional[EventKit.EKAlarm] = None):
        self.ek_alarm = ek_alarm or EventKit.EKAlarm.alloc().init()

    @classmethod
    def with_absolute_date(cls, date: datetime):
        ek_alarm = EventKit.EKAlarm.alarmWithAbsoluteDate_(date)
        return cls(ek_alarm)

    @classmethod
    def with_relative_offset(cls, offset: timedelta):
        ek_alarm = EventKit.EKAlarm.alarmWithRelativeOffset_(offset.total_seconds())
        return cls(ek_alarm)

    @property
    def absolute_date(self) -> Optional[datetime]:
        if self.ek_alarm.absoluteDate():
            return datetime.fromtimestamp(self.ek_alarm.absoluteDate().timeIntervalSince1970())
        return None

    @absolute_date.setter
    def absolute_date(self, value: datetime):
        ns_date = NSDate.dateWithTimeIntervalSince1970_(value.timestamp())
        self.ek_alarm.setAbsoluteDate_(ns_date)

    @property
    def relative_offset(self) -> Optional[timedelta]:
        if self.ek_alarm.relativeOffset():
            return timedelta(seconds=self.ek_alarm.relativeOffset())
        return None

    @relative_offset.setter
    def relative_offset(self, value: timedelta):
        self.ek_alarm.setRelativeOffset_(value.total_seconds())

    @property
    def proximity(self) -> Optional[EventKit.EKAlarmProximity]:
        return self.ek_alarm.proximity()

    @proximity.setter
    def proximity(self, value: EventKit.EKAlarmProximity):
        self.ek_alarm.setProximity_(value)

    @property
    def structured_location(self) -> Optional[EventKit.EKStructuredLocation]:
        return self.ek_alarm.structuredLocation()

    @structured_location.setter
    def structured_location(self, value: EventKit.EKStructuredLocation):
        self.ek_alarm.setStructuredLocation_(value)

    @property
    def type(self) -> EventKit.EKAlarmType:
        return self.ek_alarm.type()

    @type.setter
    def type(self, value: EventKit.EKAlarmType):
        self.ek_alarm.setType_(value)

    @property
    def email_address(self) -> Optional[str]:
        return self.ek_alarm.emailAddress()

    @email_address.setter
    def email_address(self, value: Optional[str]):
        self.ek_alarm.setEmailAddress_(value)

    @property
    def sound_name(self) -> Optional[str]:
        return self.ek_alarm.soundName()

    @sound_name.setter
    def sound_name(self, value: Optional[str]):
        self.ek_alarm.setSoundName_(value)

    @property
    def url(self) -> Optional[str]:
        url = self.ek_alarm.URL()
        return str(url) if url else None

    @url.setter
    def url(self, value: Optional[str]):
        if value:
            self.ek_alarm.setURL_(EventKit.NSURL.URLWithString_(value))
        else:
            self.ek_alarm.setURL_(None)


    def to_rfc5545_lines(self) -> list:
        lines = [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "DESCRIPTION:Reminder"
        ]

        if self.ek_alarm.absoluteDate():
            trigger_time = self.ek_alarm.absoluteDate().timeIntervalSince1970()
            trigger_date = datetime.fromtimestamp(trigger_time)
            lines.append(f"TRIGGER;VALUE=DATE-TIME:{trigger_date.strftime('%Y%m%dT%H%M%SZ')}")
        else:
            offset_seconds = self.ek_alarm.relativeOffset()
            if offset_seconds < 0:
                sign = "-"
                offset_seconds = abs(offset_seconds)
            else:
                sign = ""
            offset_hours, remainder = divmod(offset_seconds, 3600)
            offset_minutes, offset_seconds = divmod(remainder, 60)
            lines.append(f"TRIGGER:{sign}PT{int(offset_hours)}H{int(offset_minutes)}M{int(offset_seconds)}S")

        lines.append("END:VALARM")
        return lines