"""
time_series_generator.py
========================

Holds TimeSeriesGenerator class to generate time series values
based on a set of inputs.

"""

from datetime import datetime, timedelta
from calendar import monthrange


class SimpleDate(object):
    """
    Simple container class for a date.
    """

    def __init__(self, year, month, day):
        """
        Constructor: sets the instance properties and aliases.

        :param self: the instance
        :param year: year [integer]
        :param month: month [integer]
        :param day: day [integer]
        """
        self.year = self.y = year
        self.month = self.m = month
        self.day = self.d = day

    def __repr__(self):
        return "{:4d}-{:02d}-{:02d}".format(self.y, self.m, self.d)

    def as_list(self):
        """
        Return as 3-member list of integers.

        :return: list of integers ([year, month, day]).
        """
        return [self.y, self.m, self.d]

    def __gt__(self, other):
        this, other = self.as_list(), other.as_list()
        return this > other

    def __lt__(self, other):
        this, other = self.as_list(), other.as_list()
        return this < other

    def __ge__(self, other):
        this, other = self.as_list(), other.as_list()
        return this >= other

    def __le__(self, other):
        this, other = self.as_list(), other.as_list()
        return this <= other



class TimeSeriesGenerator(object):

    SUPPORTED_FREQUENCIES = ['day']
    SUPPORTED_CALENDARS = ['gregorian', 'standard', '360_day']

    def __init__(self, start, end, delta=(1, 'day'), calendar='360_day'):
        """

        :param start:
        :param end:
        :param delta:
        :param calendar:
        """
        self.start = self._validate_datetime(start)
        self.end = self._validate_datetime(end)
        self._set_delta(delta)
        self._set_calendar (calendar)

    def __iter__(self):
        return self.next()

    def __next__(self):
        """

        :return:
        """
        return self.next()

    def _validate_datetime(self, dt):
        """

        :param dt:
        :return:
        """
        return SimpleDate(*dt)

    def _set_delta(self, delta):
        """

        :param delta:
        :return:
        """
        if not delta[1] in self.SUPPORTED_FREQUENCIES:
            raise Exception("Delta uses time frequency '{}' that is not yet supported.".format(delta[1]))

        self.delta = delta

    def _set_calendar(self, calendar):
        """

        :param calendar:
        :return:
        """
        if not calendar in self.SUPPORTED_CALENDARS:
            raise Exception("Unrecognised calendar: '{}'".format(calendar))

        self.calendar = calendar

    def next(self):
        """
        Generator yielding next datetime for 360day calendar.

        :return: tuples of (time value (since reference time), datetime)
        """
        delta_n, unit = self.delta
        current_time = self.start
        value = 0

        while current_time <= self.end:
            yield (value, current_time.as_list())

            value += 1

            for i in range(delta_n):
                getattr(self, "_add_{}".format(unit))(current_time)


    def _add_year(self, dt):
        dt.y += 1

    def _add_month(self, dt):
        if dt.m < 12:
            dt.m += 1
        else:
            dt.m = 1
            self._add_year(dt)

    def _add_day(self, dt):
        if self.calendar == "360_day":
            limit = 30
        elif self.calendar in ("standard", "gregorian"):
            limit = monthrange(dt.y, dt.m)[1]

        if dt.d < limit:
            dt.d += 1
        else:
            dt.d = 1
            self._add_month(dt)

