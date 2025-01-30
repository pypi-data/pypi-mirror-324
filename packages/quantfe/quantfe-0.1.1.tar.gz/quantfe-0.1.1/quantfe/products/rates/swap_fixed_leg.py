# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 7. 12
"""

from typing import Union

from quantfe.utils.error import FinError
from quantfe.utils.date import Date
from quantfe.utils.schedule import Schedule
from quantfe.market.curves.discount_curve import DiscountCurve
from quantfe.utils import global_types, helpers, day_count, frequency, qmath, calendar


class SwapFixedLeg:
    """ Class for managing the fixed leg of a swap. A fixed leg is a leg with
    a sequence of flows calculated according to an ISDA schedule and with a
    coupon that is fixed over the life of the swap. """

    def __init__(self,
                 effective_dt: Date,  # Date interest starts to accrue
                 end_dt: Union[Date, str],  # Date contract ends
                 leg_type: global_types.SwapTypes,
                 coupon: (float),
                 freq_type: frequency.FrequencyTypes,
                 dc_type: day_count.DayCountTypes,
                 notional: float = qmath.ONE_MILLION,
                 principal: float = 0.0,
                 payment_lag: int = 0,
                 cal_type: calendar.CalendarTypes = calendar.CalendarTypes.WEEKEND,
                 bd_type: calendar.BusDayAdjustTypes = calendar.BusDayAdjustTypes.FOLLOWING,
                 dg_type: calendar.DateGenRuleTypes = calendar.DateGenRuleTypes.BACKWARD,
                 end_of_month: bool = False):
        """ Create the fixed leg of a swap contract giving the contract start
        date, its maturity, fixed coupon, fixed leg frequency, fixed leg day
        count convention and notional.  """

        helpers.check_argument_types(self.__init__, locals())
        if type(end_dt) == Date:
            self.termination_dt = end_dt
        else:
            self.termination_dt = effective_dt.add_tenor(end_dt)

        cal = calendar.Calendar(cal_type)

        self.maturity_dt = cal.adjust(self.termination_dt, bd_type)

        if effective_dt > self.maturity_dt:
            raise FinError("Effective date after maturity date")

        self.effective_dt = effective_dt
        self.end_dt = end_dt
        self.leg_type = leg_type
        self.freq_type = freq_type
        self.payment_lag = payment_lag
        self.notional = notional
        self.principal = principal
        self.cpn = coupon

        self.dc_type = dc_type
        self.cal_type = cal_type
        self.bd_type = bd_type
        self.dg_type = dg_type
        self.end_of_month = end_of_month

        self.start_accrued_dts = []
        self.end_accrued_dts = []
        self.payment_dts = []
        self.payments = []
        self.year_fracs = []
        self.accrued_days = []
        self.rates = []

        self.generate_payments()

    ###############################################################################

    def generate_payments(self):
        ''' These are generated immediately as they are for the entire
        life of the swap. Given a valuation date we can determine
        which cash flows are in the future and value the swap
        The schedule allows for a specified lag in the payment date
        Nothing is paid on the swap effective date and so the first payment
        date is the first actual payment date. '''

        schedule = Schedule(self.effective_dt,
                            self.termination_dt,
                            self.freq_type,
                            self.cal_type,
                            self.bd_type,
                            self.dg_type,
                            end_of_month=self.end_of_month)

        schedule_dts = schedule.adjusted_dts

        if len(schedule_dts) < 2:
            raise FinError("Schedule has none or only one date")

        self.start_accrued_dts = []
        self.end_accrued_dts = []
        self.payment_dts = []
        self.payments = []
        self.year_fracs = []
        self.accrued_days = []
        self.rates = []

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

            (year_frac, num, den) = day_counter.year_frac(prev_dt, next_dt)

            self.rates.append(self.cpn)

            payment = year_frac * self.notional * self.cpn

            self.payments.append(payment)
            self.year_fracs.append(year_frac)
            self.accrued_days.append(num)

            prev_dt = next_dt

    ###############################################################################

    def value(self, value_dt: Date, discount_curve: DiscountCurve):
        self.payment_dfs = []
        self.payment_pvs = []
        self.cumulative_pvs = []

        notional = self.notional
        df_value = discount_curve.cal_df(value_dt)

        leg_pv = 0.0
        num_payments = len(self.payment_dts)

        df_payment = 0.0
        for i_pmnt in range(0, num_payments):
            payment_dt = self.payment_dts[i_pmnt]
            pmnt_amount = self.payments[i_pmnt]
            if payment_dt > value_dt:
                df_payment = discount_curve.cal_df(payment_dt) / df_value
                if i_pmnt == num_payments-1:
                    payment_pv = (pmnt_amount + notional) * df_payment
                else:
                    payment_pv = pmnt_amount * df_payment
                    
                leg_pv += payment_pv

                self.payment_dfs.append(df_payment)
                self.payment_pvs.append(pmnt_amount*df_payment)
                self.cumulative_pvs.append(leg_pv)

            else:
                self.payment_dfs.append(0.0)
                self.payment_pvs.append(0.0)
                self.cumulative_pvs.append(0.0)

        if payment_dt > value_dt:
            payment_pv = self.principal * df_payment * notional
            self.payment_pvs[-1] += payment_pv
            leg_pv += payment_pv
            self.cumulative_pvs[-1] = leg_pv

        leg_pv -= self.notional
        if self.leg_type == global_types.SwapTypes.PAY:
            leg_pv = leg_pv * (-1.0)

        return leg_pv 

    ##########################################################################

    def print_payments(self):
        """ Prints the fixed leg dates, accrual factors, discount factors,
        cash amounts, their present value and their cumulative PV using the
        last valuation performed. """

        print("START DATE:", self.effective_dt)
        print("MATURITY DATE:", self.maturity_dt)
        print("COUPON (%):", self.cpn * 100)
        print("FREQUENCY:", str(self.freq_type))
        print("DAY COUNT:", str(self.dc_type))

        if len(self.payments) == 0:
            print("Payments not calculated.")
            return

        header = ["PAY_NUM", "PAY_dt", "ACCR_START", "ACCR_END",
                  "DAYS", "YEARFRAC", "RATE", "PMNT"]

        rows = []
        num_flows = len(self.payment_dts)
        for i_flow in range(0, num_flows):
            rows.append([
                i_flow + 1,
                self.payment_dts[i_flow],
                self.start_accrued_dts[i_flow],
                self.end_accrued_dts[i_flow],
                self.accrued_days[i_flow],
                round(self.year_fracs[i_flow], 4),
                round(self.rates[i_flow] * 100.0, 4),
                round(self.payments[i_flow], 2),
            ])

        table = helpers.format_table(header, rows)
        print("\nPAYMENTS SCHEDULE:")
        print(table)

    ###############################################################################

    def print_valuation(self):
        """ Prints the fixed leg dates, accrual factors, discount factors,
        cash amounts, their present value and their cumulative PV using the
        last valuation performed. """

        print("START DATE:", self.effective_dt)
        print("MATURITY DATE:", self.maturity_dt)
        print("COUPON (%):", self.cpn * 100)
        print("FREQUENCY:", str(self.freq_type))
        print("DAY COUNT:", str(self.dc_type))

        if len(self.payments) == 0:
            print("Payments not calculated.")
            return

        header = ["PAY_NUM", "PAY_dt", "NOTIONAL", "RATE", "PMNT", "DF", "PV", "CUM_PV"]

        rows = []
        num_flows = len(self.payment_dts)
        for i_flow in range(0, num_flows):
            rows.append([
                i_flow + 1,
                self.payment_dts[i_flow],
                round(self.notional, 0),
                round(self.rates[i_flow] * 100.0, 4),
                round(self.payments[i_flow], 2),
                round(self.payment_dfs[i_flow], 4),
                round(self.payment_pvs[i_flow], 2),
                round(self.cumulative_pvs[i_flow], 2),
            ])

        table = helpers.format_table(header, rows)
        print("\nPAYMENTS VALUATION:")
        print(table)

    ##########################################################################

    def __repr__(self):
        s = helpers.label_to_string("OBJECT TYPE", type(self).__name__)
        s += helpers.label_to_string("START DATE", self.effective_dt)
        s += helpers.label_to_string("TERMINATION DATE", self.termination_dt)
        s += helpers.label_to_string("MATURITY DATE", self.maturity_dt)
        s += helpers.label_to_string("NOTIONAL", self.notional)
        s += helpers.label_to_string("PRINCIPAL", self.principal)
        s += helpers.label_to_string("LEG TYPE", self.leg_type)
        s += helpers.label_to_string("COUPON", self.cpn)
        s += helpers.label_to_string("FREQUENCY", self.freq_type)
        s += helpers.label_to_string("DAY COUNT", self.dc_type)
        s += helpers.label_to_string("CALENDAR", self.cal_type)
        s += helpers.label_to_string("BUS DAY ADJUST", self.bd_type)
        s += helpers.label_to_string("DATE GEN TYPE", self.dg_type)
        return s

    ###############################################################################

    def _print(self):
        """ Print a list of the unadjusted coupon payment dates used in
        analytic calculations for the bond. """
        print(self)

    ###############################################################################