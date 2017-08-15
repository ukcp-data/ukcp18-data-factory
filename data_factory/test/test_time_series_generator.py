"""
Tests for TimeSeriesGenerator class in time_series_generator.py module.
"""

from datetime import datetime
from data_factory.time_series_generator import TimeSeriesGenerator


def test_tsg_standard_calendar_1_day():
    start = [2000, 1, 1]
    end = [2020, 12, 1]
    tsg = TimeSeriesGenerator(start, end, delta=[1, 'day'], calendar='standard')

    data = [dt for dt in tsg]
    assert(len(data) == 7641)

    assert(data[31][1] == [2000, 2, 1])
    assert(data[-1][1] == [2020, 12, 1])


def test_tsg_360_day_calendar_1_day():
    start = [2000, 1, 1]
    end = [2009, 12, 30]
    tsg = TimeSeriesGenerator(start, end, delta=[1, 'day'], calendar='360_day')

    length = 10 * 12 * 30
    data = [dt for dt in tsg]
    assert(len(data) == length)

    assert(data[31][1] == [2000, 2, 2])
    assert(data[-1][1] == [2009, 12, 30])


def test_tsg_standard_calendar_5_days():
    start = [2000, 1, 1]
    end = [2000, 12, 31]
    tsg = TimeSeriesGenerator(start, end, delta=[5, 'day'], calendar='standard')

    data = [dt for dt in tsg]
    assert(len(data) == (366 / 5) + 1)

    assert(data[4][1] == [2000, 1, 21])
    assert(data[-1][1] == [2000, 12, 31])


def test_tsg_360_day_calendar_30_days():
    start = [2000, 1, 15]
    end = [2000, 12, 15]
    tsg = TimeSeriesGenerator(start, end, delta=[30, 'day'], calendar='360_day')

    data = [dt for dt in tsg]
    assert(len(data) == 12)

    assert(data[0][1] == [2000, 1, 15])
    assert(data[-1][1] == [2000, 12, 15])


def test_tsg_standard_calendar_1_month():
    start = [2001, 1, 15]
    end = [2020, 12, 15]
    tsg = TimeSeriesGenerator(start, end, delta=[1, 'mon'], calendar='standard')

    data = [dt for dt in tsg]
    assert(len(data) == 240)

    assert(data[1][1] == [2001, 2, 15])
    assert(data[-2][1] == [2020, 11, 15])


def test_tsg_standard_calendar_month_alias():
    start = [2000, 1, 1]
    end = [2020, 12, 1]
    tsg1 = TimeSeriesGenerator(start, end, delta=[1, 'mon'], calendar='standard')
    tsg2 = TimeSeriesGenerator(start, end, delta=[1, 'month'], calendar='standard')
    assert([dt for dt in tsg1] == [dt for dt in tsg2])


def test_tsg_formats_success():
    start = [2000, 1, 1]
    end = [2000, 3, 1]
    tsg = TimeSeriesGenerator(start, end, delta=[1, 'mon'], calendar='standard')

    tsg.set_format('list')
    assert(tsg.next() == (0, [2000, 1, 1]))

    tsg.set_format('datetime')
    assert(tsg.next() == (1, datetime(2000, 2, 1)))

    tsg.set_format('string')
    assert(tsg.next() == (2, "2000-03-01T00:00:00"))