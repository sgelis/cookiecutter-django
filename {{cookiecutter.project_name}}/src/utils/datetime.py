# Standard library
import datetime
from typing import Optional


def now_timestamp_ms() -> int:
    """
    Returns:
        Current timestamp in ms, Javascript-ready.
    """
    return round(datetime.datetime.now().timestamp() * 1000)


def last_day_of_month(date: Optional[datetime.date] = None) -> datetime.date:
    """
    Args:
        date: Date for which to query the last day of its month. Defaults to today.

    Returns:
        A date object representing the last day of the month ongoing at given date.
    """
    date = date or datetime.date.today()
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
