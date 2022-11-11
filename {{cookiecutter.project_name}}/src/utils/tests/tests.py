# Standard library
import datetime

# Own
from ..datetime import last_day_of_month, now_timestamp_ms
from ..main import strip_accents


def test_last_day_of_month():
    for month in range(1, 13):
        date = datetime.date(year=2020, month=month, day=13)
        last_day = last_day_of_month(date)

        if month in (1, 3, 5, 7, 8, 10, 12):
            assert last_day.day == 31

        elif month in (4, 6, 9, 11):
            assert last_day.day == 30

        elif month == 2:
            assert last_day.day in (28, 29)


def test_now_timestamp_ms():
    expected = round(datetime.datetime.now().timestamp() * 1000)
    actual = now_timestamp_ms()

    # Tolerate 50ms drift (execution time)
    assert actual - expected < 50


def test_strip_accents():
    assert strip_accents("ÀàÇçÉéÈèËëÊêÏïÎîÖöÔôÜüÛûÙù") == "AaCcEeEeEeEeIiIiOoOoUuUuUu"
