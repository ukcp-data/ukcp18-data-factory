"""
Tests for TimeSeriesGenerator class in time_series_generator.py module.
"""

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

