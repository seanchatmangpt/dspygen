import datetime

from dateutil import parser
from typing import Optional


def parse_datetime(dt):
    """
    Parses a datetime string or object into a datetime object.

    :param dt: Datetime in string or datetime object format.
    :return: Parsed datetime object or None.
    """
    if isinstance(dt, str):
        return parser.parse(dt)
    elif isinstance(dt, datetime):
        return dt
    return None


def next_friday() -> str:
    today = datetime.date.today()
    friday = today + datetime.timedelta((4 - today.weekday()) % 7)
    # convert to YYYY-MM-DD format
    return friday.strftime("%Y-%m-%d")


TODAY = datetime.date.today()

# Calculate the number of days until Saturday (assuming today is Sunday, where Monday is 0 and Sunday is 6)
days_until_saturday = (5 - TODAY.weekday()) % 7

# Calculate the date for this Saturday
SATURDAY = TODAY + datetime.timedelta(days=days_until_saturday)

# Calculate the date for this Sunday (assuming Sunday is 6)
SUNDAY = SATURDAY + datetime.timedelta(days=1)

MONDAY_8AM = SUNDAY + datetime.timedelta(days=1)
MONDAY_8AM = datetime.datetime(MONDAY_8AM.year, MONDAY_8AM.month, MONDAY_8AM.day, 8, 0)
MONDAY_9AM = datetime.datetime(MONDAY_8AM.year, MONDAY_8AM.month, MONDAY_8AM.day, 9, 0)

tomorrow_date = TODAY + datetime.timedelta(days=1)


TOMORROW_MORNING_8AM = datetime.datetime(
    tomorrow_date.year, tomorrow_date.month, tomorrow_date.day, 8, 0
)
TOMORROW_MORNING_9AM = datetime.datetime(
    tomorrow_date.year, tomorrow_date.month, tomorrow_date.day, 8, 0
)
SATURDAY_STR = SATURDAY.strftime("%A, %B %d, %Y")
SUNDAY_STR = SUNDAY.strftime("%A, %B %d, %Y")
