# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 7. 11
"""
import json
import datetime as dt
from enum import Enum
from typing import Union

from quantfe.utils.date import Date
from quantfe.utils.error import FinError
# from numba import njit, jit, int64, boolean


easterMondayDay = [98, 90, 103, 95, 114, 106, 91, 111, 102, 87,
                   107, 99, 83, 103, 95, 115, 99, 91, 111, 96, 87,
                   107, 92, 112, 103, 95, 108, 100, 91,
                   111, 96, 88, 107, 92, 112, 104, 88, 108, 100,
                   85, 104, 96, 116, 101, 92, 112, 97, 89, 108,
                   100, 85, 105, 96, 109, 101, 93, 112, 97, 89,
                   109, 93, 113, 105, 90, 109, 101, 86, 106, 97,
                   89, 102, 94, 113, 105, 90, 110, 101, 86, 106,
                   98, 110, 102, 94, 114, 98, 90, 110, 95, 86,
                   106, 91, 111, 102, 94, 107, 99, 90, 103, 95,
                   115, 106, 91, 111, 103, 87, 107, 99, 84, 103,
                   95, 115, 100, 91, 111, 96, 88, 107, 92, 112,
                   104, 95, 108, 100, 92, 111, 96, 88, 108, 92,
                   112, 104, 89, 108, 100, 85, 105, 96, 116, 101,
                   93, 112, 97, 89, 109, 100, 85, 105, 97, 109,
                   101, 93, 113, 97, 89, 109, 94, 113, 105, 90,
                   110, 101, 86, 106, 98, 89, 102, 94, 114, 105,
                   90, 110, 102, 86, 106, 98, 111, 102, 94, 114,
                   99, 90, 110, 95, 87, 106, 91, 111, 103, 94,
                   107, 99, 91, 103, 95, 115, 107, 91, 111, 103,
                   88, 108, 100, 85, 105, 96, 109, 101, 93, 112,
                   97, 89, 109, 93, 113, 105, 90, 109, 101, 86,
                   106, 97, 89, 102, 94, 113, 105, 90, 110, 101,
                   86, 106, 98, 110, 102, 94, 114, 98, 90, 110,
                   95, 86, 106, 91, 111, 102, 94, 107, 99, 90,
                   103, 95, 115, 106, 91, 111, 103, 87, 107, 99,
                   84, 103, 95, 115, 100, 91, 111, 96, 88, 107,
                   92, 112, 104, 95, 108, 100, 92, 111, 96, 88,
                   108, 92, 112, 104, 89, 108, 100, 85, 105, 96,
                   116, 101, 93, 112, 97, 89, 109, 100, 85, 105]


class BusDayAdjustTypes(Enum):
    NONE = 1
    FOLLOWING = 2
    MODIFIED_FOLLOWING = 3
    PRECEDING = 4
    MODIFIED_PRECEDING = 5


class CalendarTypes(Enum):
    NONE = 1
    WEEKEND = 2
    AUSTRALIA = 3
    CANADA = 4
    FRANCE = 5
    GERMANY = 6
    ITALY = 7
    JAPAN = 8
    NEW_ZEALAND = 9
    NORWAY = 10
    SWEDEN = 11
    SWITZERLAND = 12
    TARGET = 13
    UNITED_STATES = 14
    UNITED_KINGDOM = 15
    SEOUL = 16
    NEW_YORK = 17
    TOKYO = 18
    LONDON = 19

class DateGenRuleTypes(Enum):
    FORWARD = 1
    BACKWARD = 2

###############################################################################


class Calendar:
    """ Class to manage designation of payment dates as holidays according to
    a regional or country-specific calendar convention specified by the user.
    It also supplies an adjustment method which takes in an adjustment
    convention and then applies that to any date that falls on a holiday in the
    specified calendar. """

    def __init__(self, cal_types: Union[CalendarTypes, list]):
        """ Create a calendar based on a specified calendar type. """
        if isinstance(cal_types, list):
            for _cal_type in cal_types:
                if _cal_type not in CalendarTypes:
                    raise FinError("Need to pass FinCalendarType and not " + str(_cal_type))
            self.cal_type = cal_types
        else:
            if cal_types not in CalendarTypes:
                raise FinError("Need to pass FinCalendarType and not " + str(cal_types))
            self.cal_type = [cal_types]

        self.day_in_year = None
        self.weekday = None
        self.holidays = {}
        
        with open("quantfe/utils/holidays.json", "r") as f:
            total_holidays = json.load(f)

        for cal_type in self.cal_type:
            if str(cal_type.value) not in total_holidays:
                raise FinError(f"Unknown calendar type: {cal_type}")
            
            for date_str, holiday_name in total_holidays[str(cal_type.value)].items():
                if date_str not in self.holidays:
                    self.holidays[date_str] = []
                self.holidays[date_str].append(holiday_name)


    ###########################################################################

    def adjust(self, date: Date, bd_type: BusDayAdjustTypes):
        """ Adjust a payment date if it falls on a holiday according to the
        specified business day convention. """

        if isinstance(bd_type, BusDayAdjustTypes) is False:
            raise FinError("Invalid type passed. Need Finbd_type")

        # If calendar type is NONE then every day is a business day
        if self.cal_type == CalendarTypes.NONE:
            return date

        if bd_type == BusDayAdjustTypes.NONE:
            return date

        elif bd_type == BusDayAdjustTypes.FOLLOWING:
            # step forward until we find a business day
            while self.is_business_day(date) is False:
                date = date.add_days(1)
            return date

        elif bd_type == BusDayAdjustTypes.MODIFIED_FOLLOWING:
            d_start = date.d
            m_start = date.m
            y_start = date.y

            # step forward until we find a business day
            while self.is_business_day(date) is False:
                date = date.add_days(1)

            # if the business day is in a different month look back
            # for previous first business day one day at a time
            # TODO: I could speed this up by starting it at initial date
            if date.m != m_start:
                date = Date(y_start, m_start, d_start)
                while self.is_business_day(date) is False:
                    date = date.add_days(-1)

            return date

        elif bd_type == BusDayAdjustTypes.PRECEDING:
            # if the business day is in the next month look back
            # for previous first business day one day at a time
            while self.is_business_day(date) is False:
                date = date.add_days(-1)

            return date

        elif bd_type == BusDayAdjustTypes.MODIFIED_PRECEDING:
            d_start = date.d
            m_start = date.m
            y_start = date.y

            # step backward until we find a business day
            while self.is_business_day(date) is False:
                date = date.add_days(-1)

            # if the business day is in a different month look forward
            # for previous first business day one day at a time
            # I could speed this up by starting it at initial date
            if date.m != m_start:
                date = Date(y_start, m_start, d_start)
                while self.is_business_day(date) is False:
                    date = date.add_days(+1)

            return date

        else:
            raise FinError("Unknown adjustment convention" + str(bd_type))

        return date

    ###############################################################################

    def add_business_days(self, start_dt: Date, num_days: int):
        """ Returns a new date that is num_days business days after Date.
        All holidays in the chosen calendar are assumed not business days. """

        # TODO: REMOVE DATETIME DEPENDENCE HERE ???

        if isinstance(num_days, int) is False:
            raise FinError("Num days must be an integer")

        _date = dt.date(start_dt.y, start_dt.m, start_dt.d)
        d = _date.day
        m = _date.month
        y = _date.year
        new_dt = Date(y, m, d)

        s = +1
        if num_days < 0:
            num_days = -1 * num_days
            s = -1

        while num_days > 0:
            _date = _date + s * dt.timedelta(days=1)
            d = _date.day
            m = _date.month
            y = _date.year
            new_dt = Date(y, m, d)

            if self.is_business_day(new_dt) is True:
                num_days -= 1

        return new_dt

    ###############################################################################

    def is_business_day(self, date: Date):
        """ Determines if a date is a business day according to the specified
        calendar. If it is it returns True, otherwise False. """

        # For all calendars so far, SAT and SUN are not business days
        # If this ever changes I will need to add a filter here.
        if date.is_weekend():
            return False

        if self.is_holiday(date) is True:
            return False
        else:
            return True

    ###############################################################################

    def is_holiday(self, date: Date):
        """ Determines if a date is a Holiday according to the specified
        calendar. Weekends are not holidays unless the holiday falls on a
        weekend date. """

        if date.str(format="%Y-%m-%d") in self.holidays:
            return True
        else:
            return False

        # start_dt = Date(date.y, 1, 1)
        # self.day_in_year = date.excel_dt - start_dt.excel_dt + 1
        # self.weekday = date.weekday

        # if self.cal_type == CalendarTypes.NONE:
        #     return self.holiday_none(date)
        # elif self.cal_type == CalendarTypes.WEEKEND:
        #     return self.holiday_weekend(date)
        # elif self.cal_type == CalendarTypes.AUSTRALIA:
        #     return self.holiday_australia(date)
        # elif self.cal_type == CalendarTypes.CANADA:
        #     return self.holiday_canada(date)
        # elif self.cal_type == CalendarTypes.FRANCE:
        #     return self.holiday_france(date)
        # elif self.cal_type == CalendarTypes.GERMANY:
        #     return self.holiday_germany(date)
        # elif self.cal_type == CalendarTypes.ITALY:
        #     return self.holiday_italy(date)
        # elif self.cal_type == CalendarTypes.JAPAN:
        #     return self.holiday_japan(date)
        # elif self.cal_type == CalendarTypes.NEW_ZEALAND:
        #     return self.holiday_new_zealand(date)
        # elif self.cal_type == CalendarTypes.NORWAY:
        #     return self.holiday_norway(date)
        # elif self.cal_type == CalendarTypes.SWEDEN:
        #     return self.holiday_sweden(date)
        # elif self.cal_type == CalendarTypes.SWITZERLAND:
        #     return self.holiday_switzerland(date)
        # elif self.cal_type == CalendarTypes.TARGET:
        #     return self.holiday_target(date)
        # elif self.cal_type == CalendarTypes.UNITED_KINGDOM:
        #     return self.holiday_united_kingdom(date)
        # elif self.cal_type == CalendarTypes.UNITED_STATES:
        #     return self.holiday_united_states(date)
        # elif self.cal_type == CalendarTypes.SEOUL:
        #     return self.holiday_seoul(date)
        # elif self.cal_type == CalendarTypes.NEW_YORK:
        #     return self.holiday_newyork(date)
        # elif self.cal_type == CalendarTypes.TOKYO:
        #     return self.holiday_tokyo(date)
        # else:
        #     print(self.cal_type)
        #     raise FinError("Unknown calendar")

    ###############################################################################

    def holiday_weekend(self, date: Date):
        """ Weekends by themselves are a holiday. """

        if date.is_weekend():
            return True
        else:
            return False

    ###############################################################################

    def holiday_australia(self, dt: Date):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 26:  # Australia day
            return True

        if m == 1 and d == 27 and weekday == Date.MON:  # Australia day
            return True

        if m == 1 and d == 28 and weekday == Date.MON:  # Australia day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em - 3:  # good friday
            return True

        if day_in_year == em:  # Easter Monday
            return True

        if m == 4 and d == 25:  # Australia day
            return True

        if m == 4 and d == 26 and weekday == Date.MON:  # Australia day
            return True

        if m == 6 and d > 7 and d < 15 and weekday == Date.MON:  # Queen
            return True

        if m == 8 and d < 8 and weekday == Date.MON:  # BANK holiday
            return True

        if m == 10 and d < 8 and weekday == Date.MON:  # BANK holiday
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26 and weekday == Date.MON:  # Xmas
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Boxing
            return True

        if m == 12 and d == 28 and weekday == Date.MON:  # Boxing
            return True

        return False

    ###############################################################################

    def holiday_united_kingdom(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 2 and weekday == Date.MON:  # new years day
            return True

        if m == 1 and d == 3 and weekday == Date.MON:  # new years day
            return True

        em = easterMondayDay[y - 1901]

        if self.day_in_year == em:  # Easter Monday
            return True

        if self.day_in_year == em - 3:  # good friday
            return True

        if m == 5 and d <= 7 and weekday == Date.MON:
            return True

        if m == 5 and d >= 25 and weekday == Date.MON:
            return True

        if m == 6 and d == 2 and y == 2022:  # SPRING BANK HOLIDAY
            return True

        if m == 6 and d == 3 and y == 2022:  # QUEEN PLAT JUB
            return True

        if m == 8 and d > 24 and weekday == Date.MON:  # Late Summer
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Xmas
            return True

        if m == 12 and d == 27 and weekday == Date.TUE:  # Xmas
            return True

        if m == 12 and d == 28 and weekday == Date.MON:  # Xmas
            return True

        if m == 12 and d == 28 and weekday == Date.TUE:  # Xmas
            return True

        return False

    ###############################################################################

    def holiday_france(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year

        if m == 1 and d == 1:  # new years day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em:  # Easter Monday
            return True

        if day_in_year == em - 3:  # good friday
            return True

        if m == 5 and d == 1:  # LABOUR DAY
            return True

        if m == 5 and d == 8:  # VICTORY DAY
            return True

        if day_in_year == em + 39 - 1:  # Ascension
            return True

        if day_in_year == em + 50 - 1:  # pentecost
            return True

        if m == 7 and d == 14:  # BASTILLE DAY
            return True

        if m == 8 and d == 15:  # ASSUMPTION
            return True

        if m == 11 and d == 1:  # ALL SAINTS
            return True

        if m == 11 and d == 11:  # ARMISTICE
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        return False

    ###############################################################################

    def holiday_sweden(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 6:  # epiphany day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em - 3:  # good friday
            return True

        if day_in_year == em:  # Easter Monday
            return True

        if day_in_year == em + 39 - 1:  # Ascension
            return True

        if m == 5 and d == 1:  # labour day
            return True

        if m == 6 and d == 6:  # June
            return True

        if m == 6 and d > 18 and d < 26 and weekday == Date.FRI:  # Midsummer
            return True

        if m == 12 and d == 24:  # Xmas eve
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        if m == 12 and d == 31:  # NYE
            return True

        return False

    ###############################################################################

    def holiday_germany(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year

        if m == 1 and d == 1:  # new years day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em:  # Easter Monday
            return True

        if day_in_year == em - 3:  # good friday
            return True

        if m == 5 and d == 1:  # LABOUR DAY
            return True

        if day_in_year == em + 39 - 1:  # Ascension
            return True

        if day_in_year == em + 50 - 1:  # pentecost
            return True

        if m == 10 and d == 3:  # GERMAN UNITY DAY
            return True

        if m == 12 and d == 24:  # Xmas eve
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        return False

    ###############################################################################

    def holiday_switzerland(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 2:  # berchtoldstag
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em:  # Easter Monday
            return True

        if day_in_year == em - 3:  # good friday
            return True

        if day_in_year == em + 39 - 1:  # Ascension
            return True

        if day_in_year == em + 50 - 1:  # pentecost / whit
            return True

        if m == 5 and d == 1:  # Labour day
            return True

        if m == 8 and d == 1:  # National day
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        return False

    ###############################################################################

    def holiday_japan(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 2 and weekday == Date.MON:  # bank holiday
            return True

        if m == 1 and d == 3 and weekday == Date.MON:  # bank holiday
            return True

        if m == 1 and d > 7 and d < 15 and weekday == Date.MON:  # coa day
            return True

        if m == 2 and d == 11:  # nfd
            return True

        if m == 2 and d == 12 and weekday == Date.MON:  # nfd
            return True

        if m == 2 and d == 23:  # emperor's birthday
            return True

        if m == 2 and d == 24 and weekday == Date.MON:  # emperor's birthday
            return True

        if m == 3 and d == 20:  # vernal equinox - NOT EXACT
            return True

        if m == 3 and d == 21 and weekday == Date.MON:
            return True

        if m == 4 and d == 29:  # SHOWA greenery
            return True

        if m == 4 and d == 30 and weekday == Date.MON:  # SHOWA greenery
            return True

        if m == 5 and d == 3:  # Memorial Day
            return True

        if m == 5 and d == 4:  # nation
            return True

        if m == 5 and d == 5:  # children
            return True

        if m == 5 and d == 6 and weekday == Date.MON:  # children
            return True

        if m == 7 and d > 14 and d < 22 and y != 2021 and weekday == Date.MON:
            return True

        if m == 7 and d == 22 and y == 2021:  # OLYMPICS
            return True

        if m == 7 and d == 23 and y == 2021:  # OLYMPICS HEALTH AND SPORTS HERE
            return True

        # Mountain day
        if m == 8 and d == 11 and y != 2021:
            return True

        if m == 8 and d == 12 and y != 2021 and weekday == Date.MON:
            return True

        if m == 8 and d == 9 and y == 2021 and weekday == Date.MON:
            return True

        # Respect for aged
        if m == 9 and d > 14 and d < 22 and weekday == Date.MON:
            return True

        # Equinox - APPROXIMATE
        if m == 9 and d == 23:
            return True

        if m == 9 and d == 24 and weekday == Date.MON:
            return True

        if m == 10 and d > 7 and d <= 14 and y != 2021 and weekday == Date.MON:  # HS
            return True

        if m == 11 and d == 3:  # Culture
            return True

        if m == 11 and d == 4 and weekday == Date.MON:  # Culture
            return True

        if m == 11 and d == 23:  # Thanksgiving
            return True
        
        if m == 12 and d == 31:  # End of year
            return True

        return False

    ###############################################################################

    def holiday_tokyo(self, dt):
        year = dt.y
        if year >= 2010 and year < 2020:
            tokyo_holidays = [
                Date(2010,1,1),
                Date(2010,1,11),
                Date(2010,2,11),
                Date(2010,3,22),
                Date(2010,4,29),
                Date(2010,5,3),
                Date(2010,5,4),
                Date(2010,5,5),
                Date(2010,7,19),
                Date(2010,9,20),
                Date(2010,9,23),
                Date(2010,10,11),
                Date(2010,11,3),
                Date(2010,11,23),
                Date(2010,12,23),
                Date(2010,12,31),
                Date(2011,1,1),
                Date(2011,1,2),
                Date(2011,1,3),
                Date(2011,1,10),
                Date(2011,2,11),
                Date(2011,3,21),
                Date(2011,4,29),
                Date(2011,5,3),
                Date(2011,5,4),
                Date(2011,5,5),
                Date(2011,7,18),
                Date(2011,9,19),
                Date(2011,9,23),
                Date(2011,10,10),
                Date(2011,11,3),
                Date(2011,11,23),
                Date(2011,12,23),
                Date(2011,12,31),
                Date(2012,1,2),
                Date(2012,1,3),
                Date(2012,1,9),
                Date(2012,2,11),
                Date(2012,3,20),
                Date(2012,4,30),
                Date(2012,5,3),
                Date(2012,5,4),
                Date(2012,5,5),
                Date(2012,7,16),
                Date(2012,9,17),
                Date(2012,9,22),
                Date(2012,10,8),
                Date(2012,11,3),
                Date(2012,11,23),
                Date(2012,12,24),
                Date(2012,12,31),
                Date(2013,1,1),
                Date(2013,1,2),
                Date(2013,1,3),
                Date(2013,1,14),
                Date(2013,2,11),
                Date(2013,3,20),
                Date(2013,4,29),
                Date(2013,5,3),
                Date(2013,5,4),
                Date(2013,5,5),
                Date(2013,5,6),
                Date(2013,7,15),
                Date(2013,9,16),
                Date(2013,9,23),
                Date(2013,10,14),
                Date(2013,11,3),
                Date(2013,11,4),
                Date(2013,11,23),
                Date(2013,12,23),
                Date(2013,12,31),
                Date(2014,1,1),
                Date(2014,1,2),
                Date(2014,1,3),
                Date(2014,1,13),
                Date(2014,2,11),
                Date(2014,3,21),
                Date(2014,4,29),
                Date(2014,5,3),
                Date(2014,5,4),
                Date(2014,5,5),
                Date(2014,5,6),
                Date(2014,7,21),
                Date(2014,9,15),
                Date(2014,9,23),
                Date(2014,10,13),
                Date(2014,11,3),
                Date(2014,11,23),
                Date(2014,11,24),
                Date(2014,12,23),
                Date(2014,12,31),
                Date(2015,1,1),
                Date(2015,1,2),
                Date(2015,1,3),
                Date(2015,1,12),
                Date(2015,2,11),
                Date(2015,3,21),
                Date(2015,4,29),
                Date(2015,5,3),
                Date(2015,5,4),
                Date(2015,5,5),
                Date(2015,5,6),
                Date(2015,7,20),
                Date(2015,9,21),
                Date(2015,9,22),
                Date(2015,9,23),
                Date(2015,10,12),
                Date(2015,11,3),
                Date(2015,11,23),
                Date(2015,12,23),
                Date(2015,12,31),
                Date(2016,1,1),
                Date(2016,1,2),
                Date(2016,1,3),
                Date(2016,1,11),
                Date(2016,2,11),
                Date(2016,3,20),
                Date(2016,3,21),
                Date(2016,4,29),
                Date(2016,5,3),
                Date(2016,5,4),
                Date(2016,5,5),
                Date(2016,7,18),
                Date(2016,8,11),
                Date(2016,9,19),
                Date(2016,9,22),
                Date(2016,10,10),
                Date(2016,11,3),
                Date(2016,11,23),
                Date(2016,12,23),
                Date(2016,12,31),
                Date(2017,1,1),
                Date(2017,1,2),
                Date(2017,1,3),
                Date(2017,1,9),
                Date(2017,2,11),
                Date(2017,3,20),
                Date(2017,4,29),
                Date(2017,5,3),
                Date(2017,5,4),
                Date(2017,5,5),
                Date(2017,7,17),
                Date(2017,8,11),
                Date(2017,9,18),
                Date(2017,9,23),
                Date(2017,10,9),
                Date(2017,11,3),
                Date(2017,11,23),
                Date(2017,12,23),
                Date(2017,12,31),
                Date(2018,1,1),
                Date(2018,1,2),
                Date(2018,1,3),
                Date(2018,1,8),
                Date(2018,2,12),
                Date(2018,3,21),
                Date(2018,4,30),
                Date(2018,5,3),
                Date(2018,5,4),
                Date(2018,5,5),
                Date(2018,7,16),
                Date(2018,8,11),
                Date(2018,9,17),
                Date(2018,9,24),
                Date(2018,10,8),
                Date(2018,11,3),
                Date(2018,11,23),
                Date(2018,12,24),
                Date(2018,12,31),
                Date(2019,1,1),
                Date(2019,1,2),
                Date(2019,1,3),
                Date(2019,1,14),
                Date(2019,2,11),
                Date(2019,3,21),
                Date(2019,4,29),
                Date(2019,5,1),
                Date(2019,5,2),
                Date(2019,5,3),
                Date(2019,5,4),
                Date(2019,5,6),
                Date(2019,7,15),
                Date(2019,8,12),
                Date(2019,9,16),
                Date(2019,9,23),
                Date(2019,10,14),
                Date(2019,10,22),
                Date(2019,11,4),
                Date(2019,11,23),
                Date(2019,12,31),
            ]
        elif year >= 2020 and year < 2030:
            tokyo_holidays = [
                Date(2020,1,1),
                Date(2020,1,2),
                Date(2020,1,3),
                Date(2020,1,13),
                Date(2020,2,11),
                Date(2020,2,23),
                Date(2020,2,24),
                Date(2020,3,20),
                Date(2020,4,29),
                Date(2020,5,3),
                Date(2020,5,4),
                Date(2020,5,5),
                Date(2020,5,6),
                Date(2020,7,23),
                Date(2020,7,24),
                Date(2020,8,10),
                Date(2020,9,21),
                Date(2020,9,22),
                Date(2020,11,3),
                Date(2020,11,23),
                Date(2020,12,31),
                Date(2021,1,1),
                Date(2021,1,2),
                Date(2021,1,3),
                Date(2021,1,11),
                Date(2021,2,11),
                Date(2021,2,23),
                Date(2021,3,20),
                Date(2021,4,29),
                Date(2021,5,3),
                Date(2021,5,4),
                Date(2021,5,5),
                Date(2021,7,22),
                Date(2021,7,23),
                Date(2021,8,8),
                Date(2021,8,9),
                Date(2021,9,20),
                Date(2021,9,23),
                Date(2021,11,3),
                Date(2021,11,23),
                Date(2021,12,31),
                Date(2022,1,1),
                Date(2022,1,2),
                Date(2022,1,3),
                Date(2022,1,10),
                Date(2022,2,11),
                Date(2022,2,23),
                Date(2022,3,21),
                Date(2022,4,29),
                Date(2022,5,3),
                Date(2022,5,4),
                Date(2022,5,5),
                Date(2022,7,18),
                Date(2022,8,11),
                Date(2022,9,19),
                Date(2022,9,23),
                Date(2022,10,10),
                Date(2022,11,3),
                Date(2022,11,23),
                Date(2022,12,31),
                Date(2023,1,1),
                Date(2023,1,2),
                Date(2023,1,3),
                Date(2023,1,9),
                Date(2023,2,11),
                Date(2023,2,23),
                Date(2023,3,21),
                Date(2023,4,29),
                Date(2023,5,3),
                Date(2023,5,4),
                Date(2023,5,5),
                Date(2023,7,17),
                Date(2023,8,11),
                Date(2023,9,18),
                Date(2023,9,23),
                Date(2023,10,9),
                Date(2023,11,3),
                Date(2023,11,23),
                Date(2023,12,31),
                Date(2024,1,1),
                Date(2024,1,2),
                Date(2024,1,3),
                Date(2024,1,8),
                Date(2024,2,12),
                Date(2024,2,23),
                Date(2024,3,20),
                Date(2024,4,29),
                Date(2024,5,3),
                Date(2024,5,4),
                Date(2024,5,6),
                Date(2024,7,15),
                Date(2024,8,12),
                Date(2024,9,16),
                Date(2024,9,23),
                Date(2024,10,14),
                Date(2024,11,4),
                Date(2024,11,23),
                Date(2024,12,31),
                Date(2025,1,1),
                Date(2025,1,2),
                Date(2025,1,3),
                Date(2025,1,13),
                Date(2025,2,11),
                Date(2025,2,23),
                Date(2025,2,24),
                Date(2025,3,20),
                Date(2025,4,29),
                Date(2025,5,3),
                Date(2025,5,4),
                Date(2025,5,5),
                Date(2025,5,6),
                Date(2025,7,21),
                Date(2025,8,11),
                Date(2025,9,15),
                Date(2025,9,23),
                Date(2025,10,13),
                Date(2025,11,3),
                Date(2025,11,24),
                Date(2025,12,31),
                Date(2026,1,1),
                Date(2026,1,2),
                Date(2026,1,3),
                Date(2026,1,12),
                Date(2026,2,11),
                Date(2026,2,23),
                Date(2026,3,20),
                Date(2026,4,29),
                Date(2026,5,3),
                Date(2026,5,4),
                Date(2026,5,5),
                Date(2026,5,6),
                Date(2026,7,20),
                Date(2026,8,11),
                Date(2026,9,21),
                Date(2026,9,22),
                Date(2026,9,23),
                Date(2026,10,12),
                Date(2026,11,3),
                Date(2026,11,23),
                Date(2026,12,31),
                Date(2027,1,1),
                Date(2027,1,2),
                Date(2027,1,3),
                Date(2027,1,11),
                Date(2027,2,11),
                Date(2027,2,23),
                Date(2027,3,22),
                Date(2027,4,29),
                Date(2027,5,3),
                Date(2027,5,4),
                Date(2027,5,5),
                Date(2027,7,19),
                Date(2027,8,11),
                Date(2027,9,20),
                Date(2027,9,23),
                Date(2027,10,11),
                Date(2027,11,3),
                Date(2027,11,23),
                Date(2027,12,31),
                Date(2028,1,1),
                Date(2028,1,2),
                Date(2028,1,3),
                Date(2028,1,10),
                Date(2028,2,11),
                Date(2028,2,23),
                Date(2028,3,20),
                Date(2028,4,29),
                Date(2028,5,3),
                Date(2028,5,4),
                Date(2028,5,5),
                Date(2028,7,17),
                Date(2028,8,11),
                Date(2028,9,18),
                Date(2028,9,22),
                Date(2028,10,9),
                Date(2028,11,3),
                Date(2028,11,23),
                Date(2028,12,31),
                Date(2029,1,1),
                Date(2029,1,2),
                Date(2029,1,3),
                Date(2029,1,8),
                Date(2029,2,12),
                Date(2029,2,23),
                Date(2029,3,20),
                Date(2029,4,30),
                Date(2029,5,3),
                Date(2029,5,4),
                Date(2029,5,5),
                Date(2029,7,16),
                Date(2029,8,11),
                Date(2029,9,17),
                Date(2029,9,24),
                Date(2029,10,8),
                Date(2029,11,3),
                Date(2029,11,23),
                Date(2029,12,31),
            ]
        elif year >= 2030 and year < 2040:
            tokyo_holidays = [
                Date(2030,1,1),
                Date(2030,1,2),
                Date(2030,1,3),
                Date(2030,1,14),
                Date(2030,2,11),
                Date(2030,2,23),
                Date(2030,3,20),
                Date(2030,4,29),
                Date(2030,5,3),
                Date(2030,5,4),
                Date(2030,5,6),
                Date(2030,7,15),
                Date(2030,8,12),
                Date(2030,9,16),
                Date(2030,9,23),
                Date(2030,10,14),
                Date(2030,11,4),
                Date(2030,11,23),
                Date(2030,12,31),
                Date(2031,1,1),
                Date(2031,1,2),
                Date(2031,1,3),
                Date(2031,1,13),
                Date(2031,2,11),
                Date(2031,2,23),
                Date(2031,2,24),
                Date(2031,3,21),
                Date(2031,4,29),
                Date(2031,5,3),
                Date(2031,5,4),
                Date(2031,5,5),
                Date(2031,5,6),
                Date(2031,7,21),
                Date(2031,8,11),
                Date(2031,9,15),
                Date(2031,9,23),
                Date(2031,10,13),
                Date(2031,11,3),
                Date(2031,11,24),
                Date(2031,12,31),
                Date(2032,1,1),
                Date(2032,1,2),
                Date(2032,1,3),
                Date(2032,1,12),
                Date(2032,2,11),
                Date(2032,2,23),
                Date(2032,3,20),
                Date(2032,4,29),
                Date(2032,5,3),
                Date(2032,5,4),
                Date(2032,5,5),
                Date(2032,7,19),
                Date(2032,8,11),
                Date(2032,9,20),
                Date(2032,9,21),
                Date(2032,9,22),
                Date(2032,10,11),
                Date(2032,11,3),
                Date(2032,11,23),
                Date(2032,12,31),
                Date(2033,1,1),
                Date(2033,1,2),
                Date(2033,1,3),
                Date(2033,1,10),
                Date(2033,2,11),
                Date(2033,2,23),
                Date(2033,3,21),
                Date(2033,4,29),
                Date(2033,5,3),
                Date(2033,5,4),
                Date(2033,5,5),
                Date(2033,7,18),
                Date(2033,8,11),
                Date(2033,9,19),
                Date(2033,9,23),
                Date(2033,10,10),
                Date(2033,11,3),
                Date(2033,11,23),
                Date(2033,12,31),
                Date(2034,1,1),
                Date(2034,1,2),
                Date(2034,1,3),
                Date(2034,1,9),
                Date(2034,2,11),
                Date(2034,2,23),
                Date(2034,3,20),
                Date(2034,4,29),
                Date(2034,5,3),
                Date(2034,5,4),
                Date(2034,5,5),
                Date(2034,7,17),
                Date(2034,8,11),
                Date(2034,9,18),
                Date(2034,9,23),
                Date(2034,10,9),
                Date(2034,11,3),
                Date(2034,11,23),
                Date(2034,12,31),
                Date(2035,1,1),
                Date(2035,1,2),
                Date(2035,1,3),
                Date(2035,1,8),
                Date(2035,2,12),
                Date(2035,2,23),
                Date(2035,3,21),
                Date(2035,4,30),
                Date(2035,5,3),
                Date(2035,5,4),
                Date(2035,5,5),
                Date(2035,7,16),
                Date(2035,8,11),
                Date(2035,9,17),
                Date(2035,9,24),
                Date(2035,10,8),
                Date(2035,11,3),
                Date(2035,11,23),
                Date(2035,12,31),
                Date(2036,1,1),
                Date(2036,1,2),
                Date(2036,1,3),
                Date(2036,1,14),
                Date(2036,2,11),
                Date(2036,2,23),
                Date(2036,3,20),
                Date(2036,4,29),
                Date(2036,5,3),
                Date(2036,5,4),
                Date(2036,5,5),
                Date(2036,5,6),
                Date(2036,7,21),
                Date(2036,8,11),
                Date(2036,9,15),
                Date(2036,9,22),
                Date(2036,10,13),
                Date(2036,11,3),
                Date(2036,11,24),
                Date(2036,12,31),
                Date(2037,1,1),
                Date(2037,1,2),
                Date(2037,1,3),
                Date(2037,1,12),
                Date(2037,2,11),
                Date(2037,2,23),
                Date(2037,3,20),
                Date(2037,4,29),
                Date(2037,5,3),
                Date(2037,5,4),
                Date(2037,5,5),
                Date(2037,5,6),
                Date(2037,7,20),
                Date(2037,8,11),
                Date(2037,9,21),
                Date(2037,9,22),
                Date(2037,9,23),
                Date(2037,10,12),
                Date(2037,11,3),
                Date(2037,11,23),
                Date(2037,12,31),
                Date(2038,1,1),
                Date(2038,1,2),
                Date(2038,1,3),
                Date(2038,1,11),
                Date(2038,2,11),
                Date(2038,2,23),
                Date(2038,3,20),
                Date(2038,4,29),
                Date(2038,5,3),
                Date(2038,5,4),
                Date(2038,5,5),
                Date(2038,7,19),
                Date(2038,8,11),
                Date(2038,9,20),
                Date(2038,9,23),
                Date(2038,10,11),
                Date(2038,11,3),
                Date(2038,11,23),
                Date(2038,12,31),
                Date(2039,1,1),
                Date(2039,1,2),
                Date(2039,1,3),
                Date(2039,1,10),
                Date(2039,2,11),
                Date(2039,2,23),
                Date(2039,3,21),
                Date(2039,4,29),
                Date(2039,5,3),
                Date(2039,5,4),
                Date(2039,5,5),
                Date(2039,7,18),
                Date(2039,8,11),
                Date(2039,9,19),
                Date(2039,9,23),
                Date(2039,10,10),
                Date(2039,11,3),
                Date(2039,11,23),
                Date(2039,12,31),
            ]
        elif year >= 2040 and year < 2050:
            tokyo_holidays = [
                Date(2040,1,1),
                Date(2040,1,2),
                Date(2040,1,3),
                Date(2040,1,9),
                Date(2040,2,11),
                Date(2040,2,23),
                Date(2040,3,20),
                Date(2040,4,30),
                Date(2040,5,3),
                Date(2040,5,4),
                Date(2040,5,5),
                Date(2040,7,16),
                Date(2040,8,11),
                Date(2040,9,17),
                Date(2040,9,22),
                Date(2040,10,8),
                Date(2040,11,3),
                Date(2040,11,23),
                Date(2040,12,31),
                Date(2041,1,1),
                Date(2041,1,2),
                Date(2041,1,3),
                Date(2041,1,14),
                Date(2041,2,11),
                Date(2041,2,23),
                Date(2041,3,20),
                Date(2041,4,29),
                Date(2041,5,3),
                Date(2041,5,4),
                Date(2041,5,6),
                Date(2041,7,15),
                Date(2041,8,12),
                Date(2041,9,16),
                Date(2041,9,23),
                Date(2041,10,14),
                Date(2041,11,4),
                Date(2041,11,23),
                Date(2041,12,31),
                Date(2042,1,1),
                Date(2042,1,2),
                Date(2042,1,3),
                Date(2042,1,13),
                Date(2042,2,11),
                Date(2042,2,23),
                Date(2042,2,24),
                Date(2042,3,20),
                Date(2042,4,29),
                Date(2042,5,3),
                Date(2042,5,4),
                Date(2042,5,5),
                Date(2042,5,6),
                Date(2042,7,21),
                Date(2042,8,11),
                Date(2042,9,15),
                Date(2042,9,23),
                Date(2042,10,13),
                Date(2042,11,3),
                Date(2042,11,24),
                Date(2042,12,31),
                Date(2043,1,1),
                Date(2043,1,2),
                Date(2043,1,3),
                Date(2043,1,12),
                Date(2043,2,11),
                Date(2043,2,23),
                Date(2043,3,21),
                Date(2043,4,29),
                Date(2043,5,3),
                Date(2043,5,4),
                Date(2043,5,5),
                Date(2043,5,6),
                Date(2043,7,20),
                Date(2043,8,11),
                Date(2043,9,21),
                Date(2043,9,22),
                Date(2043,9,23),
                Date(2043,10,12),
                Date(2043,11,3),
                Date(2043,11,23),
                Date(2043,12,31),
                Date(2044,1,1),
                Date(2044,1,2),
                Date(2044,1,3),
                Date(2044,1,11),
                Date(2044,2,11),
                Date(2044,2,23),
                Date(2044,3,21),
                Date(2044,4,29),
                Date(2044,5,3),
                Date(2044,5,4),
                Date(2044,5,5),
                Date(2044,7,18),
                Date(2044,8,11),
                Date(2044,9,19),
                Date(2044,9,22),
                Date(2044,10,10),
                Date(2044,11,3),
                Date(2044,11,23),
                Date(2044,12,31),
                Date(2045,1,1),
                Date(2045,1,2),
                Date(2045,1,3),
                Date(2045,1,9),
                Date(2045,2,11),
                Date(2045,2,23),
                Date(2045,3,20),
                Date(2045,4,29),
                Date(2045,5,3),
                Date(2045,5,4),
                Date(2045,5,5),
                Date(2045,7,17),
                Date(2045,8,11),
                Date(2045,9,18),
                Date(2045,9,22),
                Date(2045,10,9),
                Date(2045,11,3),
                Date(2045,11,23),
                Date(2045,12,31),
                Date(2046,1,1),
                Date(2046,1,2),
                Date(2046,1,3),
                Date(2046,1,8),
                Date(2046,2,12),
                Date(2046,2,23),
                Date(2046,3,20),
                Date(2046,4,30),
                Date(2046,5,3),
                Date(2046,5,4),
                Date(2046,5,5),
                Date(2046,7,16),
                Date(2046,8,11),
                Date(2046,9,17),
                Date(2046,9,24),
                Date(2046,10,8),
                Date(2046,11,3),
                Date(2046,11,23),
                Date(2046,12,31),
                Date(2047,1,1),
                Date(2047,1,2),
                Date(2047,1,3),
                Date(2047,1,14),
                Date(2047,2,11),
                Date(2047,2,23),
                Date(2047,3,21),
                Date(2047,4,29),
                Date(2047,5,3),
                Date(2047,5,4),
                Date(2047,5,6),
                Date(2047,7,15),
                Date(2047,8,12),
                Date(2047,9,16),
                Date(2047,9,23),
                Date(2047,10,14),
                Date(2047,11,4),
                Date(2047,11,23),
                Date(2047,12,31),
                Date(2048,1,1),
                Date(2048,1,2),
                Date(2048,1,3),
                Date(2048,1,13),
                Date(2048,2,11),
                Date(2048,2,23),
                Date(2048,2,24),
                Date(2048,3,20),
                Date(2048,4,29),
                Date(2048,5,3),
                Date(2048,5,4),
                Date(2048,5,5),
                Date(2048,5,6),
                Date(2048,7,20),
                Date(2048,8,11),
                Date(2048,9,21),
                Date(2048,9,22),
                Date(2048,10,12),
                Date(2048,11,3),
                Date(2048,11,23),
                Date(2048,12,31),
                Date(2049,1,1),
                Date(2049,1,2),
                Date(2049,1,3),
                Date(2049,1,11),
                Date(2049,2,11),
                Date(2049,2,23),
                Date(2049,3,21),
                Date(2049,4,29),
                Date(2049,5,3),
                Date(2049,5,4),
                Date(2049,5,5),
                Date(2049,5,6),
                Date(2049,7,19),
                Date(2049,8,11),
                Date(2049,9,20),
                Date(2049,9,21),
                Date(2049,9,22),
                Date(2049,10,11),
                Date(2049,11,3),
                Date(2049,11,23),
                Date(2049,12,31),
            ]
        elif year >= 2050 and year < 2060:
            tokyo_holidays = [
                Date(2050,1,1),
                Date(2050,1,2),
                Date(2050,1,3),
                Date(2050,1,10),
                Date(2050,2,11),
                Date(2050,2,23),
                Date(2050,3,20),
                Date(2050,4,29),
                Date(2050,5,3),
                Date(2050,5,4),
                Date(2050,5,5),
                Date(2050,7,18),
                Date(2050,8,11),
                Date(2050,9,19),
                Date(2050,9,23),
                Date(2050,10,10),
                Date(2050,11,3),
                Date(2050,11,23),
                Date(2050,12,31),
                Date(2051,1,1),
                Date(2051,1,2),
                Date(2051,1,3),
                Date(2051,1,9),
                Date(2051,2,11),
                Date(2051,2,23),
                Date(2051,3,21),
                Date(2051,4,29),
                Date(2051,5,3),
                Date(2051,5,4),
                Date(2051,5,5),
                Date(2051,7,17),
                Date(2051,8,11),
                Date(2051,9,18),
                Date(2051,9,23),
                Date(2051,10,9),
                Date(2051,11,3),
                Date(2051,11,23),
                Date(2051,12,31),
                Date(2052,1,1),
                Date(2052,1,2),
                Date(2052,1,3),
                Date(2052,1,8),
                Date(2052,2,11),
                Date(2052,2,12),
                Date(2052,2,23),
                Date(2052,3,20),
                Date(2052,4,29),
                Date(2052,5,3),
                Date(2052,5,4),
                Date(2052,5,6),
                Date(2052,7,15),
                Date(2052,8,12),
                Date(2052,9,16),
                Date(2052,9,22),
                Date(2052,9,23),
                Date(2052,10,14),
                Date(2052,11,4),
                Date(2052,11,23),
                Date(2052,12,31),
                Date(2053,1,1),
                Date(2053,1,2),
                Date(2053,1,3),
                Date(2053,1,13),
                Date(2053,2,11),
                Date(2053,2,23),
                Date(2053,2,24),
                Date(2053,3,20),
                Date(2053,4,29),
                Date(2053,5,3),
                Date(2053,5,4),
                Date(2053,5,5),
                Date(2053,5,6),
                Date(2053,7,21),
                Date(2053,8,11),
                Date(2053,9,15),
                Date(2053,9,22),
                Date(2053,10,13),
                Date(2053,11,3),
                Date(2053,11,24),
                Date(2053,12,31),
                Date(2054,1,1),
                Date(2054,1,2),
                Date(2054,1,3),
                Date(2054,1,12),
                Date(2054,2,11),
                Date(2054,2,23),
                Date(2054,3,20),
                Date(2054,4,29),
                Date(2054,5,3),
                Date(2054,5,4),
                Date(2054,5,5),
                Date(2054,5,6),
                Date(2054,7,20),
                Date(2054,8,11),
                Date(2054,9,21),
                Date(2054,9,23),
                Date(2054,10,12),
                Date(2054,11,3),
                Date(2054,11,23),
                Date(2054,12,31),
                Date(2055,1,1),
                Date(2055,1,2),
                Date(2055,1,3),
                Date(2055,1,11),
                Date(2055,2,11),
                Date(2055,2,23),
                Date(2055,3,22),
                Date(2055,4,29),
                Date(2055,5,3),
                Date(2055,5,4),
                Date(2055,5,5),
                Date(2055,7,19),
                Date(2055,8,11),
                Date(2055,9,20),
                Date(2055,9,23),
                Date(2055,10,11),
                Date(2055,11,3),
                Date(2055,11,23),
                Date(2055,12,31),
                Date(2056,1,1),
                Date(2056,1,2),
                Date(2056,1,3),
                Date(2056,1,10),
                Date(2056,2,11),
                Date(2056,2,23),
                Date(2056,3,20),
                Date(2056,4,29),
                Date(2056,5,3),
                Date(2056,5,4),
                Date(2056,5,5),
                Date(2056,7,17),
                Date(2056,8,11),
                Date(2056,9,18),
                Date(2056,9,22),
                Date(2056,10,9),
                Date(2056,11,3),
                Date(2056,11,23),
                Date(2056,12,31),
                Date(2057,1,1),
                Date(2057,1,2),
                Date(2057,1,3),
                Date(2057,1,8),
                Date(2057,2,12),
                Date(2057,2,23),
                Date(2057,3,20),
                Date(2057,4,30),
                Date(2057,5,3),
                Date(2057,5,4),
                Date(2057,5,5),
                Date(2057,7,16),
                Date(2057,8,11),
                Date(2057,9,17),
                Date(2057,9,22),
                Date(2057,10,8),
                Date(2057,11,3),
                Date(2057,11,23),
                Date(2057,12,31),
                Date(2058,1,1),
                Date(2058,1,2),
                Date(2058,1,3),
                Date(2058,1,14),
                Date(2058,2,11),
                Date(2058,2,23),
                Date(2058,3,20),
                Date(2058,4,29),
                Date(2058,5,3),
                Date(2058,5,4),
                Date(2058,5,6),
                Date(2058,7,15),
                Date(2058,8,12),
                Date(2058,9,16),
                Date(2058,9,23),
                Date(2058,10,14),
                Date(2058,11,4),
                Date(2058,11,23),
                Date(2058,12,31),
                Date(2059,1,1),
                Date(2059,1,2),
                Date(2059,1,3),
                Date(2059,1,13),
                Date(2059,2,11),
                Date(2059,2,23),
                Date(2059,2,24),
                Date(2059,3,20),
                Date(2059,4,29),
                Date(2059,5,3),
                Date(2059,5,4),
                Date(2059,5,5),
                Date(2059,5,6),
                Date(2059,7,21),
                Date(2059,8,11),
                Date(2059,9,15),
                Date(2059,9,23),
                Date(2059,10,13),
                Date(2059,11,3),
                Date(2059,11,24),
                Date(2059,12,31),
            ]
        elif year >= 2060 and year < 2070:
            tokyo_holidays = [
                Date(2060,1,1),
                Date(2060,1,2),
                Date(2060,1,3),
                Date(2060,1,12),
                Date(2060,2,11),
                Date(2060,2,23),
                Date(2060,3,20),
                Date(2060,4,29),
                Date(2060,5,3),
                Date(2060,5,4),
                Date(2060,5,5),
                Date(2060,5,6),
                Date(2060,7,19),
                Date(2060,8,11),
                Date(2060,9,20),
                Date(2060,9,22),
                Date(2060,10,11),
                Date(2060,11,3),
                Date(2060,11,23),
                Date(2060,12,31),
                Date(2061,1,1),
                Date(2061,1,2),
                Date(2061,1,3),
                Date(2061,1,10),
                Date(2061,2,11),
                Date(2061,2,23),
                Date(2061,3,21),
                Date(2061,4,29),
                Date(2061,5,3),
                Date(2061,5,4),
                Date(2061,5,5),
                Date(2061,7,18),
                Date(2061,8,11),
                Date(2061,9,19),
                Date(2061,9,22),
                Date(2061,10,10),
                Date(2061,11,3),
                Date(2061,11,23),
                Date(2061,12,31),
                Date(2062,1,1),
                Date(2062,1,2),
                Date(2062,1,3),
                Date(2062,1,9),
                Date(2062,2,11),
                Date(2062,2,23),
                Date(2062,3,20),
                Date(2062,4,29),
                Date(2062,5,3),
                Date(2062,5,4),
                Date(2062,5,5),
                Date(2062,7,17),
                Date(2062,8,11),
                Date(2062,9,18),
                Date(2062,9,23),
                Date(2062,10,9),
                Date(2062,11,3),
                Date(2062,11,23),
                Date(2062,12,31),
                Date(2063,1,1),
                Date(2063,1,2),
                Date(2063,1,3),
                Date(2063,1,8),
                Date(2063,2,12),
                Date(2063,2,23),
                Date(2063,3,20),
                Date(2063,4,30),
                Date(2063,5,3),
                Date(2063,5,4),
                Date(2063,5,5),
                Date(2063,7,16),
                Date(2063,8,11),
                Date(2063,9,17),
                Date(2063,9,24),
                Date(2063,10,8),
                Date(2063,11,3),
                Date(2063,11,23),
                Date(2063,12,31),
                Date(2064,1,1),
                Date(2064,1,2),
                Date(2064,1,3),
                Date(2064,1,14),
                Date(2064,2,11),
                Date(2064,2,23),
                Date(2064,3,20),
                Date(2064,4,29),
                Date(2064,5,3),
                Date(2064,5,4),
                Date(2064,5,5),
                Date(2064,5,6),
                Date(2064,7,21),
                Date(2064,8,11),
                Date(2064,9,15),
                Date(2064,9,22),
                Date(2064,10,13),
                Date(2064,11,3),
                Date(2064,11,24),
                Date(2064,12,31),
                Date(2065,1,1),
                Date(2065,1,2),
                Date(2065,1,3),
                Date(2065,1,12),
                Date(2065,2,11),
                Date(2065,2,23),
                Date(2065,3,20),
                Date(2065,4,29),
                Date(2065,5,3),
                Date(2065,5,4),
                Date(2065,5,5),
                Date(2065,5,6),
                Date(2065,7,20),
                Date(2065,8,11),
                Date(2065,9,21),
                Date(2065,9,22),
                Date(2065,10,12),
                Date(2065,11,3),
                Date(2065,11,23),
                Date(2065,12,31),
                Date(2066,1,1),
                Date(2066,1,2),
                Date(2066,1,3),
                Date(2066,1,11),
                Date(2066,2,11),
                Date(2066,2,23),
                Date(2066,3,20),
                Date(2066,4,29),
                Date(2066,5,3),
                Date(2066,5,4),
                Date(2066,5,5),
                Date(2066,7,19),
                Date(2066,8,11),
                Date(2066,9,20),
                Date(2066,9,23),
                Date(2066,10,11),
                Date(2066,11,3),
                Date(2066,11,23),
                Date(2066,12,31),
                Date(2067,1,1),
                Date(2067,1,2),
                Date(2067,1,3),
                Date(2067,1,10),
                Date(2067,2,11),
                Date(2067,2,23),
                Date(2067,3,21),
                Date(2067,4,29),
                Date(2067,5,3),
                Date(2067,5,4),
                Date(2067,5,5),
                Date(2067,7,18),
                Date(2067,8,11),
                Date(2067,9,19),
                Date(2067,9,23),
                Date(2067,10,10),
                Date(2067,11,3),
                Date(2067,11,23),
                Date(2067,12,31),
                Date(2068,1,1),
                Date(2068,1,2),
                Date(2068,1,3),
                Date(2068,1,9),
                Date(2068,2,11),
                Date(2068,2,23),
                Date(2068,3,20),
                Date(2068,4,30),
                Date(2068,5,3),
                Date(2068,5,4),
                Date(2068,5,5),
                Date(2068,7,16),
                Date(2068,8,11),
                Date(2068,9,17),
                Date(2068,9,22),
                Date(2068,10,8),
                Date(2068,11,3),
                Date(2068,11,23),
                Date(2068,12,31),
                Date(2069,1,1),
                Date(2069,1,2),
                Date(2069,1,3),
                Date(2069,1,14),
                Date(2069,2,11),
                Date(2069,2,23),
                Date(2069,3,20),
                Date(2069,4,29),
                Date(2069,5,3),
                Date(2069,5,4),
                Date(2069,5,5),
                Date(2069,5,6),
                Date(2069,7,15),
                Date(2069,8,12),
                Date(2069,9,16),
                Date(2069,9,23),
                Date(2069,10,14),
                Date(2069,11,4),
                Date(2069,11,23),
                Date(2069,12,31),
            ]
        elif year >= 2070 and year < 2080:
            tokyo_holidays = [
                Date(2070,1,1),
                Date(2070,1,2),
                Date(2070,1,3),
                Date(2070,1,13),
                Date(2070,2,11),
                Date(2070,2,23),
                Date(2070,2,24),
                Date(2070,3,20),
                Date(2070,4,29),
                Date(2070,5,3),
                Date(2070,5,4),
                Date(2070,5,5),
                Date(2070,5,6),
                Date(2070,7,21),
                Date(2070,8,11),
                Date(2070,9,15),
                Date(2070,9,23),
                Date(2070,10,13),
                Date(2070,11,3),
                Date(2070,11,24),
                Date(2070,12,31),
                Date(2071,1,1),
                Date(2071,1,2),
                Date(2071,1,3),
                Date(2071,1,12),
                Date(2071,2,11),
                Date(2071,2,23),
                Date(2071,3,20),
                Date(2071,4,29),
                Date(2071,5,3),
                Date(2071,5,4),
                Date(2071,5,5),
                Date(2071,5,6),
                Date(2071,7,20),
                Date(2071,8,11),
                Date(2071,9,21),
                Date(2071,9,23),
                Date(2071,10,12),
                Date(2071,11,3),
                Date(2071,11,23),
                Date(2071,12,31),
                Date(2072,1,1),
                Date(2072,1,2),
                Date(2072,1,3),
                Date(2072,1,11),
                Date(2072,2,11),
                Date(2072,2,23),
                Date(2072,3,21),
                Date(2072,4,29),
                Date(2072,5,3),
                Date(2072,5,4),
                Date(2072,5,5),
                Date(2072,7,18),
                Date(2072,8,11),
                Date(2072,9,19),
                Date(2072,9,22),
                Date(2072,10,10),
                Date(2072,11,3),
                Date(2072,11,23),
                Date(2072,12,31),
                Date(2073,1,1),
                Date(2073,1,2),
                Date(2073,1,3),
                Date(2073,1,9),
                Date(2073,2,11),
                Date(2073,2,23),
                Date(2073,3,20),
                Date(2073,4,29),
                Date(2073,5,3),
                Date(2073,5,4),
                Date(2073,5,5),
                Date(2073,7,17),
                Date(2073,8,11),
                Date(2073,9,18),
                Date(2073,9,22),
                Date(2073,10,9),
                Date(2073,11,3),
                Date(2073,11,23),
                Date(2073,12,31),
                Date(2074,1,1),
                Date(2074,1,2),
                Date(2074,1,3),
                Date(2074,1,8),
                Date(2074,2,12),
                Date(2074,2,23),
                Date(2074,3,20),
                Date(2074,4,30),
                Date(2074,5,3),
                Date(2074,5,4),
                Date(2074,5,5),
                Date(2074,7,16),
                Date(2074,8,11),
                Date(2074,9,17),
                Date(2074,9,24),
                Date(2074,10,8),
                Date(2074,11,3),
                Date(2074,11,23),
                Date(2074,12,31),
                Date(2075,1,1),
                Date(2075,1,2),
                Date(2075,1,3),
                Date(2075,1,14),
                Date(2075,2,11),
                Date(2075,2,23),
                Date(2075,3,20),
                Date(2075,4,29),
                Date(2075,5,3),
                Date(2075,5,4),
                Date(2075,5,6),
                Date(2075,7,15),
                Date(2075,8,12),
                Date(2075,9,16),
                Date(2075,9,23),
                Date(2075,10,14),
                Date(2075,11,4),
                Date(2075,11,23),
                Date(2075,12,31),
                Date(2076,1,1),
                Date(2076,1,2),
                Date(2076,1,3),
                Date(2076,1,13),
                Date(2076,2,11),
                Date(2076,2,23),
                Date(2076,2,24),
                Date(2076,3,20),
                Date(2076,4,29),
                Date(2076,5,3),
                Date(2076,5,4),
                Date(2076,5,5),
                Date(2076,5,6),
                Date(2076,7,20),
                Date(2076,8,11),
                Date(2076,9,21),
                Date(2076,9,22),
                Date(2076,10,12),
                Date(2076,11,3),
                Date(2076,11,23),
                Date(2076,12,31),
                Date(2077,1,1),
                Date(2077,1,2),
                Date(2077,1,3),
                Date(2077,1,11),
                Date(2077,2,11),
                Date(2077,2,23),
                Date(2077,3,20),
                Date(2077,4,29),
                Date(2077,5,3),
                Date(2077,5,4),
                Date(2077,5,5),
                Date(2077,7,19),
                Date(2077,8,11),
                Date(2077,9,20),
                Date(2077,9,22),
                Date(2077,10,11),
                Date(2077,11,3),
                Date(2077,11,23),
                Date(2077,12,31),
                Date(2078,1,1),
                Date(2078,1,2),
                Date(2078,1,3),
                Date(2078,1,10),
                Date(2078,2,11),
                Date(2078,2,23),
                Date(2078,3,21),
                Date(2078,4,29),
                Date(2078,5,3),
                Date(2078,5,4),
                Date(2078,5,5),
                Date(2078,7,18),
                Date(2078,8,11),
                Date(2078,9,19),
                Date(2078,9,22),
                Date(2078,10,10),
                Date(2078,11,3),
                Date(2078,11,23),
                Date(2078,12,31),
                Date(2079,1,1),
                Date(2079,1,2),
                Date(2079,1,3),
                Date(2079,1,9),
                Date(2079,2,11),
                Date(2079,2,23),
                Date(2079,3,20),
                Date(2079,4,29),
                Date(2079,5,3),
                Date(2079,5,4),
                Date(2079,5,5),
                Date(2079,7,17),
                Date(2079,8,11),
                Date(2079,9,18),
                Date(2079,9,23),
                Date(2079,10,9),
                Date(2079,11,3),
                Date(2079,11,23),
                Date(2079,12,31),
            ]
        elif year >= 2080 and year < 2090:
            tokyo_holidays = [
                Date(2080,1,1),
                Date(2080,1,2),
                Date(2080,1,3),
                Date(2080,1,8),
                Date(2080,2,12),
                Date(2080,2,23),
                Date(2080,3,20),
                Date(2080,4,29),
                Date(2080,5,3),
                Date(2080,5,4),
                Date(2080,5,6),
                Date(2080,7,15),
                Date(2080,8,12),
                Date(2080,9,16),
                Date(2080,9,23),
                Date(2080,10,14),
                Date(2080,11,4),
                Date(2080,11,23),
                Date(2080,12,31),
                Date(2081,1,1),
                Date(2081,1,2),
                Date(2081,1,3),
                Date(2081,1,13),
                Date(2081,2,11),
                Date(2081,2,23),
                Date(2081,2,24),
                Date(2081,3,20),
                Date(2081,4,29),
                Date(2081,5,3),
                Date(2081,5,4),
                Date(2081,5,5),
                Date(2081,5,6),
                Date(2081,7,21),
                Date(2081,8,11),
                Date(2081,9,15),
                Date(2081,9,22),
                Date(2081,10,13),
                Date(2081,11,3),
                Date(2081,11,24),
                Date(2081,12,31),
                Date(2082,1,1),
                Date(2082,1,2),
                Date(2082,1,3),
                Date(2082,1,12),
                Date(2082,2,11),
                Date(2082,2,23),
                Date(2082,3,20),
                Date(2082,4,29),
                Date(2082,5,3),
                Date(2082,5,4),
                Date(2082,5,5),
                Date(2082,5,6),
                Date(2082,7,20),
                Date(2082,8,11),
                Date(2082,9,21),
                Date(2082,9,22),
                Date(2082,10,12),
                Date(2082,11,3),
                Date(2082,11,23),
                Date(2082,12,31),
                Date(2083,1,1),
                Date(2083,1,2),
                Date(2083,1,3),
                Date(2083,1,11),
                Date(2083,2,11),
                Date(2083,2,23),
                Date(2083,3,20),
                Date(2083,4,29),
                Date(2083,5,3),
                Date(2083,5,4),
                Date(2083,5,5),
                Date(2083,7,19),
                Date(2083,8,11),
                Date(2083,9,20),
                Date(2083,9,23),
                Date(2083,10,11),
                Date(2083,11,3),
                Date(2083,11,23),
                Date(2083,12,31),
                Date(2084,1,1),
                Date(2084,1,2),
                Date(2084,1,3),
                Date(2084,1,10),
                Date(2084,2,11),
                Date(2084,2,23),
                Date(2084,3,20),
                Date(2084,4,29),
                Date(2084,5,3),
                Date(2084,5,4),
                Date(2084,5,5),
                Date(2084,7,17),
                Date(2084,8,11),
                Date(2084,9,18),
                Date(2084,9,22),
                Date(2084,10,9),
                Date(2084,11,3),
                Date(2084,11,23),
                Date(2084,12,31),
                Date(2085,1,1),
                Date(2085,1,2),
                Date(2085,1,3),
                Date(2085,1,8),
                Date(2085,2,12),
                Date(2085,2,23),
                Date(2085,3,20),
                Date(2085,4,30),
                Date(2085,5,3),
                Date(2085,5,4),
                Date(2085,5,5),
                Date(2085,7,16),
                Date(2085,8,11),
                Date(2085,9,17),
                Date(2085,9,22),
                Date(2085,10,8),
                Date(2085,11,3),
                Date(2085,11,23),
                Date(2085,12,31),
                Date(2086,1,1),
                Date(2086,1,2),
                Date(2086,1,3),
                Date(2086,1,14),
                Date(2086,2,11),
                Date(2086,2,23),
                Date(2086,3,20),
                Date(2086,4,29),
                Date(2086,5,3),
                Date(2086,5,4),
                Date(2086,5,6),
                Date(2086,7,15),
                Date(2086,8,12),
                Date(2086,9,16),
                Date(2086,9,23),
                Date(2086,10,14),
                Date(2086,11,4),
                Date(2086,11,23),
                Date(2086,12,31),
                Date(2087,1,1),
                Date(2087,1,2),
                Date(2087,1,3),
                Date(2087,1,13),
                Date(2087,2,11),
                Date(2087,2,23),
                Date(2087,2,24),
                Date(2087,3,20),
                Date(2087,4,29),
                Date(2087,5,3),
                Date(2087,5,4),
                Date(2087,5,5),
                Date(2087,5,6),
                Date(2087,7,21),
                Date(2087,8,11),
                Date(2087,9,15),
                Date(2087,9,23),
                Date(2087,10,13),
                Date(2087,11,3),
                Date(2087,11,24),
                Date(2087,12,31),
                Date(2088,1,1),
                Date(2088,1,2),
                Date(2088,1,3),
                Date(2088,1,12),
                Date(2088,2,11),
                Date(2088,2,23),
                Date(2088,3,20),
                Date(2088,4,29),
                Date(2088,5,3),
                Date(2088,5,4),
                Date(2088,5,5),
                Date(2088,7,19),
                Date(2088,8,11),
                Date(2088,9,20),
                Date(2088,9,22),
                Date(2088,10,11),
                Date(2088,11,3),
                Date(2088,11,23),
                Date(2088,12,31),
                Date(2089,1,1),
                Date(2089,1,2),
                Date(2089,1,3),
                Date(2089,1,10),
                Date(2089,2,11),
                Date(2089,2,23),
                Date(2089,3,21),
                Date(2089,4,29),
                Date(2089,5,3),
                Date(2089,5,4),
                Date(2089,5,5),
                Date(2089,7,18),
                Date(2089,8,11),
                Date(2089,9,19),
                Date(2089,9,22),
                Date(2089,10,10),
                Date(2089,11,3),
                Date(2089,11,23),
                Date(2089,12,31),
            ]
        elif year >= 2090 and year < 2100:
            tokyo_holidays = [
                Date(2090,1,1),
                Date(2090,1,2),
                Date(2090,1,3),
                Date(2090,1,9),
                Date(2090,2,11),
                Date(2090,2,23),
                Date(2090,3,20),
                Date(2090,4,29),
                Date(2090,5,3),
                Date(2090,5,4),
                Date(2090,5,5),
                Date(2090,7,17),
                Date(2090,8,11),
                Date(2090,9,18),
                Date(2090,9,22),
                Date(2090,10,9),
                Date(2090,11,3),
                Date(2090,11,23),
                Date(2090,12,31),
                Date(2091,1,1),
                Date(2091,1,2),
                Date(2091,1,3),
                Date(2091,1,8),
                Date(2091,2,12),
                Date(2091,2,23),
                Date(2091,3,20),
                Date(2091,4,30),
                Date(2091,5,3),
                Date(2091,5,4),
                Date(2091,5,5),
                Date(2091,7,16),
                Date(2091,8,11),
                Date(2091,9,17),
                Date(2091,9,24),
                Date(2091,10,8),
                Date(2091,11,3),
                Date(2091,11,23),
                Date(2091,12,31),
                Date(2092,1,1),
                Date(2092,1,2),
                Date(2092,1,3),
                Date(2092,1,14),
                Date(2092,2,11),
                Date(2092,2,23),
                Date(2092,3,19),
                Date(2092,4,29),
                Date(2092,5,3),
                Date(2092,5,4),
                Date(2092,5,5),
                Date(2092,5,6),
                Date(2092,7,21),
                Date(2092,8,11),
                Date(2092,9,15),
                Date(2092,9,22),
                Date(2092,10,13),
                Date(2092,11,3),
                Date(2092,11,24),
                Date(2092,12,31),
                Date(2093,1,1),
                Date(2093,1,2),
                Date(2093,1,3),
                Date(2093,1,12),
                Date(2093,2,11),
                Date(2093,2,23),
                Date(2093,3,20),
                Date(2093,4,29),
                Date(2093,5,3),
                Date(2093,5,4),
                Date(2093,5,5),
                Date(2093,5,6),
                Date(2093,7,20),
                Date(2093,8,11),
                Date(2093,9,21),
                Date(2093,9,22),
                Date(2093,10,12),
                Date(2093,11,3),
                Date(2093,11,23),
                Date(2093,12,31),
                Date(2094,1,1),
                Date(2094,1,2),
                Date(2094,1,3),
                Date(2094,1,11),
                Date(2094,2,11),
                Date(2094,2,23),
                Date(2094,3,20),
                Date(2094,4,29),
                Date(2094,5,3),
                Date(2094,5,4),
                Date(2094,5,5),
                Date(2094,7,19),
                Date(2094,8,11),
                Date(2094,9,20),
                Date(2094,9,22),
                Date(2094,10,11),
                Date(2094,11,3),
                Date(2094,11,23),
                Date(2094,12,31),
                Date(2095,1,1),
                Date(2095,1,2),
                Date(2095,1,3),
                Date(2095,1,10),
                Date(2095,2,11),
                Date(2095,2,23),
                Date(2095,3,21),
                Date(2095,4,29),
                Date(2095,5,3),
                Date(2095,5,4),
                Date(2095,5,5),
                Date(2095,7,18),
                Date(2095,8,11),
                Date(2095,9,19),
                Date(2095,9,23),
                Date(2095,10,10),
                Date(2095,11,3),
                Date(2095,11,23),
                Date(2095,12,31),
                Date(2096,1,1),
                Date(2096,1,2),
                Date(2096,1,3),
                Date(2096,1,9),
                Date(2096,2,11),
                Date(2096,2,23),
                Date(2096,3,19),
                Date(2096,4,30),
                Date(2096,5,3),
                Date(2096,5,4),
                Date(2096,5,5),
                Date(2096,7,16),
                Date(2096,8,11),
                Date(2096,9,17),
                Date(2096,9,22),
                Date(2096,10,8),
                Date(2096,11,3),
                Date(2096,11,23),
                Date(2096,12,31),
                Date(2097,1,1),
                Date(2097,1,2),
                Date(2097,1,3),
                Date(2097,1,14),
                Date(2097,2,11),
                Date(2097,2,23),
                Date(2097,3,20),
                Date(2097,4,29),
                Date(2097,5,3),
                Date(2097,5,4),
                Date(2097,5,6),
                Date(2097,7,15),
                Date(2097,8,12),
                Date(2097,9,16),
                Date(2097,9,23),
                Date(2097,10,14),
                Date(2097,11,4),
                Date(2097,11,23),
                Date(2097,12,31),
                Date(2098,1,1),
                Date(2098,1,2),
                Date(2098,1,3),
                Date(2098,1,13),
                Date(2098,2,11),
                Date(2098,2,23),
                Date(2098,2,24),
                Date(2098,3,20),
                Date(2098,4,29),
                Date(2098,5,3),
                Date(2098,5,4),
                Date(2098,5,5),
                Date(2098,5,6),
                Date(2098,7,21),
                Date(2098,8,11),
                Date(2098,9,15),
                Date(2098,9,22),
                Date(2098,10,13),
                Date(2098,11,3),
                Date(2098,11,24),
                Date(2098,12,31),
                Date(2099,1,1),
                Date(2099,1,2),
                Date(2099,1,3),
                Date(2099,1,12),
                Date(2099,2,11),
                Date(2099,2,23),
                Date(2099,3,20),
                Date(2099,4,29),
                Date(2099,5,3),
                Date(2099,5,4),
                Date(2099,5,5),
                Date(2099,5,6),
                Date(2099,7,20),
                Date(2099,8,11),
                Date(2099,9,21),
                Date(2099,9,23),
                Date(2099,10,12),
                Date(2099,11,3),
                Date(2099,11,23),
                Date(2099,12,31)
            ]
        else:
            raise FinError("Year not supported")
        if dt in tokyo_holidays:
            return True
        return False

    ###############################################################################

    def holiday_new_zealand(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 2 and weekday == Date.MON:  # new years day
            return True

        if m == 1 and d == 3 and weekday == Date.MON:  # new years day
            return True

        if m == 1 and d > 18 and d < 26 and weekday == Date.MON:  # Anniversary
            return True

        if m == 2 and d == 6:  # Waitanga day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em - 3:  # good friday
            return True

        if day_in_year == em:  # Easter Monday
            return True

        if m == 4 and d == 25:  # ANZAC day
            return True

        if m == 6 and d < 8 and weekday == Date.MON:  # Queen
            return True

        if m == 10 and d > 21 and d < 29 and weekday == Date.MON:  # LABOR DAY
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26 and weekday == Date.MON:  # Xmas
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Boxing
            return True

        if m == 12 and d == 28 and weekday == Date.MON:  # Boxing
            return True

        return False

    ###############################################################################

    def holiday_norway(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # new years day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em - 4:  # holy thursday
            return True

        if day_in_year == em - 3:  # good friday
            return True

        if day_in_year == em:  # Easter Monday
            return True

        if day_in_year == em + 38:  # Ascension
            return True

        if day_in_year == em + 49:  # Pentecost
            return True

        if m == 5 and d == 1:  # May day
            return True

        if m == 5 and d == 17:  # Independence day
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        return False

    ###############################################################################

    def holiday_united_states(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday.
        This is a generic US calendar that contains the superset of
        holidays for bond markets, NYSE, and public holidays. For each of
        these and other categories there will be some variations. """

        m = dt.m
        d = dt.d
        weekday = self.weekday

        if m == 1 and d == 1:  # NYD
            return True

        if m == 1 and d == 2 and weekday == Date.MON:  # NYD
            return True

        if m == 1 and d == 3 and weekday == Date.MON:  # NYD
            return True

        if m == 1 and d >= 15 and d < 22 and weekday == Date.MON:  # MLK
            return True

        if m == 2 and d >= 15 and d < 22 and weekday == Date.MON:  # GW
            return True

        if m == 5 and d >= 25 and d <= 31 and weekday == Date.MON:  # MD
            return True

        if m == 7 and d == 4:  # Indep day
            return True

        if m == 7 and d == 5 and weekday == Date.MON:  # Indep day
            return True

        if m == 7 and d == 3 and weekday == Date.FRI:  # Indep day
            return True

        if m == 9 and d >= 1 and d < 8 and weekday == Date.MON:  # Lab
            return True

        if m == 10 and d >= 8 and d < 15 and weekday == Date.MON:  # CD
            return True

        if m == 11 and d == 11:  # Veterans day
            return True

        if m == 11 and d == 12 and weekday == Date.MON:  # Vets
            return True

        if m == 11 and d == 10 and weekday == Date.FRI:  # Vets
            return True

        if m == 11 and d >= 22 and d < 29 and weekday == Date.THU:  # TG
            return True

        if m == 12 and d == 24 and weekday == Date.FRI:  # Xmas holiday
            return True

        if m == 12 and d == 25:  # Xmas holiday
            return True

        if m == 12 and d == 26 and weekday == Date.MON:  # Xmas holiday
            return True

        if m == 12 and d == 31 and weekday == Date.FRI:
            return True

        return False

    ###############################################################################

    def holiday_newyork(self, dt):
        newyork_holidays = [
            Date(2010,1,1),
            Date(2010,1,18),
            Date(2010,2,17),
            Date(2010,5,31),
            Date(2010,6,18),
            Date(2010,6,19),
            Date(2010,7,4),
            Date(2010,7,5),
            Date(2010,9,6),
            Date(2010,10,11),
            Date(2010,11,11),
            Date(2010,11,25),
            Date(2010,12,24),
            Date(2011,1,1),
            Date(2011,1,17),
            Date(2011,2,16),
            Date(2011,5,30),
            Date(2011,6,19),
            Date(2011,6,20),
            Date(2011,7,4),
            Date(2011,9,5),
            Date(2011,10,10),
            Date(2011,11,11),
            Date(2011,11,24),
            Date(2011,12,26),
            Date(2012,1,2),
            Date(2012,1,16),
            Date(2012,2,15),
            Date(2012,5,28),
            Date(2012,6,19),
            Date(2012,7,4),
            Date(2012,9,3),
            Date(2012,10,8),
            Date(2012,11,12),
            Date(2012,11,22),
            Date(2012,12,25),
            Date(2013,1,1),
            Date(2013,1,21),
            Date(2013,2,20),
            Date(2013,5,27),
            Date(2013,6,19),
            Date(2013,7,4),
            Date(2013,9,2),
            Date(2013,10,14),
            Date(2013,11,11),
            Date(2013,11,28),
            Date(2013,12,25),
            Date(2014,1,1),
            Date(2014,1,20),
            Date(2014,2,19),
            Date(2014,5,26),
            Date(2014,6,19),
            Date(2014,7,4),
            Date(2014,9,1),
            Date(2014,10,13),
            Date(2014,11,11),
            Date(2014,11,27),
            Date(2014,12,25),
            Date(2015,1,1),
            Date(2015,1,19),
            Date(2015,2,18),
            Date(2015,5,25),
            Date(2015,6,19),
            Date(2015,7,3),
            Date(2015,7,4),
            Date(2015,9,7),
            Date(2015,10,12),
            Date(2015,11,11),
            Date(2015,11,26),
            Date(2015,12,25),
            Date(2016,1,1),
            Date(2016,1,18),
            Date(2016,2,17),
            Date(2016,5,30),
            Date(2016,6,19),
            Date(2016,6,20),
            Date(2016,7,4),
            Date(2016,9,5),
            Date(2016,10,10),
            Date(2016,11,11),
            Date(2016,11,24),
            Date(2016,12,26),
            Date(2017,1,2),
            Date(2017,1,16),
            Date(2017,2,15),
            Date(2017,5,29),
            Date(2017,6,19),
            Date(2017,7,4),
            Date(2017,9,4),
            Date(2017,10,9),
            Date(2017,11,11),
            Date(2017,11,23),
            Date(2017,12,25),
            Date(2018,1,1),
            Date(2018,1,15),
            Date(2018,2,21),
            Date(2018,5,28),
            Date(2018,6,19),
            Date(2018,7,4),
            Date(2018,9,3),
            Date(2018,10,8),
            Date(2018,11,12),
            Date(2018,11,22),
            Date(2018,12,25),
            Date(2019,1,1),
            Date(2019,1,21),
            Date(2019,2,20),
            Date(2019,5,27),
            Date(2019,6,19),
            Date(2019,7,4),
            Date(2019,9,2),
            Date(2019,10,14),
            Date(2019,11,11),
            Date(2019,11,28),
            Date(2019,12,25),
            Date(2020,1,1),
            Date(2020,1,20),
            Date(2020,2,19),
            Date(2020,5,25),
            Date(2020,6,19),
            Date(2020,7,3),
            Date(2020,7,4),
            Date(2020,9,7),
            Date(2020,10,12),
            Date(2020,11,11),
            Date(2020,11,26),
            Date(2020,12,25),
            Date(2021,1,1),
            Date(2021,1,18),
            Date(2021,2,17),
            Date(2021,5,31),
            Date(2021,6,18),
            Date(2021,6,19),
            Date(2021,7,4),
            Date(2021,7,5),
            Date(2021,9,6),
            Date(2021,10,11),
            Date(2021,11,11),
            Date(2021,11,25),
            Date(2021,12,24),
            Date(2022,1,1),
            Date(2022,1,17),
            Date(2022,2,16),
            Date(2022,5,30),
            Date(2022,6,19),
            Date(2022,6,20),
            Date(2022,7,4),
            Date(2022,9,5),
            Date(2022,10,10),
            Date(2022,11,11),
            Date(2022,11,24),
            Date(2022,12,26),
            Date(2023,1,2),
            Date(2023,1,16),
            Date(2023,2,15),
            Date(2023,5,29),
            Date(2023,6,19),
            Date(2023,7,4),
            Date(2023,9,4),
            Date(2023,10,9),
            Date(2023,11,11),
            Date(2023,11,23),
            Date(2023,12,25),
            Date(2024,1,1),
            Date(2024,1,15),
            Date(2024,2,21),
            Date(2024,5,27),
            Date(2024,6,19),
            Date(2024,7,4),
            Date(2024,9,2),
            Date(2024,10,14),
            Date(2024,11,11),
            Date(2024,11,28),
            Date(2024,12,25),
            Date(2025,1,1),
            Date(2025,1,9),
            Date(2025,1,20),
            Date(2025,2,19),
            Date(2025,5,26),
            Date(2025,6,19),
            Date(2025,7,4),
            Date(2025,9,1),
            Date(2025,10,13),
            Date(2025,11,11),
            Date(2025,11,27),
            Date(2025,12,25),
            Date(2026,1,1),
            Date(2026,1,19),
            Date(2026,2,18),
            Date(2026,5,25),
            Date(2026,6,19),
            Date(2026,7,3),
            Date(2026,7,4),
            Date(2026,9,7),
            Date(2026,10,12),
            Date(2026,11,11),
            Date(2026,11,26),
            Date(2026,12,25),
            Date(2027,1,1),
            Date(2027,1,18),
            Date(2027,2,17),
            Date(2027,5,31),
            Date(2027,6,18),
            Date(2027,6,19),
            Date(2027,7,4),
            Date(2027,7,5),
            Date(2027,9,6),
            Date(2027,10,11),
            Date(2027,11,11),
            Date(2027,11,25),
            Date(2027,12,24),
            Date(2028,1,1),
            Date(2028,1,17),
            Date(2028,2,16),
            Date(2028,5,29),
            Date(2028,6,19),
            Date(2028,7,4),
            Date(2028,9,4),
            Date(2028,10,9),
            Date(2028,11,11),
            Date(2028,11,23),
            Date(2028,12,25),
            Date(2029,1,1),
            Date(2029,1,15),
            Date(2029,2,21),
            Date(2029,5,28),
            Date(2029,6,19),
            Date(2029,7,4),
            Date(2029,9,3),
            Date(2029,10,8),
            Date(2029,11,12),
            Date(2029,11,22),
            Date(2029,12,25),
            Date(2030,1,1),
            Date(2030,1,21),
            Date(2030,2,20),
            Date(2030,5,27),
            Date(2030,6,19),
            Date(2030,7,4),
            Date(2030,9,2),
            Date(2030,10,14),
            Date(2030,11,11),
            Date(2030,11,28),
            Date(2030,12,25),
            Date(2031,1,1),
            Date(2031,1,20),
            Date(2031,2,19),
            Date(2031,5,26),
            Date(2031,6,19),
            Date(2031,7,4),
            Date(2031,9,1),
            Date(2031,10,13),
            Date(2031,11,11),
            Date(2031,11,27),
            Date(2031,12,25),
            Date(2032,1,1),
            Date(2032,1,19),
            Date(2032,2,18),
            Date(2032,5,31),
            Date(2032,6,18),
            Date(2032,6,19),
            Date(2032,7,4),
            Date(2032,7,5),
            Date(2032,9,6),
            Date(2032,10,11),
            Date(2032,11,11),
            Date(2032,11,25),
            Date(2032,12,24),
            Date(2033,1,1),
            Date(2033,1,17),
            Date(2033,2,16),
            Date(2033,5,30),
            Date(2033,6,19),
            Date(2033,6,20),
            Date(2033,7,4),
            Date(2033,9,5),
            Date(2033,10,10),
            Date(2033,11,11),
            Date(2033,11,24),
            Date(2033,12,26),
            Date(2034,1,2),
            Date(2034,1,16),
            Date(2034,2,15),
            Date(2034,5,29),
            Date(2034,6,19),
            Date(2034,7,4),
            Date(2034,9,4),
            Date(2034,10,9),
            Date(2034,11,11),
            Date(2034,11,23),
            Date(2034,12,25),
            Date(2035,1,1),
            Date(2035,1,15),
            Date(2035,2,21),
            Date(2035,5,28),
            Date(2035,6,19),
            Date(2035,7,4),
            Date(2035,9,3),
            Date(2035,10,8),
            Date(2035,11,12),
            Date(2035,11,22),
            Date(2035,12,25),
            Date(2036,1,1),
            Date(2036,1,21),
            Date(2036,2,20),
            Date(2036,5,26),
            Date(2036,6,19),
            Date(2036,7,4),
            Date(2036,9,1),
            Date(2036,10,13),
            Date(2036,11,11),
            Date(2036,11,27),
            Date(2036,12,25),
            Date(2037,1,1),
            Date(2037,1,19),
            Date(2037,2,18),
            Date(2037,5,25),
            Date(2037,6,19),
            Date(2037,7,3),
            Date(2037,7,4),
            Date(2037,9,7),
            Date(2037,10,12),
            Date(2037,11,11),
            Date(2037,11,26),
            Date(2037,12,25),
            Date(2038,1,1),
            Date(2038,1,18),
            Date(2038,2,17),
            Date(2038,5,31),
            Date(2038,6,18),
            Date(2038,6,19),
            Date(2038,7,4),
            Date(2038,7,5),
            Date(2038,9,6),
            Date(2038,10,11),
            Date(2038,11,11),
            Date(2038,11,25),
            Date(2038,12,24),
            Date(2039,1,1),
            Date(2039,1,17),
            Date(2039,2,16),
            Date(2039,5,30),
            Date(2039,6,19),
            Date(2039,6,20),
            Date(2039,7,4),
            Date(2039,9,5),
            Date(2039,10,10),
            Date(2039,11,11),
            Date(2039,11,24),
            Date(2039,12,26),
            Date(2040,1,2),
            Date(2040,1,16),
            Date(2040,2,15),
            Date(2040,5,28),
            Date(2040,6,19),
            Date(2040,7,4),
            Date(2040,9,3),
            Date(2040,10,8),
            Date(2040,11,12),
            Date(2040,11,22),
            Date(2040,12,25),
            Date(2041,1,1),
            Date(2041,1,21),
            Date(2041,2,20),
            Date(2041,5,27),
            Date(2041,6,19),
            Date(2041,7,4),
            Date(2041,9,2),
            Date(2041,10,14),
            Date(2041,11,11),
            Date(2041,11,28),
            Date(2041,12,25),
            Date(2042,1,1),
            Date(2042,1,20),
            Date(2042,2,19),
            Date(2042,5,26),
            Date(2042,6,19),
            Date(2042,7,4),
            Date(2042,9,1),
            Date(2042,10,13),
            Date(2042,11,11),
            Date(2042,11,27),
            Date(2042,12,25),
            Date(2043,1,1),
            Date(2043,1,19),
            Date(2043,2,18),
            Date(2043,5,25),
            Date(2043,6,19),
            Date(2043,7,3),
            Date(2043,7,4),
            Date(2043,9,7),
            Date(2043,10,12),
            Date(2043,11,11),
            Date(2043,11,26),
            Date(2043,12,25),
            Date(2044,1,1),
            Date(2044,1,18),
            Date(2044,2,17),
            Date(2044,5,30),
            Date(2044,6,19),
            Date(2044,6,20),
            Date(2044,7,4),
            Date(2044,9,5),
            Date(2044,10,10),
            Date(2044,11,11),
            Date(2044,11,24),
            Date(2044,12,26),
            Date(2045,1,2),
            Date(2045,1,16),
            Date(2045,2,15),
            Date(2045,5,29),
            Date(2045,6,19),
            Date(2045,7,4),
            Date(2045,9,4),
            Date(2045,10,9),
            Date(2045,11,11),
            Date(2045,11,23),
            Date(2045,12,25),
            Date(2046,1,1),
            Date(2046,1,15),
            Date(2046,2,21),
            Date(2046,5,28),
            Date(2046,6,19),
            Date(2046,7,4),
            Date(2046,9,3),
            Date(2046,10,8),
            Date(2046,11,12),
            Date(2046,11,22),
            Date(2046,12,25),
            Date(2047,1,1),
            Date(2047,1,21),
            Date(2047,2,20),
            Date(2047,5,27),
            Date(2047,6,19),
            Date(2047,7,4),
            Date(2047,9,2),
            Date(2047,10,14),
            Date(2047,11,11),
            Date(2047,11,28),
            Date(2047,12,25),
            Date(2048,1,1),
            Date(2048,1,20),
            Date(2048,2,19),
            Date(2048,5,25),
            Date(2048,6,19),
            Date(2048,7,3),
            Date(2048,7,4),
            Date(2048,9,7),
            Date(2048,10,12),
            Date(2048,11,11),
            Date(2048,11,26),
            Date(2048,12,25),
            Date(2049,1,1),
            Date(2049,1,18),
            Date(2049,2,17),
            Date(2049,5,31),
            Date(2049,6,18),
            Date(2049,6,19),
            Date(2049,7,4),
            Date(2049,7,5),
            Date(2049,9,6),
            Date(2049,10,11),
            Date(2049,11,11),
            Date(2049,11,25),
            Date(2049,12,24),
            Date(2050,1,1),
            Date(2050,1,17),
            Date(2050,2,16),
            Date(2050,5,30),
            Date(2050,6,19),
            Date(2050,6,20),
            Date(2050,7,4),
            Date(2050,9,5),
            Date(2050,10,10),
            Date(2050,11,11),
            Date(2050,11,24),
            Date(2050,12,26),
            Date(2051,1,2),
            Date(2051,1,16),
            Date(2051,2,15),
            Date(2051,5,29),
            Date(2051,6,19),
            Date(2051,7,4),
            Date(2051,9,4),
            Date(2051,10,9),
            Date(2051,11,11),
            Date(2051,11,23),
            Date(2051,12,25),
            Date(2052,1,1),
            Date(2052,1,15),
            Date(2052,2,21),
            Date(2052,5,27),
            Date(2052,6,19),
            Date(2052,7,4),
            Date(2052,9,2),
            Date(2052,10,14),
            Date(2052,11,11),
            Date(2052,11,28),
            Date(2052,12,25),
            Date(2053,1,1),
            Date(2053,1,20),
            Date(2053,2,19),
            Date(2053,5,26),
            Date(2053,6,19),
            Date(2053,7,4),
            Date(2053,9,1),
            Date(2053,10,13),
            Date(2053,11,11),
            Date(2053,11,27),
            Date(2053,12,25),
            Date(2054,1,1),
            Date(2054,1,19),
            Date(2054,2,18),
            Date(2054,5,25),
            Date(2054,6,19),
            Date(2054,7,3),
            Date(2054,7,4),
            Date(2054,9,7),
            Date(2054,10,12),
            Date(2054,11,11),
            Date(2054,11,26),
            Date(2054,12,25),
            Date(2055,1,1),
            Date(2055,1,18),
            Date(2055,2,17),
            Date(2055,5,31),
            Date(2055,6,18),
            Date(2055,6,19),
            Date(2055,7,4),
            Date(2055,7,5),
            Date(2055,9,6),
            Date(2055,10,11),
            Date(2055,11,11),
            Date(2055,11,25),
            Date(2055,12,24),
            Date(2056,1,1),
            Date(2056,1,17),
            Date(2056,2,16),
            Date(2056,5,29),
            Date(2056,6,19),
            Date(2056,7,4),
            Date(2056,9,4),
            Date(2056,10,9),
            Date(2056,11,11),
            Date(2056,11,23),
            Date(2056,12,25),
            Date(2057,1,1),
            Date(2057,1,15),
            Date(2057,2,21),
            Date(2057,5,28),
            Date(2057,6,19),
            Date(2057,7,4),
            Date(2057,9,3),
            Date(2057,10,8),
            Date(2057,11,12),
            Date(2057,11,22),
            Date(2057,12,25),
            Date(2058,1,1),
            Date(2058,1,21),
            Date(2058,2,20),
            Date(2058,5,27),
            Date(2058,6,19),
            Date(2058,7,4),
            Date(2058,9,2),
            Date(2058,10,14),
            Date(2058,11,11),
            Date(2058,11,28),
            Date(2058,12,25),
            Date(2059,1,1),
            Date(2059,1,20),
            Date(2059,2,19),
            Date(2059,5,26),
            Date(2059,6,19),
            Date(2059,7,4),
            Date(2059,9,1),
            Date(2059,10,13),
            Date(2059,11,11),
            Date(2059,11,27),
            Date(2059,12,25),
            Date(2060,1,1),
            Date(2060,1,19),
            Date(2060,2,18),
            Date(2060,5,31),
            Date(2060,6,18),
            Date(2060,6,19),
            Date(2060,7,4),
            Date(2060,7,5),
            Date(2060,9,6),
            Date(2060,10,11),
            Date(2060,11,11),
            Date(2060,11,25),
            Date(2060,12,24),
            Date(2061,1,1),
            Date(2061,1,17),
            Date(2061,2,16),
            Date(2061,5,30),
            Date(2061,6,19),
            Date(2061,6,20),
            Date(2061,7,4),
            Date(2061,9,5),
            Date(2061,10,10),
            Date(2061,11,11),
            Date(2061,11,24),
            Date(2061,12,26),
            Date(2062,1,2),
            Date(2062,1,16),
            Date(2062,2,15),
            Date(2062,5,29),
            Date(2062,6,19),
            Date(2062,7,4),
            Date(2062,9,4),
            Date(2062,10,9),
            Date(2062,11,11),
            Date(2062,11,23),
            Date(2062,12,25),
            Date(2063,1,1),
            Date(2063,1,15),
            Date(2063,2,21),
            Date(2063,5,28),
            Date(2063,6,19),
            Date(2063,7,4),
            Date(2063,9,3),
            Date(2063,10,8),
            Date(2063,11,12),
            Date(2063,11,22),
            Date(2063,12,25),
            Date(2064,1,1),
            Date(2064,1,21),
            Date(2064,2,20),
            Date(2064,5,26),
            Date(2064,6,19),
            Date(2064,7,4),
            Date(2064,9,1),
            Date(2064,10,13),
            Date(2064,11,11),
            Date(2064,11,27),
            Date(2064,12,25),
            Date(2065,1,1),
            Date(2065,1,19),
            Date(2065,2,18),
            Date(2065,5,25),
            Date(2065,6,19),
            Date(2065,7,3),
            Date(2065,7,4),
            Date(2065,9,7),
            Date(2065,10,12),
            Date(2065,11,11),
            Date(2065,11,26),
            Date(2065,12,25),
            Date(2066,1,1),
            Date(2066,1,18),
            Date(2066,2,17),
            Date(2066,5,31),
            Date(2066,6,18),
            Date(2066,6,19),
            Date(2066,7,4),
            Date(2066,7,5),
            Date(2066,9,6),
            Date(2066,10,11),
            Date(2066,11,11),
            Date(2066,11,25),
            Date(2066,12,24),
            Date(2067,1,1),
            Date(2067,1,17),
            Date(2067,2,16),
            Date(2067,5,30),
            Date(2067,6,19),
            Date(2067,6,20),
            Date(2067,7,4),
            Date(2067,9,5),
            Date(2067,10,10),
            Date(2067,11,11),
            Date(2067,11,24),
            Date(2067,12,26),
            Date(2068,1,2),
            Date(2068,1,16),
            Date(2068,2,15),
            Date(2068,5,28),
            Date(2068,6,19),
            Date(2068,7,4),
            Date(2068,9,3),
            Date(2068,10,8),
            Date(2068,11,12),
            Date(2068,11,22),
            Date(2068,12,25),
            Date(2069,1,1),
            Date(2069,1,21),
            Date(2069,2,20),
            Date(2069,5,27),
            Date(2069,6,19),
            Date(2069,7,4),
            Date(2069,9,2),
            Date(2069,10,14),
            Date(2069,11,11),
            Date(2069,11,28),
            Date(2069,12,25),
            Date(2070,1,1),
            Date(2070,1,20),
            Date(2070,2,19),
            Date(2070,5,26),
            Date(2070,6,19),
            Date(2070,7,4),
            Date(2070,9,1),
            Date(2070,10,13),
            Date(2070,11,11),
            Date(2070,11,27),
            Date(2070,12,25),
            Date(2071,1,1),
            Date(2071,1,19),
            Date(2071,2,18),
            Date(2071,5,25),
            Date(2071,6,19),
            Date(2071,7,3),
            Date(2071,7,4),
            Date(2071,9,7),
            Date(2071,10,12),
            Date(2071,11,11),
            Date(2071,11,26),
            Date(2071,12,25),
            Date(2072,1,1),
            Date(2072,1,18),
            Date(2072,2,17),
            Date(2072,5,30),
            Date(2072,6,19),
            Date(2072,6,20),
            Date(2072,7,4),
            Date(2072,9,5),
            Date(2072,10,10),
            Date(2072,11,11),
            Date(2072,11,24),
            Date(2072,12,26),
            Date(2073,1,2),
            Date(2073,1,16),
            Date(2073,2,15),
            Date(2073,5,29),
            Date(2073,6,19),
            Date(2073,7,4),
            Date(2073,9,4),
            Date(2073,10,9),
            Date(2073,11,11),
            Date(2073,11,23),
            Date(2073,12,25),
            Date(2074,1,1),
            Date(2074,1,15),
            Date(2074,2,21),
            Date(2074,5,28),
            Date(2074,6,19),
            Date(2074,7,4),
            Date(2074,9,3),
            Date(2074,10,8),
            Date(2074,11,12),
            Date(2074,11,22),
            Date(2074,12,25),
            Date(2075,1,1),
            Date(2075,1,21),
            Date(2075,2,20),
            Date(2075,5,27),
            Date(2075,6,19),
            Date(2075,7,4),
            Date(2075,9,2),
            Date(2075,10,14),
            Date(2075,11,11),
            Date(2075,11,28),
            Date(2075,12,25),
            Date(2076,1,1),
            Date(2076,1,20),
            Date(2076,2,19),
            Date(2076,5,25),
            Date(2076,6,19),
            Date(2076,7,3),
            Date(2076,7,4),
            Date(2076,9,7),
            Date(2076,10,12),
            Date(2076,11,11),
            Date(2076,11,26),
            Date(2076,12,25),
            Date(2077,1,1),
            Date(2077,1,18),
            Date(2077,2,17),
            Date(2077,5,31),
            Date(2077,6,18),
            Date(2077,6,19),
            Date(2077,7,4),
            Date(2077,7,5),
            Date(2077,9,6),
            Date(2077,10,11),
            Date(2077,11,11),
            Date(2077,11,25),
            Date(2077,12,24),
            Date(2078,1,1),
            Date(2078,1,17),
            Date(2078,2,16),
            Date(2078,5,30),
            Date(2078,6,19),
            Date(2078,6,20),
            Date(2078,7,4),
            Date(2078,9,5),
            Date(2078,10,10),
            Date(2078,11,11),
            Date(2078,11,24),
            Date(2078,12,26),
            Date(2079,1,2),
            Date(2079,1,16),
            Date(2079,2,15),
            Date(2079,5,29),
            Date(2079,6,19),
            Date(2079,7,4),
            Date(2079,9,4),
            Date(2079,10,9),
            Date(2079,11,11),
            Date(2079,11,23),
            Date(2079,12,25),
            Date(2080,1,1),
            Date(2080,1,15),
            Date(2080,2,21),
            Date(2080,5,27),
            Date(2080,6,19),
            Date(2080,7,4),
            Date(2080,9,2),
            Date(2080,10,14),
            Date(2080,11,11),
            Date(2080,11,28),
            Date(2080,12,25),
            Date(2081,1,1),
            Date(2081,1,20),
            Date(2081,2,19),
            Date(2081,5,26),
            Date(2081,6,19),
            Date(2081,7,4),
            Date(2081,9,1),
            Date(2081,10,13),
            Date(2081,11,11),
            Date(2081,11,27),
            Date(2081,12,25),
            Date(2082,1,1),
            Date(2082,1,19),
            Date(2082,2,18),
            Date(2082,5,25),
            Date(2082,6,19),
            Date(2082,7,3),
            Date(2082,7,4),
            Date(2082,9,7),
            Date(2082,10,12),
            Date(2082,11,11),
            Date(2082,11,26),
            Date(2082,12,25),
            Date(2083,1,1),
            Date(2083,1,18),
            Date(2083,2,17),
            Date(2083,5,31),
            Date(2083,6,18),
            Date(2083,6,19),
            Date(2083,7,4),
            Date(2083,7,5),
            Date(2083,9,6),
            Date(2083,10,11),
            Date(2083,11,11),
            Date(2083,11,25),
            Date(2083,12,24),
            Date(2084,1,1),
            Date(2084,1,17),
            Date(2084,2,16),
            Date(2084,5,29),
            Date(2084,6,19),
            Date(2084,7,4),
            Date(2084,9,4),
            Date(2084,10,9),
            Date(2084,11,11),
            Date(2084,11,23),
            Date(2084,12,25),
            Date(2085,1,1),
            Date(2085,1,15),
            Date(2085,2,21),
            Date(2085,5,28),
            Date(2085,6,19),
            Date(2085,7,4),
            Date(2085,9,3),
            Date(2085,10,8),
            Date(2085,11,12),
            Date(2085,11,22),
            Date(2085,12,25),
            Date(2086,1,1),
            Date(2086,1,21),
            Date(2086,2,20),
            Date(2086,5,27),
            Date(2086,6,19),
            Date(2086,7,4),
            Date(2086,9,2),
            Date(2086,10,14),
            Date(2086,11,11),
            Date(2086,11,28),
            Date(2086,12,25),
            Date(2087,1,1),
            Date(2087,1,20),
            Date(2087,2,19),
            Date(2087,5,26),
            Date(2087,6,19),
            Date(2087,7,4),
            Date(2087,9,1),
            Date(2087,10,13),
            Date(2087,11,11),
            Date(2087,11,27),
            Date(2087,12,25),
            Date(2088,1,1),
            Date(2088,1,19),
            Date(2088,2,18),
            Date(2088,5,31),
            Date(2088,6,18),
            Date(2088,6,19),
            Date(2088,7,4),
            Date(2088,7,5),
            Date(2088,9,6),
            Date(2088,10,11),
            Date(2088,11,11),
            Date(2088,11,25),
            Date(2088,12,24),
            Date(2089,1,1),
            Date(2089,1,17),
            Date(2089,2,16),
            Date(2089,5,30),
            Date(2089,6,19),
            Date(2089,6,20),
            Date(2089,7,4),
            Date(2089,9,5),
            Date(2089,10,10),
            Date(2089,11,11),
            Date(2089,11,24),
            Date(2089,12,26),
            Date(2090,1,2),
            Date(2090,1,16),
            Date(2090,2,15),
            Date(2090,5,29),
            Date(2090,6,19),
            Date(2090,7,4),
            Date(2090,9,4),
            Date(2090,10,9),
            Date(2090,11,11),
            Date(2090,11,23),
            Date(2090,12,25),
            Date(2091,1,1),
            Date(2091,1,15),
            Date(2091,2,21),
            Date(2091,5,28),
            Date(2091,6,19),
            Date(2091,7,4),
            Date(2091,9,3),
            Date(2091,10,8),
            Date(2091,11,12),
            Date(2091,11,22),
            Date(2091,12,25),
            Date(2092,1,1),
            Date(2092,1,21),
            Date(2092,2,20),
            Date(2092,5,26),
            Date(2092,6,19),
            Date(2092,7,4),
            Date(2092,9,1),
            Date(2092,10,13),
            Date(2092,11,11),
            Date(2092,11,27),
            Date(2092,12,25),
            Date(2093,1,1),
            Date(2093,1,19),
            Date(2093,2,18),
            Date(2093,5,25),
            Date(2093,6,19),
            Date(2093,7,3),
            Date(2093,7,4),
            Date(2093,9,7),
            Date(2093,10,12),
            Date(2093,11,11),
            Date(2093,11,26),
            Date(2093,12,25),
            Date(2094,1,1),
            Date(2094,1,18),
            Date(2094,2,17),
            Date(2094,5,31),
            Date(2094,6,18),
            Date(2094,6,19),
            Date(2094,7,4),
            Date(2094,7,5),
            Date(2094,9,6),
            Date(2094,10,11),
            Date(2094,11,11),
            Date(2094,11,25),
            Date(2094,12,24),
            Date(2095,1,1),
            Date(2095,1,17),
            Date(2095,2,16),
            Date(2095,5,30),
            Date(2095,6,19),
            Date(2095,6,20),
            Date(2095,7,4),
            Date(2095,9,5),
            Date(2095,10,10),
            Date(2095,11,11),
            Date(2095,11,24),
            Date(2095,12,26),
            Date(2096,1,2),
            Date(2096,1,16),
            Date(2096,2,15),
            Date(2096,5,28),
            Date(2096,6,19),
            Date(2096,7,4),
            Date(2096,9,3),
            Date(2096,10,8),
            Date(2096,11,12),
            Date(2096,11,22),
            Date(2096,12,25),
            Date(2097,1,1),
            Date(2097,1,21),
            Date(2097,2,20),
            Date(2097,5,27),
            Date(2097,6,19),
            Date(2097,7,4),
            Date(2097,9,2),
            Date(2097,10,14),
            Date(2097,11,11),
            Date(2097,11,28),
            Date(2097,12,25),
            Date(2098,1,1),
            Date(2098,1,20),
            Date(2098,2,19),
            Date(2098,5,26),
            Date(2098,6,19),
            Date(2098,7,4),
            Date(2098,9,1),
            Date(2098,10,13),
            Date(2098,11,11),
            Date(2098,11,27),
            Date(2098,12,25),
            Date(2099,1,1),
            Date(2099,1,19),
            Date(2099,2,18),
            Date(2099,5,25),
            Date(2099,6,19),
            Date(2099,7,3),
            Date(2099,7,4),
            Date(2099,9,7),
            Date(2099,10,12),
            Date(2099,11,11),
            Date(2099,11,26),
            Date(2099,12,25),
            Date(2100,1,1),
            Date(2100,1,18),
            Date(2100,2,17),
            Date(2100,5,31),
            Date(2100,6,18),
            Date(2100,6,19),
            Date(2100,7,4),
            Date(2100,7,5),
            Date(2100,9,6),
            Date(2100,10,11),
            Date(2100,11,11),
            Date(2100,11,25),
            Date(2100,12,24),
            Date(2101,1,1),
            Date(2101,1,17),
            Date(2101,2,16),
            Date(2101,5,30),
            Date(2101,6,19),
            Date(2101,6,20),
            Date(2101,7,4),
            Date(2101,9,5),
            Date(2101,10,10),
            Date(2101,11,11),
            Date(2101,11,24),
            Date(2101,12,26),
            Date(2102,1,2),
            Date(2102,1,16),
            Date(2102,2,15),
            Date(2102,5,29),
            Date(2102,6,19),
            Date(2102,7,4),
            Date(2102,9,4),
            Date(2102,10,9),
            Date(2102,11,11),
            Date(2102,11,23),
            Date(2102,12,25),
            Date(2103,1,1),
            Date(2103,1,15),
            Date(2103,2,21),
            Date(2103,5,28),
            Date(2103,6,19),
            Date(2103,7,4),
            Date(2103,9,3),
            Date(2103,10,8),
            Date(2103,11,12),
            Date(2103,11,22),
            Date(2103,12,25),
            Date(2104,1,1),
            Date(2104,1,21),
            Date(2104,2,20),
            Date(2104,5,26),
            Date(2104,6,19),
            Date(2104,7,4),
            Date(2104,9,1),
            Date(2104,10,13),
            Date(2104,11,11),
            Date(2104,11,27),
            Date(2104,12,25),
            Date(2105,1,1),
            Date(2105,1,19),
            Date(2105,2,18),
            Date(2105,5,25),
            Date(2105,6,19),
            Date(2105,7,3),
            Date(2105,7,4),
            Date(2105,9,7),
            Date(2105,10,12),
            Date(2105,11,11),
            Date(2105,11,26),
            Date(2105,12,25),
            Date(2106,1,1),
            Date(2106,1,18),
            Date(2106,2,17),
            Date(2106,5,31),
            Date(2106,6,18),
            Date(2106,6,19),
            Date(2106,7,4),
            Date(2106,7,5),
            Date(2106,9,6),
            Date(2106,10,11),
            Date(2106,11,11),
            Date(2106,11,25),
            Date(2106,12,24),
            Date(2107,1,1),
            Date(2107,1,17),
            Date(2107,2,16),
            Date(2107,5,30),
            Date(2107,6,19),
            Date(2107,6,20),
            Date(2107,7,4),
            Date(2107,9,5),
            Date(2107,10,10),
            Date(2107,11,11),
            Date(2107,11,24),
            Date(2107,12,26),
            Date(2108,1,2),
            Date(2108,1,16),
            Date(2108,2,15),
            Date(2108,5,28),
            Date(2108,6,19),
            Date(2108,7,4),
            Date(2108,9,3),
            Date(2108,10,8),
            Date(2108,11,12),
            Date(2108,11,22),
            Date(2108,12,25),
            Date(2109,1,1),
            Date(2109,1,21),
            Date(2109,2,20),
            Date(2109,5,27),
            Date(2109,6,19),
            Date(2109,7,4),
            Date(2109,9,2),
            Date(2109,10,14),
            Date(2109,11,11),
            Date(2109,11,28),
            Date(2109,12,25),
            Date(2110,1,1),
            Date(2110,1,20),
            Date(2110,2,19),
            Date(2110,5,26),
            Date(2110,6,19),
            Date(2110,7,4),
            Date(2110,9,1),
            Date(2110,10,13),
            Date(2110,11,11),
            Date(2110,11,27),
            Date(2110,12,25),
            Date(2111,1,1),
            Date(2111,1,19),
            Date(2111,2,18),
            Date(2111,5,25),
            Date(2111,6,19),
            Date(2111,7,3),
            Date(2111,7,4),
            Date(2111,9,7),
            Date(2111,10,12),
            Date(2111,11,11),
            Date(2111,11,26),
            Date(2111,12,25),
            Date(2112,1,1),
            Date(2112,1,18),
            Date(2112,2,17),
            Date(2112,5,30),
            Date(2112,6,19),
            Date(2112,6,20),
            Date(2112,7,4),
            Date(2112,9,5),
            Date(2112,10,10),
            Date(2112,11,11),
            Date(2112,11,24),
            Date(2112,12,26),
            Date(2113,1,2),
            Date(2113,1,16),
            Date(2113,2,15),
            Date(2113,5,29),
            Date(2113,6,19),
            Date(2113,7,4),
            Date(2113,9,4),
            Date(2113,10,9),
            Date(2113,11,11),
            Date(2113,11,23),
            Date(2113,12,25),
            Date(2114,1,1),
            Date(2114,1,15),
            Date(2114,2,21),
            Date(2114,5,28),
            Date(2114,6,19),
            Date(2114,7,4),
            Date(2114,9,3),
            Date(2114,10,8),
            Date(2114,11,12),
            Date(2114,11,22),
            Date(2114,12,25),
            Date(2115,1,1),
            Date(2115,1,21),
            Date(2115,2,20),
            Date(2115,5,27),
            Date(2115,6,19),
            Date(2115,7,4),
            Date(2115,9,2),
            Date(2115,10,14),
            Date(2115,11,11),
            Date(2115,11,28),
            Date(2115,12,25),
            Date(2116,1,1),
            Date(2116,1,20),
            Date(2116,2,19),
            Date(2116,5,25),
            Date(2116,6,19),
            Date(2116,7,3),
            Date(2116,7,4),
            Date(2116,9,7),
            Date(2116,10,12),
            Date(2116,11,11),
            Date(2116,11,26),
            Date(2116,12,25),
            Date(2117,1,1),
            Date(2117,1,18),
            Date(2117,2,17),
            Date(2117,5,31),
            Date(2117,6,18),
            Date(2117,6,19),
            Date(2117,7,4),
            Date(2117,7,5),
            Date(2117,9,6),
            Date(2117,10,11),
            Date(2117,11,11),
            Date(2117,11,25),
            Date(2117,12,24),
            Date(2118,1,1),
            Date(2118,1,17),
            Date(2118,2,16),
            Date(2118,5,30),
            Date(2118,6,19),
            Date(2118,6,20),
            Date(2118,7,4),
            Date(2118,9,5),
            Date(2118,10,10),
            Date(2118,11,11),
            Date(2118,11,24),
            Date(2118,12,26),
            Date(2119,1,2),
            Date(2119,1,16),
            Date(2119,2,15),
            Date(2119,5,29),
            Date(2119,6,19),
            Date(2119,7,4),
            Date(2119,9,4),
            Date(2119,10,9),
            Date(2119,11,11),
            Date(2119,11,23),
            Date(2119,12,25),
            Date(2120,1,1),
            Date(2120,1,15),
            Date(2120,2,21),
            Date(2120,5,27),
            Date(2120,6,19),
            Date(2120,7,4),
            Date(2120,9,2),
            Date(2120,10,14),
            Date(2120,11,11),
            Date(2120,11,28),
            Date(2120,12,25),
            Date(2121,1,1),
            Date(2121,1,20),
            Date(2121,2,19),
            Date(2121,5,26),
            Date(2121,6,19),
            Date(2121,7,4),
            Date(2121,9,1),
            Date(2121,10,13),
            Date(2121,11,11),
            Date(2121,11,27),
            Date(2121,12,25),
            Date(2122,1,1),
            Date(2122,1,19),
            Date(2122,2,18),
            Date(2122,5,25),
            Date(2122,6,19),
            Date(2122,7,3),
            Date(2122,7,4),
            Date(2122,9,7),
            Date(2122,10,12),
            Date(2122,11,11),
            Date(2122,11,26),
            Date(2122,12,25),
            Date(2123,1,1),
            Date(2123,1,18),
            Date(2123,2,17),
            Date(2123,5,31),
            Date(2123,6,18),
            Date(2123,6,19),
            Date(2123,7,4),
            Date(2123,7,5),
            Date(2123,9,6),
            Date(2123,10,11),
            Date(2123,11,11),
            Date(2123,11,25),
            Date(2123,12,24),
            Date(2124,1,1),
            Date(2124,1,17),
            Date(2124,2,16),
            Date(2124,5,29),
            Date(2124,6,19),
            Date(2124,7,4),
            Date(2124,9,4),
            Date(2124,10,9),
            Date(2124,11,11),
            Date(2124,11,23),
            Date(2124,12,25),
            Date(2125,1,1),
            Date(2125,1,15),
            Date(2125,2,21),
            Date(2125,5,28),
            Date(2125,6,19),
            Date(2125,7,4),
            Date(2125,9,3),
            Date(2125,10,8),
            Date(2125,11,12),
            Date(2125,11,22),
            Date(2125,12,25),
            Date(2126,1,1),
            Date(2126,1,21),
            Date(2126,2,20),
            Date(2126,5,27),
            Date(2126,6,19),
            Date(2126,7,4),
            Date(2126,9,2),
            Date(2126,10,14),
            Date(2126,11,11),
            Date(2126,11,28),
            Date(2126,12,25),
            Date(2127,1,1),
            Date(2127,1,20),
            Date(2127,2,19),
            Date(2127,5,26),
            Date(2127,6,19),
            Date(2127,7,4),
            Date(2127,9,1),
            Date(2127,10,13),
            Date(2127,11,11),
            Date(2127,11,27),
            Date(2127,12,25),
            Date(2128,1,1),
            Date(2128,1,19),
            Date(2128,2,18),
            Date(2128,5,31),
            Date(2128,6,18),
            Date(2128,6,19),
            Date(2128,7,4),
            Date(2128,7,5),
            Date(2128,9,6),
            Date(2128,10,11),
            Date(2128,11,11),
            Date(2128,11,25),
            Date(2128,12,24),
            Date(2129,1,1),
            Date(2129,1,17),
            Date(2129,2,16),
            Date(2129,5,30),
            Date(2129,6,19),
            Date(2129,6,20),
            Date(2129,7,4),
            Date(2129,9,5),
            Date(2129,10,10),
            Date(2129,11,11),
            Date(2129,11,24),
            Date(2129,12,26),
            Date(2130,1,2),
            Date(2130,1,16),
            Date(2130,2,15),
            Date(2130,5,29),
            Date(2130,6,19),
            Date(2130,7,4),
            Date(2130,9,4),
            Date(2130,10,9),
            Date(2130,11,11),
            Date(2130,11,23),
            Date(2130,12,25)
        ]
        if dt in newyork_holidays:
            return True
        return False

    ###############################################################################

    def holiday_canada(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year
        weekday = self.weekday

        if m == 1 and d == 1:  # NYD
            return True

        if m == 1 and d == 2 and weekday == Date.MON:  # NYD
            return True

        if m == 1 and d == 3 and weekday == Date.MON:  # NYD
            return True

        if m == 2 and d >= 15 and d < 22 and weekday == Date.MON:  # FAMILY
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em - 3:  # good friday
            return True

        if m == 5 and d >= 18 and d < 25 and weekday == Date.MON:  # VICTORIA
            return True

        if m == 7 and d == 1:  # Canada day
            return True

        if m == 7 and d == 2 and weekday == Date.MON:  # Canada day
            return True

        if m == 7 and d == 3 and weekday == Date.MON:  # Canada day
            return True

        if m == 8 and d < 8 and weekday == Date.MON:  # Provincial
            return True

        if m == 9 and d < 8 and weekday == Date.MON:  # Labor
            return True

        if m == 10 and d >= 8 and d < 15 and weekday == Date.MON:  # THANKS
            return True

        if m == 11 and d == 11:  # Veterans day
            return True

        if m == 11 and d == 12 and weekday == Date.MON:  # Vets
            return True

        if m == 11 and d == 13 and weekday == Date.MON:  # Vets
            return True

        if m == 12 and d == 25:  # Xmas holiday
            return True

        if m == 12 and d == 26 and weekday == Date.MON:  # Xmas holiday
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Xmas holiday
            return True

        if m == 12 and d == 26:  # Boxing holiday
            return True

        if m == 12 and d == 27 and weekday == Date.MON:  # Boxing holiday
            return True

        if m == 12 and d == 28 and weekday == Date.TUE:  # Boxing holiday
            return True

        return False

    ###############################################################################

    def holiday_italy(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year

        if m == 1 and d == 1:  # new years day
            return True

        if m == 1 and d == 6:  # epiphany
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em:  # Easter Monday
            return True

        if day_in_year == em - 3:  # good friday
            return True

        if m == 4 and d == 25:  # LIBERATION DAY
            return True

        if m == 5 and d == 1:  # LABOUR DAY
            return True

        if m == 6 and d == 2 and y > 1999:  # REPUBLIC DAY
            return True

        if m == 8 and d == 15:  # ASSUMPTION
            return True

        if m == 11 and d == 1:  # ALL SAINTS
            return True

        if m == 12 and d == 8:  # IMMAC CONC
            return True

        if m == 12 and d == 25:  # Xmas
            return True

        if m == 12 and d == 26:  # Boxing day
            return True

        return False

    ###############################################################################

    def holiday_seoul(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """
        korea_holidays = [
            Date(2010,1,1),
            Date(2010,2,15),
            Date(2010,3,1),
            Date(2010,5,5),
            Date(2010,5,21),
            Date(2010,6,2),
            Date(2010,9,21),
            Date(2010,9,22),
            Date(2010,9,23),
            Date(2011,2,2),
            Date(2011,2,3),
            Date(2011,2,4),
            Date(2011,3,1),
            Date(2011,5,5),
            Date(2011,5,10),
            Date(2011,6,6),
            Date(2011,8,15),
            Date(2011,9,12),
            Date(2011,9,13),
            Date(2011,10,3),
            Date(2012,1,23),
            Date(2012,1,24),
            Date(2012,3,1),
            Date(2012,4,11),
            Date(2012,5,1),
            Date(2012,5,28),
            Date(2012,6,6),
            Date(2012,8,15),
            Date(2012,10,1),
            Date(2012,10,3),
            Date(2012,12,19),
            Date(2012,12,25),
            Date(2013,1,1),
            Date(2013,2,11),
            Date(2013,3,1),
            Date(2013,5,1),
            Date(2013,5,17),
            Date(2013,6,6),
            Date(2013,8,15),
            Date(2013,9,18),
            Date(2013,9,19),
            Date(2013,9,20),
            Date(2013,10,3),
            Date(2013,10,9),
            Date(2013,12,25),
            Date(2014,1,1),
            Date(2014,1,30),
            Date(2014,1,31),
            Date(2014,5,1),
            Date(2014,5,5),
            Date(2014,5,6),
            Date(2014,6,4),
            Date(2014,6,6),
            Date(2014,8,15),
            Date(2014,9,8),
            Date(2014,9,9),
            Date(2014,9,10),
            Date(2014,10,3),
            Date(2014,10,9),
            Date(2014,12,25),
            Date(2015,1,1),
            Date(2015,2,18),
            Date(2015,2,19),
            Date(2015,2,20),
            Date(2015,5,1),
            Date(2015,5,5),
            Date(2015,5,25),
            Date(2015,8,14),
            Date(2015,9,28),
            Date(2015,9,29),
            Date(2015,10,9),
            Date(2015,12,25),
            Date(2016,1,1),
            Date(2016,2,8),
            Date(2016,2,9),
            Date(2016,2,10),
            Date(2016,3,1),
            Date(2016,4,13),
            Date(2016,5,5),
            Date(2016,5,6),
            Date(2016,6,6),
            Date(2016,8,15),
            Date(2016,9,14),
            Date(2016,9,15),
            Date(2016,9,16),
            Date(2016,10,3),
            Date(2017,1,27),
            Date(2017,1,30),
            Date(2017,3,1),
            Date(2017,5,1),
            Date(2017,5,3),
            Date(2017,5,5),
            Date(2017,5,9),
            Date(2017,6,6),
            Date(2017,8,15),
            Date(2017,10,2),
            Date(2017,10,3),
            Date(2017,10,4),
            Date(2017,10,5),
            Date(2017,10,6),
            Date(2017,10,9),
            Date(2017,12,25),
            Date(2018,1,1),
            Date(2018,2,15),
            Date(2018,2,16),
            Date(2018,3,1),
            Date(2018,5,1),
            Date(2018,5,7),
            Date(2018,5,22),
            Date(2018,6,6),
            Date(2018,6,13),
            Date(2018,8,15),
            Date(2018,9,24),
            Date(2018,9,25),
            Date(2018,9,26),
            Date(2018,10,3),
            Date(2018,10,9),
            Date(2018,12,25),
            Date(2019,1,1),
            Date(2019,2,4),
            Date(2019,2,5),
            Date(2019,2,6),
            Date(2019,3,1),
            Date(2019,5,1),
            Date(2019,5,6),
            Date(2019,6,6),
            Date(2019,8,15),
            Date(2019,9,12),
            Date(2019,9,13),
            Date(2019,10,3),
            Date(2019,10,9),
            Date(2019,12,25),
            Date(2020,1,1),
            Date(2020,1,24),
            Date(2020,1,27),
            Date(2020,4,15),
            Date(2020,4,30),
            Date(2020,5,1),
            Date(2020,5,5),
            Date(2020,8,17),
            Date(2020,9,30),
            Date(2020,10,1),
            Date(2020,10,2),
            Date(2020,10,9),
            Date(2020,12,25),
            Date(2021,1,1),
            Date(2021,2,11),
            Date(2021,2,12),
            Date(2021,3,1),
            Date(2021,5,5),
            Date(2021,5,19),
            Date(2021,8,16),
            Date(2021,9,20),
            Date(2021,9,21),
            Date(2021,9,22),
            Date(2021,10,4),
            Date(2021,10,11),
            Date(2022,1,31),
            Date(2022,2,1),
            Date(2022,2,2),
            Date(2022,3,1),
            Date(2022,3,9),
            Date(2022,5,5),
            Date(2022,6,1),
            Date(2022,6,6),
            Date(2022,8,15),
            Date(2022,9,9),
            Date(2022,9,12),
            Date(2022,10,3),
            Date(2022,10,10),
            Date(2023,1,23),
            Date(2023,1,24),
            Date(2023,3,1),
            Date(2023,5,1),
            Date(2023,5,5),
            Date(2023,5,29),
            Date(2023,6,6),
            Date(2023,8,15),
            Date(2023,9,28),
            Date(2023,9,29),
            Date(2023,10,2),
            Date(2023,10,3),
            Date(2023,10,9),
            Date(2023,12,25),
            Date(2024,1,1),
            Date(2024,2,9),
            Date(2024,2,12),
            Date(2024,3,1),
            Date(2024,4,10),
            Date(2024,5,1),
            Date(2024,5,6),
            Date(2024,5,15),
            Date(2024,6,6),
            Date(2024,8,15),
            Date(2024,9,16),
            Date(2024,9,17),
            Date(2024,9,18),
            Date(2024,10,1),
            Date(2024,10,3),
            Date(2024,10,9),
            Date(2024,12,25),
            Date(2025,1,1),
            Date(2025,1,27),
            Date(2025,1,28),
            Date(2025,1,29),
            Date(2025,1,30),
            Date(2025,3,3),
            Date(2025,5,1),
            Date(2025,5,5),
            Date(2025,5,6),
            Date(2025,6,6),
            Date(2025,8,15),
            Date(2025,10,3),
            Date(2025,10,6),
            Date(2025,10,7),
            Date(2025,10,8),
            Date(2025,10,9),
            Date(2025,12,25),
            Date(2026,1,1),
            Date(2026,2,16),
            Date(2026,2,17),
            Date(2026,2,18),
            Date(2026,3,2),
            Date(2026,5,1),
            Date(2026,5,5),
            Date(2026,5,25),
            Date(2026,6,3),
            Date(2026,8,17),
            Date(2026,9,24),
            Date(2026,9,25),
            Date(2026,10,5),
            Date(2026,10,9),
            Date(2026,12,25),
            Date(2027,1,1),
            Date(2027,2,8),
            Date(2027,2,9),
            Date(2027,3,1),
            Date(2027,3,3),
            Date(2027,5,5),
            Date(2027,5,13),
            Date(2027,8,16),
            Date(2027,9,14),
            Date(2027,9,15),
            Date(2027,9,16),
            Date(2027,10,4),
            Date(2027,10,11),
            Date(2027,12,27),
            Date(2028,1,26),
            Date(2028,1,27),
            Date(2028,1,28),
            Date(2028,3,1),
            Date(2028,4,12),
            Date(2028,5,1),
            Date(2028,5,2),
            Date(2028,5,5),
            Date(2028,6,6),
            Date(2028,8,15),
            Date(2028,10,2),
            Date(2028,10,3),
            Date(2028,10,4),
            Date(2028,10,5),
            Date(2028,10,9),
            Date(2028,12,25),
            Date(2029,1,1),
            Date(2029,2,12),
            Date(2029,2,13),
            Date(2029,2,14),
            Date(2029,3,1),
            Date(2029,5,1),
            Date(2029,5,7),
            Date(2029,5,21),
            Date(2029,6,6),
            Date(2029,8,15),
            Date(2029,9,21),
            Date(2029,9,24),
            Date(2029,10,3),
            Date(2029,10,9),
            Date(2029,12,25),
            Date(2030,1,1),
            Date(2030,2,4),
            Date(2030,2,5),
            Date(2030,3,1),
            Date(2030,5,1),
            Date(2030,5,6),
            Date(2030,5,9),
            Date(2030,6,6),
            Date(2030,6,12),
            Date(2030,8,15),
            Date(2030,9,11),
            Date(2030,9,12),
            Date(2030,9,13),
            Date(2030,10,3),
            Date(2030,10,9),
            Date(2030,12,25),
            Date(2031,1,1),
            Date(2031,1,22),
            Date(2031,1,23),
            Date(2031,1,24),
            Date(2031,3,3),
            Date(2031,5,1),
            Date(2031,5,5),
            Date(2031,5,28),
            Date(2031,6,6),
            Date(2031,8,15),
            Date(2031,9,30),
            Date(2031,10,1),
            Date(2031,10,2),
            Date(2031,10,3),
            Date(2031,10,9),
            Date(2031,12,25),
            Date(2032,1,1),
            Date(2032,2,10),
            Date(2032,2,11),
            Date(2032,2,12),
            Date(2032,3,1),
            Date(2032,3,3),
            Date(2032,4,14),
            Date(2032,5,5),
            Date(2032,5,17),
            Date(2032,8,16),
            Date(2032,9,20),
            Date(2032,9,21),
            Date(2032,10,4),
            Date(2032,10,11),
            Date(2032,12,27),
            Date(2033,1,31),
            Date(2033,2,1),
            Date(2033,2,2),
            Date(2033,3,1),
            Date(2033,5,5),
            Date(2033,5,6),
            Date(2033,6,6),
            Date(2033,8,15),
            Date(2033,9,7),
            Date(2033,9,8),
            Date(2033,9,9),
            Date(2033,10,3),
            Date(2033,10,10),
            Date(2033,12,26),
            Date(2034,2,20),
            Date(2034,2,21),
            Date(2034,3,1),
            Date(2034,5,1),
            Date(2034,5,5),
            Date(2034,5,25),
            Date(2034,5,31),
            Date(2034,6,6),
            Date(2034,8,15),
            Date(2034,9,26),
            Date(2034,9,27),
            Date(2034,9,28),
            Date(2034,10,3),
            Date(2034,10,9),
            Date(2034,12,25),
            Date(2035,1,1),
            Date(2035,2,7),
            Date(2035,2,8),
            Date(2035,2,9),
            Date(2035,3,1),
            Date(2035,5,1),
            Date(2035,5,7),
            Date(2035,5,15),
            Date(2035,6,6),
            Date(2035,8,15),
            Date(2035,9,17),
            Date(2035,9,18),
            Date(2035,10,3),
            Date(2035,10,9),
            Date(2035,12,25),
            Date(2036,1,1),
            Date(2036,1,28),
            Date(2036,1,29),
            Date(2036,1,30),
            Date(2036,3,3),
            Date(2036,4,9),
            Date(2036,5,1),
            Date(2036,5,5),
            Date(2036,5,6),
            Date(2036,6,6),
            Date(2036,8,15),
            Date(2036,10,3),
            Date(2036,10,6),
            Date(2036,10,7),
            Date(2036,10,9),
            Date(2036,12,25),
            Date(2037,1,1),
            Date(2037,2,16),
            Date(2037,2,17),
            Date(2037,3,2),
            Date(2037,3,4),
            Date(2037,5,1),
            Date(2037,5,5),
            Date(2037,5,22),
            Date(2037,8,17),
            Date(2037,9,23),
            Date(2037,9,24),
            Date(2037,9,25),
            Date(2037,10,5),
            Date(2037,10,9),
            Date(2037,12,25),
            Date(2038,1,1),
            Date(2038,2,3),
            Date(2038,2,4),
            Date(2038,2,5),
            Date(2038,3,1),
            Date(2038,5,5),
            Date(2038,5,11),
            Date(2038,6,2),
            Date(2038,8,16),
            Date(2038,9,13),
            Date(2038,9,14),
            Date(2038,9,15),
            Date(2038,10,4),
            Date(2038,10,11),
            Date(2039,1,24),
            Date(2039,1,25),
            Date(2039,1,26),
            Date(2039,3,1),
            Date(2039,5,5),
            Date(2039,6,6),
            Date(2039,8,15),
            Date(2039,10,3),
            Date(2039,10,4),
            Date(2039,10,5),
            Date(2039,10,10),
            Date(2040,2,13),
            Date(2040,2,14),
            Date(2040,3,1),
            Date(2040,4,11),
            Date(2040,5,1),
            Date(2040,5,7),
            Date(2040,5,18),
            Date(2040,6,6),
            Date(2040,8,15),
            Date(2040,9,20),
            Date(2040,9,21),
            Date(2040,10,3),
            Date(2040,10,9),
            Date(2040,12,25),
            Date(2041,1,1),
            Date(2041,1,31),
            Date(2041,2,1),
            Date(2041,3,1),
            Date(2041,5,1),
            Date(2041,5,6),
            Date(2041,5,7),
            Date(2041,6,6),
            Date(2041,8,15),
            Date(2041,9,9),
            Date(2041,9,10),
            Date(2041,9,11),
            Date(2041,10,3),
            Date(2041,10,9),
            Date(2041,12,25),
            Date(2042,1,1),
            Date(2042,1,21),
            Date(2042,1,22),
            Date(2042,1,23),
            Date(2042,3,3),
            Date(2042,3,5),
            Date(2042,5,1),
            Date(2042,5,5),
            Date(2042,5,26),
            Date(2042,6,4),
            Date(2042,6,6),
            Date(2042,8,15),
            Date(2042,9,29),
            Date(2042,9,30),
            Date(2042,10,3),
            Date(2042,10,9),
            Date(2042,12,25),
            Date(2043,1,1),
            Date(2043,2,9),
            Date(2043,2,10),
            Date(2043,2,11),
            Date(2043,3,2),
            Date(2043,5,1),
            Date(2043,5,5),
            Date(2043,8,17),
            Date(2043,9,16),
            Date(2043,9,17),
            Date(2043,9,18),
            Date(2043,10,5),
            Date(2043,10,9),
            Date(2043,12,25),
            Date(2044,1,1),
            Date(2044,1,29),
            Date(2044,2,1),
            Date(2044,3,1),
            Date(2044,4,13),
            Date(2044,5,5),
            Date(2044,5,6),
            Date(2044,6,6),
            Date(2044,8,15),
            Date(2044,10,3),
            Date(2044,10,4),
            Date(2044,10,5),
            Date(2044,10,6),
            Date(2044,10,10),
            Date(2045,2,16),
            Date(2045,2,17),
            Date(2045,3,1),
            Date(2045,5,1),
            Date(2045,5,5),
            Date(2045,5,24),
            Date(2045,6,6),
            Date(2045,8,15),
            Date(2045,9,25),
            Date(2045,9,26),
            Date(2045,9,27),
            Date(2045,10,3),
            Date(2045,10,9),
            Date(2045,12,25),
            Date(2046,1,1),
            Date(2046,2,5),
            Date(2046,2,6),
            Date(2046,2,7),
            Date(2046,3,1),
            Date(2046,5,1),
            Date(2046,5,7),
            Date(2046,6,6),
            Date(2046,6,13),
            Date(2046,8,15),
            Date(2046,9,14),
            Date(2046,9,17),
            Date(2046,10,3),
            Date(2046,10,9),
            Date(2046,12,25),
            Date(2047,1,1),
            Date(2047,1,25),
            Date(2047,1,28),
            Date(2047,3,1),
            Date(2047,3,6),
            Date(2047,5,1),
            Date(2047,5,2),
            Date(2047,5,6),
            Date(2047,6,6),
            Date(2047,8,15),
            Date(2047,10,3),
            Date(2047,10,4),
            Date(2047,10,7),
            Date(2047,10,9),
            Date(2047,12,25),
            Date(2048,1,1),
            Date(2048,2,13),
            Date(2048,2,14),
            Date(2048,3,2),
            Date(2048,4,15),
            Date(2048,5,1),
            Date(2048,5,5),
            Date(2048,5,20),
            Date(2048,8,17),
            Date(2048,9,21),
            Date(2048,9,22),
            Date(2048,9,23),
            Date(2048,10,5),
            Date(2048,10,9),
            Date(2048,12,25),
            Date(2049,1,1),
            Date(2049,2,1),
            Date(2049,2,2),
            Date(2049,2,3),
            Date(2049,3,1),
            Date(2049,5,5),
            Date(2049,8,16),
            Date(2049,9,10),
            Date(2049,9,13),
            Date(2049,10,4),
            Date(2049,10,11),
            Date(2050,1,24),
            Date(2050,1,25),
            Date(2050,3,1),
            Date(2050,5,5),
            Date(2050,6,1),
            Date(2050,6,6),
            Date(2050,8,15),
            Date(2050,9,29),
            Date(2050,9,30),
            Date(2050,10,3),
            Date(2050,10,10),
            Date(2051,2,10),
            Date(2051,2,13),
            Date(2051,3,1),
            Date(2051,5,1),
            Date(2051,5,5),
            Date(2051,5,17),
            Date(2051,6,6),
            Date(2051,8,15),
            Date(2051,9,18),
            Date(2051,9,19),
            Date(2051,9,20),
            Date(2051,10,3),
            Date(2051,10,9),
            Date(2051,12,25),
            Date(2052,1,1),
            Date(2052,1,31),
            Date(2052,2,1),
            Date(2052,2,2),
            Date(2052,3,1),
            Date(2052,3,6),
            Date(2052,4,10),
            Date(2052,5,1),
            Date(2052,5,6),
            Date(2052,5,7),
            Date(2052,6,6),
            Date(2052,8,15),
            Date(2052,9,6),
            Date(2052,9,9),
            Date(2052,10,3),
            Date(2052,10,9),
            Date(2052,12,25),
            Date(2053,1,1),
            Date(2053,2,18),
            Date(2053,2,19),
            Date(2053,2,20),
            Date(2053,3,3),
            Date(2053,5,1),
            Date(2053,5,5),
            Date(2053,6,6),
            Date(2053,8,15),
            Date(2053,9,25),
            Date(2053,9,26),
            Date(2053,10,3),
            Date(2053,10,9),
            Date(2053,12,25),
            Date(2054,1,1),
            Date(2054,2,9),
            Date(2054,2,10),
            Date(2054,3,2),
            Date(2054,5,1),
            Date(2054,5,5),
            Date(2054,5,15),
            Date(2054,6,3),
            Date(2054,8,17),
            Date(2054,9,15),
            Date(2054,9,16),
            Date(2054,9,17),
            Date(2054,10,5),
            Date(2054,10,9),
            Date(2054,12,25),
            Date(2055,1,1),
            Date(2055,1,27),
            Date(2055,1,28),
            Date(2055,1,29),
            Date(2055,3,1),
            Date(2055,5,4),
            Date(2055,5,5),
            Date(2055,8,16),
            Date(2055,10,4),
            Date(2055,10,5),
            Date(2055,10,6),
            Date(2055,10,7),
            Date(2055,10,11),
            Date(2056,2,14),
            Date(2056,2,15),
            Date(2056,2,16),
            Date(2056,3,1),
            Date(2056,4,12),
            Date(2056,5,1),
            Date(2056,5,5),
            Date(2056,5,22),
            Date(2056,6,6),
            Date(2056,8,15),
            Date(2056,9,25),
            Date(2056,9,26),
            Date(2056,10,3),
            Date(2056,10,9),
            Date(2056,12,25),
            Date(2057,1,1),
            Date(2057,2,5),
            Date(2057,2,6),
            Date(2057,3,1),
            Date(2057,3,7),
            Date(2057,5,1),
            Date(2057,5,7),
            Date(2057,5,11),
            Date(2057,6,6),
            Date(2057,8,15),
            Date(2057,9,12),
            Date(2057,9,13),
            Date(2057,9,14),
            Date(2057,10,3),
            Date(2057,10,9),
            Date(2057,12,25),
            Date(2058,1,1),
            Date(2058,1,23),
            Date(2058,1,24),
            Date(2058,1,25),
            Date(2058,3,1),
            Date(2058,4,30),
            Date(2058,5,1),
            Date(2058,5,6),
            Date(2058,6,6),
            Date(2058,6,12),
            Date(2058,8,15),
            Date(2058,10,1),
            Date(2058,10,2),
            Date(2058,10,3),
            Date(2058,10,4),
            Date(2058,10,9),
            Date(2058,12,25),
            Date(2059,1,1),
            Date(2059,2,11),
            Date(2059,2,12),
            Date(2059,2,13),
            Date(2059,3,3),
            Date(2059,5,1),
            Date(2059,5,5),
            Date(2059,5,19),
            Date(2059,6,6),
            Date(2059,8,15),
            Date(2059,9,22),
            Date(2059,9,23),
            Date(2059,10,3),
            Date(2059,10,9),
            Date(2059,12,25),
            Date(2060,1,1),
            Date(2060,2,2),
            Date(2060,2,3),
            Date(2060,2,4),
            Date(2060,3,1),
            Date(2060,4,14),
            Date(2060,5,5),
            Date(2060,5,7),
            Date(2060,8,16),
            Date(2060,9,8),
            Date(2060,9,9),
            Date(2060,9,10),
            Date(2060,10,4),
            Date(2060,10,11),
            Date(2061,1,21),
            Date(2061,1,24),
            Date(2061,3,1),
            Date(2061,5,5),
            Date(2061,5,26),
            Date(2061,6,6),
            Date(2061,8,15),
            Date(2061,9,27),
            Date(2061,9,28),
            Date(2061,9,29),
            Date(2061,10,3),
            Date(2061,10,10),
            Date(2062,2,8),
            Date(2062,2,9),
            Date(2062,2,10),
            Date(2062,3,1),
            Date(2062,3,8),
            Date(2062,5,1),
            Date(2062,5,5),
            Date(2062,5,16),
            Date(2062,5,31),
            Date(2062,6,6),
            Date(2062,8,15),
            Date(2062,9,18),
            Date(2062,9,19),
            Date(2062,10,3),
            Date(2062,10,9),
            Date(2062,12,25),
            Date(2063,1,1),
            Date(2063,1,29),
            Date(2063,1,30),
            Date(2063,1,31),
            Date(2063,3,1),
            Date(2063,5,1),
            Date(2063,5,7),
            Date(2063,6,6),
            Date(2063,8,15),
            Date(2063,10,3),
            Date(2063,10,5),
            Date(2063,10,8),
            Date(2063,10,9),
            Date(2063,12,25),
            Date(2064,1,1),
            Date(2064,2,18),
            Date(2064,2,19),
            Date(2064,3,3),
            Date(2064,4,9),
            Date(2064,5,1),
            Date(2064,5,5),
            Date(2064,5,23),
            Date(2064,6,6),
            Date(2064,8,15),
            Date(2064,9,24),
            Date(2064,9,25),
            Date(2064,9,26),
            Date(2064,10,3),
            Date(2064,10,9),
            Date(2064,12,25),
            Date(2065,1,1),
            Date(2065,2,4),
            Date(2065,2,5),
            Date(2065,2,6),
            Date(2065,3,2),
            Date(2065,5,1),
            Date(2065,5,5),
            Date(2065,5,12),
            Date(2065,8,17),
            Date(2065,9,14),
            Date(2065,9,15),
            Date(2065,9,16),
            Date(2065,10,5),
            Date(2065,10,9),
            Date(2065,12,25),
            Date(2066,1,1),
            Date(2066,1,25),
            Date(2066,1,26),
            Date(2066,1,27),
            Date(2066,3,1),
            Date(2066,5,5),
            Date(2066,6,2),
            Date(2066,8,16),
            Date(2066,10,4),
            Date(2066,10,5),
            Date(2066,10,6),
            Date(2066,10,11),
            Date(2067,2,14),
            Date(2067,2,15),
            Date(2067,2,16),
            Date(2067,3,1),
            Date(2067,3,9),
            Date(2067,5,5),
            Date(2067,5,20),
            Date(2067,6,6),
            Date(2067,8,15),
            Date(2067,9,22),
            Date(2067,9,23),
            Date(2067,10,3),
            Date(2067,10,10),
            Date(2068,2,2),
            Date(2068,2,3),
            Date(2068,3,1),
            Date(2068,4,11),
            Date(2068,5,1),
            Date(2068,5,7),
            Date(2068,5,9),
            Date(2068,6,6),
            Date(2068,8,15),
            Date(2068,9,10),
            Date(2068,9,11),
            Date(2068,9,12),
            Date(2068,10,3),
            Date(2068,10,9),
            Date(2068,12,25),
            Date(2069,1,1),
            Date(2069,1,22),
            Date(2069,1,23),
            Date(2069,1,24),
            Date(2069,3,1),
            Date(2069,5,1),
            Date(2069,5,6),
            Date(2069,6,6),
            Date(2069,8,15),
            Date(2069,9,30),
            Date(2069,10,1),
            Date(2069,10,3),
            Date(2069,10,9),
            Date(2069,12,25),
            Date(2070,1,1),
            Date(2070,2,10),
            Date(2070,2,11),
            Date(2070,2,12),
            Date(2070,3,3),
            Date(2070,5,1),
            Date(2070,5,5),
            Date(2070,6,4),
            Date(2070,6,6),
            Date(2070,8,15),
            Date(2070,9,18),
            Date(2070,9,19),
            Date(2070,10,3),
            Date(2070,10,9),
            Date(2070,12,25),
            Date(2071,1,1),
            Date(2071,1,30),
            Date(2071,2,2),
            Date(2071,3,2),
            Date(2071,5,1),
            Date(2071,5,5),
            Date(2071,5,7),
            Date(2071,8,17),
            Date(2071,9,7),
            Date(2071,9,8),
            Date(2071,9,9),
            Date(2071,10,5),
            Date(2071,10,9),
            Date(2071,12,25),
            Date(2072,1,1),
            Date(2072,2,18),
            Date(2072,2,19),
            Date(2072,3,1),
            Date(2072,3,9),
            Date(2072,4,13),
            Date(2072,5,5),
            Date(2072,5,25),
            Date(2072,6,6),
            Date(2072,8,15),
            Date(2072,9,26),
            Date(2072,9,27),
            Date(2072,9,28),
            Date(2072,10,3),
            Date(2072,10,10),
            Date(2073,2,6),
            Date(2073,2,7),
            Date(2073,2,8),
            Date(2073,3,1),
            Date(2073,5,1),
            Date(2073,5,5),
            Date(2073,6,6),
            Date(2073,8,15),
            Date(2073,9,15),
            Date(2073,9,18),
            Date(2073,10,3),
            Date(2073,10,9),
            Date(2073,12,25),
            Date(2074,1,1),
            Date(2074,1,26),
            Date(2074,1,29)
        ]
        if dt in korea_holidays:
            return True
        return False

    ###############################################################################

    def holiday_target(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """

        m = dt.m
        d = dt.d
        y = dt.y
        day_in_year = self.day_in_year

        if m == 1 and d == 1:  # new year's day
            return True

        if m == 5 and d == 1:  # May day
            return True

        em = easterMondayDay[y - 1901]

        if day_in_year == em - 3:  # Easter Friday holiday
            return True

        if day_in_year == em:  # Easter monday holiday
            return True

        if m == 12 and d == 25:  # Xmas bank holiday
            return True

        if m == 12 and d == 26:  # Xmas bank holiday
            return True

        return False

    ###############################################################################

    def holiday_none(self, dt=None):
        """ No day is a holiday. """
        return False

    ###############################################################################

    def get_holiday_list(self, year: float):
        """ generates a list of holidays in a specific year for the specified
        calendar. Useful for diagnostics. """
        start_dt = Date(1, 1, year)
        end_dt = Date(1, 1, year + 1)
        holiday_list = []
        while start_dt < end_dt:
            if self.is_business_day(start_dt) is False and start_dt.is_weekend() is False:
                holiday_list.append(start_dt.__str__())

            start_dt = start_dt.add_days(1)

        return holiday_list

    ###############################################################################

    def easter_monday(self, year: float):
        """ Get the day in a given year that is Easter Monday. This is not
        easy to compute, so we rely on a pre-calculated array. """

        if year > 2100:
            raise FinError("Unable to determine Easter monday in year " + str(year))

        em_days = easterMondayDay[year - 1901]
        start_dt = Date(1, 1, year)
        em = start_dt.add_days(em_days-1)
        return em

    ###############################################################################

    def __str__(self):
        s = self.cal_type.name
        return s

    ###############################################################################

    def __repr__(self):
        s = self.cal_type
        return s

    ###############################################################################