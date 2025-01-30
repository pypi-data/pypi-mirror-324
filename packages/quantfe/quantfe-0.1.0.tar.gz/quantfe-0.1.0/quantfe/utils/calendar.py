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
    KOREA = 16


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

    def __init__(self, cal_type: Union[CalendarTypes, list]):
        """ Create a calendar based on a specified calendar type. """
        if isinstance(cal_type, list):
            for _cal_type in cal_type:
                if _cal_type not in CalendarTypes:
                    raise FinError("Need to pass FinCalendarType and not " + str(_cal_type))            
        else:
            if cal_type not in CalendarTypes:
                raise FinError("Need to pass FinCalendarType and not " + str(cal_type))

        self.cal_type = cal_type
        self.day_in_year = None
        self.holiday_list = []
        self.weekday = None
        
        with open("quantfe/utils/holidays.json", "r") as f:
            holidays = json.load(f)

        if self.cal_type == CalendarTypes.NONE:
            pass
        elif self.cal_type == CalendarTypes.WEEKEND:
            return self.holiday_weekend(dt)
        elif self.cal_type == CalendarTypes.AUSTRALIA:
            return self.holiday_australia(dt)
        elif self.cal_type == CalendarTypes.CANADA:
            return self.holiday_canada(dt)
        elif self.cal_type == CalendarTypes.FRANCE:
            return self.holiday_france(dt)
        elif self.cal_type == CalendarTypes.GERMANY:
            return self.holiday_germany(dt)
        elif self.cal_type == CalendarTypes.ITALY:
            return self.holiday_italy(dt)
        elif self.cal_type == CalendarTypes.JAPAN:
            return self.holiday_japan(dt)
        elif self.cal_type == CalendarTypes.NEW_ZEALAND:
            return self.holiday_new_zealand(dt)
        elif self.cal_type == CalendarTypes.NORWAY:
            return self.holiday_norway(dt)
        elif self.cal_type == CalendarTypes.SWEDEN:
            return self.holiday_sweden(dt)
        elif self.cal_type == CalendarTypes.SWITZERLAND:
            return self.holiday_switzerland(dt)
        elif self.cal_type == CalendarTypes.TARGET:
            return self.holiday_target(dt)
        elif self.cal_type == CalendarTypes.UNITED_KINGDOM:
            return self.holiday_united_kingdom(dt)
        elif self.cal_type == CalendarTypes.UNITED_STATES:
            return self.holiday_united_states(dt)
        elif self.cal_type == CalendarTypes.KOREA:
            for holiday in holidays["seoul"]:
                holidate = Date.from_string(holiday, "%Y-%m-%d")
                if holidate not in self.holiday_list:
                    self.holiday_list.append(holidate)

        else:
            raise FinError(f"Unknown calendar: {self.cal_type}")


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

    def is_business_day(self, dt: Date):
        """ Determines if a date is a business day according to the specified
        calendar. If it is it returns True, otherwise False. """

        # For all calendars so far, SAT and SUN are not business days
        # If this ever changes I will need to add a filter here.
        if dt.is_weekend():
            return False

        if self.is_holiday(dt) is True:
            return False
        else:
            return True

    ###############################################################################

    def is_holiday(self, date: Date):
        """ Determines if a date is a Holiday according to the specified
        calendar. Weekends are not holidays unless the holiday falls on a
        weekend date. """

        if date in self.holiday_list:
            return True
        else:
            return False

        # start_dt = Date(dt.y, 1, 1)
        # self.day_in_year = dt.excel_dt - start_dt.excel_dt + 1
        # self.weekday = dt.weekday

        # if self.cal_type == CalendarTypes.NONE:
        #     return self.holiday_none(dt)
        # elif self.cal_type == CalendarTypes.WEEKEND:
        #     return self.holiday_weekend(dt)
        # elif self.cal_type == CalendarTypes.AUSTRALIA:
        #     return self.holiday_australia(dt)
        # elif self.cal_type == CalendarTypes.CANADA:
        #     return self.holiday_canada(dt)
        # elif self.cal_type == CalendarTypes.FRANCE:
        #     return self.holiday_france(dt)
        # elif self.cal_type == CalendarTypes.GERMANY:
        #     return self.holiday_germany(dt)
        # elif self.cal_type == CalendarTypes.ITALY:
        #     return self.holiday_italy(dt)
        # elif self.cal_type == CalendarTypes.JAPAN:
        #     return self.holiday_japan(dt)
        # elif self.cal_type == CalendarTypes.NEW_ZEALAND:
        #     return self.holiday_new_zealand(dt)
        # elif self.cal_type == CalendarTypes.NORWAY:
        #     return self.holiday_norway(dt)
        # elif self.cal_type == CalendarTypes.SWEDEN:
        #     return self.holiday_sweden(dt)
        # elif self.cal_type == CalendarTypes.SWITZERLAND:
        #     return self.holiday_switzerland(dt)
        # elif self.cal_type == CalendarTypes.TARGET:
        #     return self.holiday_target(dt)
        # elif self.cal_type == CalendarTypes.UNITED_KINGDOM:
        #     return self.holiday_united_kingdom(dt)
        # elif self.cal_type == CalendarTypes.UNITED_STATES:
        #     return self.holiday_united_states(dt)
        # elif self.cal_type == CalendarTypes.KOREA:
        #     return self.holiday_korea(dt)
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

        if m == 1 and d > 7 and d < 15 and weekday == Date.MON:  # coa
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

    def holiday_korea(self, dt):
        """ Only bank holidays. Weekends by themselves are not a holiday. """
        korea_holidays = [
            Date(2020, 1, 1),
            Date(2020, 1, 24),
            Date(2020, 1, 27),
            Date(2020, 4, 15),
            Date(2020, 4, 30),
            Date(2020, 5, 1),
            Date(2020, 5, 5),
            Date(2020, 8, 17),
            Date(2020, 9, 30),
            Date(2020, 10, 1),
            Date(2020, 10, 2),
            Date(2020, 10, 9),
            Date(2020, 12, 25),
            Date(2021, 1, 1),
            Date(2021, 2, 11),
            Date(2021, 2, 12),
            Date(2021, 3, 1),
            Date(2021, 5, 5),
            Date(2021, 5, 19),
            Date(2021, 8, 16),
            Date(2021, 9, 20),
            Date(2021, 9, 21),
            Date(2021, 9, 22),
            Date(2021, 10, 4),
            Date(2021, 10, 11),
            Date(2022, 1, 31),
            Date(2022, 2, 1),
            Date(2022, 2, 2),
            Date(2022, 3, 1),
            Date(2022, 3, 9),
            Date(2022, 5, 5),
            Date(2022, 6, 1),
            Date(2022, 6, 6),
            Date(2022, 8, 15),
            Date(2022, 9, 9),
            Date(2022, 9, 12),
            Date(2022, 10, 3),
            Date(2022, 10, 10),
            Date(2023, 1, 23),
            Date(2023, 1, 24),
            Date(2023, 3, 1),
            Date(2023, 5, 1),
            Date(2023, 5, 5),
            Date(2023, 5, 29),
            Date(2023, 6, 6),
            Date(2023, 8, 15),
            Date(2023, 9, 28),
            Date(2023, 9, 29),
            Date(2023, 10, 2),
            Date(2023, 10, 3),
            Date(2023, 10, 9),
            Date(2023, 12, 25),
            Date(2024, 1, 1),
            Date(2024, 2, 9),
            Date(2024, 2, 12),
            Date(2024, 3, 1),
            Date(2024, 4, 10),
            Date(2024, 5, 1),
            Date(2024, 5, 6),
            Date(2024, 5, 15),
            Date(2024, 6, 6),
            Date(2024, 8, 15),
            Date(2024, 9, 16),
            Date(2024, 9, 17),
            Date(2024, 9, 18),
            Date(2024, 10, 1),
            Date(2024, 10, 3),
            Date(2024, 10, 9),
            Date(2024, 12, 25),
            Date(2025, 1, 1),
            Date(2025, 1, 28),
            Date(2025, 1, 29),
            Date(2025, 1, 30),
            Date(2025, 3, 3),
            Date(2025, 5, 1),
            Date(2025, 5, 5),
            Date(2025, 5, 6),
            Date(2025, 6, 6),
            Date(2025, 8, 15),
            Date(2025, 10, 3),
            Date(2025, 10, 6),
            Date(2025, 10, 7),
            Date(2025, 10, 8),
            Date(2025, 10, 9),
            Date(2025, 12, 25),
            Date(2026, 1, 1),
            Date(2026, 2, 16),
            Date(2026, 2, 17),
            Date(2026, 2, 18),
            Date(2026, 3, 2),
            Date(2026, 5, 1),
            Date(2026, 5, 5),
            Date(2026, 5, 25),
            Date(2026, 6, 3),
            Date(2026, 8, 17),
            Date(2026, 9, 24),
            Date(2026, 9, 25),
            Date(2026, 10, 5),
            Date(2026, 10, 9),
            Date(2026, 12, 25),
            Date(2027, 1, 1),
            Date(2027, 2, 8),
            Date(2027, 2, 9),
            Date(2027, 3, 1),
            Date(2027, 3, 3),
            Date(2027, 5, 5),
            Date(2027, 5, 13),
            Date(2027, 8, 16),
            Date(2027, 9, 14),
            Date(2027, 9, 15),
            Date(2027, 9, 16),
            Date(2027, 10, 4),
            Date(2027, 10, 11),
            Date(2027, 12, 27),
            Date(2028, 1, 26),
            Date(2028, 1, 27),
            Date(2028, 1, 28),
            Date(2028, 3, 1),
            Date(2028, 4, 12),
            Date(2028, 5, 1),
            Date(2028, 5, 2),
            Date(2028, 5, 5),
            Date(2028, 6, 6),
            Date(2028, 8, 15),
            Date(2028, 10, 2),
            Date(2028, 10, 3),
            Date(2028, 10, 4),
            Date(2028, 10, 5),
            Date(2028, 10, 9),
            Date(2028, 12, 25),
            Date(2029, 1, 1),
            Date(2029, 2, 12),
            Date(2029, 2, 13),
            Date(2029, 2, 14),
            Date(2029, 3, 1),
            Date(2029, 5, 1),
            Date(2029, 5, 7),
            Date(2029, 5, 21),
            Date(2029, 6, 6),
            Date(2029, 8, 15),
            Date(2029, 9, 21),
            Date(2029, 9, 24),
            Date(2029, 10, 3),
            Date(2029, 10, 9),
            Date(2029, 12, 25),
            Date(2030, 1, 1),
            Date(2030, 2, 4),
            Date(2030, 2, 5),
            Date(2030, 3, 1),
            Date(2030, 5, 1),
            Date(2030, 5, 6),
            Date(2030, 5, 9),
            Date(2030, 6, 6),
            Date(2030, 6, 12),
            Date(2030, 8, 15),
            Date(2030, 9, 11),
            Date(2030, 9, 12),
            Date(2030, 9, 13),
            Date(2030, 10, 3),
            Date(2030, 10, 9),
            Date(2030, 12, 25),
            Date(2031, 1, 1),
            Date(2031, 1, 22),
            Date(2031, 1, 23),
            Date(2031, 1, 24),
            Date(2031, 3, 3),
            Date(2031, 5, 1),
            Date(2031, 5, 5),
            Date(2031, 5, 28),
            Date(2031, 6, 6),
            Date(2031, 8, 15),
            Date(2031, 9, 30),
            Date(2031, 10, 1),
            Date(2031, 10, 2),
            Date(2031, 10, 3),
            Date(2031, 10, 9),
            Date(2031, 12, 25),
            Date(2032, 1, 1),
            Date(2032, 2, 10),
            Date(2032, 2, 11),
            Date(2032, 2, 12),
            Date(2032, 3, 1),
            Date(2032, 3, 3),
            Date(2032, 4, 14),
            Date(2032, 5, 5),
            Date(2032, 5, 17),
            Date(2032, 8, 16),
            Date(2032, 9, 20),
            Date(2032, 9, 21),
            Date(2032, 10, 4),
            Date(2032, 10, 11),
            Date(2032, 12, 27),
            Date(2033, 1, 31),
            Date(2033, 2, 1),
            Date(2033, 2, 2),
            Date(2033, 3, 1),
            Date(2033, 5, 5),
            Date(2033, 5, 6),
            Date(2033, 6, 6),
            Date(2033, 8, 15),
            Date(2033, 9, 7),
            Date(2033, 9, 8),
            Date(2033, 9, 9),
            Date(2033, 10, 3),
            Date(2033, 10, 10),
            Date(2033, 12, 26),
            Date(2034, 2, 20),
            Date(2034, 2, 21),
            Date(2034, 3, 1),
            Date(2034, 5, 1),
            Date(2034, 5, 5),
            Date(2034, 5, 25),
            Date(2034, 5, 31),
            Date(2034, 6, 6),
            Date(2034, 8, 15),
            Date(2034, 9, 26),
            Date(2034, 9, 27),
            Date(2034, 9, 28),
            Date(2034, 10, 3),
            Date(2034, 10, 9),
            Date(2034, 12, 25),
            Date(2035, 1, 1),
            Date(2035, 2, 7),
            Date(2035, 2, 8),
            Date(2035, 2, 9),
            Date(2035, 3, 1),
            Date(2035, 5, 1),
            Date(2035, 5, 7),
            Date(2035, 5, 15),
            Date(2035, 6, 6),
            Date(2035, 8, 15),
            Date(2035, 9, 17),
            Date(2035, 9, 18),
            Date(2035, 10, 3),
            Date(2035, 10, 9),
            Date(2035, 12, 25),
            Date(2036, 1, 1),
            Date(2036, 1, 28),
            Date(2036, 1, 29),
            Date(2036, 1, 30),
            Date(2036, 3, 3),
            Date(2036, 4, 9),
            Date(2036, 5, 1),
            Date(2036, 5, 5),
            Date(2036, 5, 6),
            Date(2036, 6, 6),
            Date(2036, 8, 15),
            Date(2036, 10, 3),
            Date(2036, 10, 6),
            Date(2036, 10, 7),
            Date(2036, 10, 9),
            Date(2036, 12, 25),
            Date(2037, 1, 1),
            Date(2037, 2, 16),
            Date(2037, 2, 17),
            Date(2037, 3, 2),
            Date(2037, 3, 4),
            Date(2037, 5, 1),
            Date(2037, 5, 5),
            Date(2037, 5, 22),
            Date(2037, 8, 17),
            Date(2037, 9, 23),
            Date(2037, 9, 24),
            Date(2037, 9, 25),
            Date(2037, 10, 5),
            Date(2037, 10, 9),
            Date(2037, 12, 25),
            Date(2038, 1, 1),
            Date(2038, 2, 3),
            Date(2038, 2, 4),
            Date(2038, 2, 5),
            Date(2038, 3, 1),
            Date(2038, 5, 5),
            Date(2038, 5, 11),
            Date(2038, 6, 2),
            Date(2038, 8, 16),
            Date(2038, 9, 13),
            Date(2038, 9, 14),
            Date(2038, 9, 15),
            Date(2038, 10, 4),
            Date(2038, 10, 11),
            Date(2039, 1, 24),
            Date(2039, 1, 25),
            Date(2039, 1, 26),
            Date(2039, 3, 1),
            Date(2039, 5, 5),
            Date(2039, 6, 6),
            Date(2039, 8, 15),
            Date(2039, 10, 3),
            Date(2039, 10, 4),
            Date(2039, 10, 5),
            Date(2039, 10, 10),
            Date(2040, 2, 13),
            Date(2040, 2, 14),
            Date(2040, 3, 1),
            Date(2040, 4, 11),
            Date(2040, 5, 1),
            Date(2040, 5, 7),
            Date(2040, 5, 18),
            Date(2040, 6, 6),
            Date(2040, 8, 15),
            Date(2040, 9, 20),
            Date(2040, 9, 21),
            Date(2040, 10, 3),
            Date(2040, 10, 9),
            Date(2040, 12, 25),
            Date(2041, 1, 1),
            Date(2041, 1, 31),
            Date(2041, 2, 1)
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