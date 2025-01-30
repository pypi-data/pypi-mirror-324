# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2025. 1. 20
"""

from typing import Union

from quantfe.utils.error import FinError
from quantfe.utils.date import Date
from quantfe.utils.schedule import Schedule
from quantfe.market.curves.discount_curve import DiscountCurve
from quantfe.utils import day_count, frequency, calendar, global_types, helpers, qmath


class SwapOvernightLeg:
    """
    Class for managing the overnight leg of a swap.
    """

    def __init__(self,
                 effective_dt: Date,  # Date interest starts to accrue
                 end_dt: Union[Date, str],  # Date contract ends
                 leg_type: global_types.SwapTypes,
                 spread: float,
                 freq_type: frequency.FrequencyTypes,
                 dc_type: day_count.DayCountTypes,
                 notional: float = qmath.ONE_MILLION,
                 principal: float = 0.0,
                 payment_lag: int = 0,
                 cal_type: calendar.CalendarTypes = calendar.CalendarTypes.WEEKEND,
                 bd_type: calendar.BusDayAdjustTypes = calendar.BusDayAdjustTypes.FOLLOWING,
                 dg_type: calendar.DateGenRuleTypes = calendar.DateGenRuleTypes.BACKWARD,
                 ):
        
        helpers.check_argument_types(self.__init__, locals())

        if type(end_dt) == Date:
            self.termination_dt = end_dt
        else:
            self.termination_dt = Date(end_dt)

        cal = calendar.Calendar(cal_type)
        self.maturity_dt = cal.adjust(self.termination_dt, bd_type)

        if effective_dt > self.maturity_dt:
            raise FinError("Start date after maturity date")

        self.effective_dt = effective_dt

        self.end_dt = end_dt
        self.leg_type = leg_type
        self.freq_type = freq_type
        self.payment_lag = payment_lag
        self.principal = principal
        self.notional = notional
        self.notional_array = []
        self.spread = spread

        self.dc_type = dc_type
        self.cal_type = cal_type
        self.bd_type = bd_type
        self.dg_type = dg_type

        self.start_accrued_dts = []
        self.end_accrued_dts = []
        self.payment_dts = []
        self.payments = []
        self.year_fracs = []
        self.accrued_days = []

        self.generate_payment_dts()

    def generate_payment_dts(self):
        """ Generate the overnight leg payment dates and accrual factors. """

        schedule = Schedule(self.effective_dt, 
                            self.termination_dt, 
                            self.freq_type, 
                            self.cal_type, 
                            self.bd_type, 
                            self.dg_type)

        schedule_dts = schedule.adjusted_dts

        if len(schedule_dts) < 2:
            raise FinError("Schedule has none or only one date")

        self.start_accrued_dts = []
        self.end_accrued_dts = []
        self.payment_dts = []
        self.year_fracs = []
        self.accrued_days = []

        prev_dt = schedule_dts[0]

        day_counter = day_count.DayCount(self.dc_type)
        cal = calendar.Calendar(self.cal_type)

        for next_dt in schedule_dts[1:]:
            self.start_accrued_dts.append(prev_dt)
            self.end_accrued_dts.append(next_dt)

            if self.payment_lag == 0:
                payment_dt = next_dt
            else:
                payment_dt = cal.add_business_days(next_dt, self.payment_lag)

            self.payment_dts.append(payment_dt)
            (year_frac, num, _) = day_counter.year_frac(prev_dt, next_dt)
            self.year_fracs.append(year_frac)
            self.accrued_days.append(num)
            prev_dt = next_dt

    def value(self, value_dt: Date, discount_curve: DiscountCurve, index_curve: DiscountCurve, ois_rate_history: dict):
        pv = self.notional
        day_counter = day_count.DayCount(self.dc_type)
        for i_start_dt in range(len(self.start_accrued_dts)):
            start_dt = self.start_accrued_dts[i_start_dt]
            end_dt = self.end_accrued_dts[i_start_dt]
            if end_dt < value_dt:
                continue
            _schedule = Schedule(start_dt, end_dt, frequency.FrequencyTypes.DAILY, self.cal_type, self.bd_type, self.dg_type)
            
            self.fwd_rates = []
            self.apply_dates = []
            for i in range(len(_schedule.adjusted_dts[1:])):
                (year_frac, num, _) = day_counter.year_frac(_schedule.adjusted_dts[i], _schedule.adjusted_dts[i+1])
                self.apply_dates.append(num)
                if value_dt > _schedule.adjusted_dts[i]:
                    applied_rate = ois_rate_history[_schedule.adjusted_dts[i].datetime().strftime("%Y-%m-%d")]
                    pv *= (1 + applied_rate * year_frac)
                else:
                    # fwd_rate = index_curve.fwd_rate(_schedule.adjusted_dts[i], _schedule.adjusted_dts[i+1], self.dc_type)
                    break
                # self.fwd_rates.append(applied_rate)
        

        pv -= self.notional
        if self.leg_type == global_types.SwapTypes.PAY:
            pv *= -1.0
        return pv
