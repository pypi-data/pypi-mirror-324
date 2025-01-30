# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 7. 14
"""

import numpy as np
import math
from numba import njit, float64, int64

from quantfe.utils.error import FinError
from quantfe.utils.date import Date
from quantfe.utils import calendar, helpers, frequency, day_count
import quantfe.market.curves.interpolator as interp

USE_FLAT_HAZARD_RATE_INTEGRAL = True
STANDARD_RECOVERY_RATE = 0.40
GLOB_NUM_STEPS_PER_YEAR = 25


@njit(float64[:](float64, float64, float64[:], float64[:], float64[:], float64[:], float64[:], float64[:], int64), fastmath=True, cache=True)
def _risky_pv01_numba(teff,
                      accrual_factor_pcd_to_now,
                      payment_times,
                      year_fracs,
                      np_ibor_times,
                      np_ibor_values,
                      np_surv_times,
                      np_surv_values,
                      pv01_method):
    """ Fast calculation of the risky PV01 of a CDS using NUMBA.
    The output is a numpy array of the full and clean risky PV01."""

    method = interp.InterpTypes.FLAT_FWD_RATES.value

    if 1 == 0:
        print("===================")
        print("Teff", teff)
        print("Acc", accrual_factor_pcd_to_now)
        print("Payments", payment_times)
        print("Alphas", year_fracs)
        print("QTimes", np_surv_times)
        print("QValues", np_surv_values)

    cpnAccruedIndicator = 1

    # Method 0 : This is the market standard which assumes that the cpn
    # accrued is treated as though on average default occurs roughly midway
    # through a cpn period.

    tncd = payment_times[0]

    # The first cpn is a special case which needs to be handled carefully
    # taking into account what cpn has already accrued and what has not
    qeff = interp._uinterpolate(teff, np_surv_times, np_surv_values, method)
    q1 = interp._uinterpolate(tncd, np_surv_times, np_surv_values, method)
    z1 = interp._uinterpolate(tncd, np_ibor_times, np_ibor_values, method)

    # this is the part of the cpn accrued from previous cpn date to now
    # accrual_factor_pcd_to_now = day_count.year_frac(pcd,teff)

    # reference credit survives to the premium payment date
    full_rpv01 = q1 * z1 * year_fracs[1]

    # cpn accrued from previous cpn to today paid in full at default
    # before cpn payment
    full_rpv01 = full_rpv01 + z1 * \
        (qeff - q1) * accrual_factor_pcd_to_now * cpnAccruedIndicator

    # future accrued from now to cpn payment date assuming default roughly
    # midway
    full_rpv01 += 0.5 * z1 * \
        (qeff - q1) * (year_fracs[1] - accrual_factor_pcd_to_now) \
        * cpnAccruedIndicator

    for it in range(1, len(payment_times)):

        t2 = payment_times[it]

        q2 = interp._uinterpolate(t2, np_surv_times, np_surv_values, method)
        z2 = interp._uinterpolate(t2, np_ibor_times, np_ibor_values, method)

        accrual_factor = year_fracs[it]

        # full cpn is paid at the end of the current period if survives to
        # payment date
        full_rpv01 += q2 * z2 * accrual_factor

        #######################################################################

        if cpnAccruedIndicator == 1:

            if USE_FLAT_HAZARD_RATE_INTEGRAL:
                # This needs to be updated to handle small h+r
                tau = accrual_factor
                h12 = -math.log(q2 / q1) / tau
                r12 = -math.log(z2 / z1) / tau
                alpha = h12 + r12
                exp_term = 1.0 - math.exp(-alpha * tau) - alpha * \
                    tau * math.exp(-alpha * tau)
                d_full_rpv01 = q1 * z1 * h12 * \
                    exp_term / abs(alpha * alpha + 1e-20)
            else:
                d_full_rpv01 = 0.50 * (q1 - q2) * z2 * accrual_factor

            full_rpv01 = full_rpv01 + d_full_rpv01

        q1 = q2

    clean_rpv01 = full_rpv01 - accrual_factor_pcd_to_now

    return np.array([full_rpv01, clean_rpv01])

###############################################################################

@njit(float64(float64, float64, float64[:], float64[:], float64[:], float64[:], float64, int64, int64), fastmath=True, cache=True)
def _prot_leg_pv_numba(teff,
                        t_mat,
                        np_ibor_times,
                        np_ibor_values,
                        np_surv_times,
                        np_surv_values,
                        contract_recovery_rate,
                        num_steps_per_year,
                        prot_method):
    """ Fast calculation of the CDS protection leg PV using NUMBA to speed up
    the numerical integration over time. """

    method = interp.InterpTypes.FLAT_FWD_RATES.value
    dt = 1.0 / num_steps_per_year
    num_steps = int((t_mat-teff) * num_steps_per_year + 0.50)
    dt = (t_mat - teff) / num_steps

    t = teff
    z1 = interp._uinterpolate(t, np_ibor_times, np_ibor_values, method)
    q1 = interp._uinterpolate(t, np_surv_times, np_surv_values, method)

    prot_pv = 0.0
    small = 1e-8

    if USE_FLAT_HAZARD_RATE_INTEGRAL:

        for _ in range(0, num_steps):
            t = t + dt
            z2 = interp._uinterpolate(t, np_ibor_times, np_ibor_values, method)
            q2 = interp._uinterpolate(t, np_surv_times, np_surv_values, method)
            # This needs to be updated to handle small h+r
            h12 = -math.log(q2 / q1) / dt
            r12 = -math.log(z2 / z1) / dt
            exp_term = math.exp(-(r12 + h12) * dt)
            dprot_pv = h12 * (1.0 - exp_term) * q1 * z1 / \
                (abs(h12 + r12) + small)
            prot_pv += dprot_pv
            q1 = q2
            z1 = z2

    else:

        for _ in range(0, num_steps):
            t += dt
            z2 = interp._uinterpolate(t, np_ibor_times, np_ibor_values, method)
            q2 = interp._uinterpolate(t, np_surv_times, np_surv_values, method)
            dq = q1 - q2
            dprot_pv = 0.5 * (z1 + z2) * dq
            prot_pv += dprot_pv
            q1 = q2
            z1 = z2

    prot_pv = prot_pv * (1.0 - contract_recovery_rate)
    return prot_pv

###############################################################################


class CDS:
    """ A class which manages a Credit Default Swap. It performs schedule
    generation and the valuation and risk management of CDS. """

    def __init__(self,
                 step_in_dt: Date,  # Date protection starts
                 maturity_dt_or_tenor: (Date, str),  # Date or tenor
                 running_cpn: float,  # Annualised cpn on premium fee leg
                 notional: float = math.ONE_MILLION,
                 long_protect: bool = True,
                 freq_type: frequency.FrequencyTypes = frequency.FrequencyTypes.QUARTERLY,
                 dc_type: day_count.DayCountTypes = day_count.DayCountTypes.ACT_360,
                 cal_type: calendar.CalendarTypes = calendar.CalendarTypes.WEEKEND,
                 bd_type: calendar.BusDayAdjustTypes = calendar.BusDayAdjustTypes.FOLLOWING,
                 dg_type: calendar.DateGenRuleTypes = calendar.DateGenRuleTypes.BACKWARD):
        """ Create a CDS from the step-in date, maturity date and cpn """

        helpers.check_argument_types(self.__init__, locals())

        if isinstance(maturity_dt_or_tenor, Date):
            maturity_dt = maturity_dt_or_tenor
        else:
            # To get the next CDS date we move on by the tenor and then roll to
            # the next CDS date after that. We do not holiday adjust it. That
            # is handled in the schedule generation.
            maturity_dt = step_in_dt.add_tenor(maturity_dt_or_tenor)
            maturity_dt = maturity_dt.next_cds_date()

        if step_in_dt > maturity_dt:
            raise FinError("Step in date after maturity date")

        self.step_in_dt = step_in_dt
        self.maturity_dt = maturity_dt
        self.running_cpn = running_cpn
        self.notional = notional
        self.long_protect = long_protect
        self.dc_type = dc_type
        self.dg_type = dg_type
        self.cal_type = cal_type
        self.freq_type = freq_type
        self.bd_type = bd_type

        self._generate_adjusted_cds_payment_dts()
        self._calc_flows()

    ###########################################################################

    def _generate_adjusted_cds_payment_dts(self):
        """ Generate CDS payment dates which have been holiday adjusted."""
        freq = frequency.annual_frequency(self.freq_type)
        cal = calendar.Calendar(self.cal_type)
        start_dt = self.step_in_dt

        self.payment_dts = []
        self.accrual_start_dts = []
        self.accrual_end_dts = []
        num_months = int(12.0 / freq)

        # We generate unadjusted dates - not adjusted for weekends or holidays
        unadjusted_schedule_dts = []

        if self.dg_type == calendar.DateGenRuleTypes.BACKWARD:

            # We start at end date and step backwards

            next_dt = self.maturity_dt

            unadjusted_schedule_dts.append(next_dt)

            # the unadjusted dates start at end date and end at previous
            # cpn date
            while next_dt > start_dt:
                next_dt = next_dt.add_months(-num_months)
                unadjusted_schedule_dts.append(next_dt)

            # now we adjust for holiday using business day adjustment
            # convention specified
            adjusted_dts = []

            for date in reversed(unadjusted_schedule_dts):
                adjusted = cal.adjust(date, self.bd_type)
                adjusted_dts.append(adjusted)
                
        # eg: https://www.cdsmodel.com/assets/cds-model/docs/Standard%20CDS%20Examples.pdf
        # Payment       = [20-MAR-2009, 22-JUN-2009, 21-SEP-2009, 21-DEC-2009, 22-MAR-2010]
        # Accrual Start = [22-DEC-2008, 20-MAR-2009, 22-JUN-2009, 21-SEP-2009, 21-DEC-2009]
        # Accrual End   = [19-MAR-2009, 21-JUN-2009, 20-SEP-2009, 20-DEC-2009, 20-MAR-2010]

        elif self.dg_type == calendar.DateGenRuleTypes.FORWARD:

            # We start at start date and step forwards

            next_dt = start_dt

            # the unadjusted dates start at start date and end at last date
            # before maturity date
            while next_dt < self.maturity_dt:
                unadjusted_schedule_dts.append(next_dt)
                next_dt = next_dt.add_months(num_months)

            # We then append the maturity date
            unadjusted_schedule_dts.append(self.maturity_dt)

            adjusted_dts = []
            for date in unadjusted_schedule_dts:
                adjusted = calendar.adjust(date, self.bd_type)
                adjusted_dts.append(adjusted)

    # eg. Date(20, 2, 2009) to Date(20, 3, 2010) with DateGenRuleTypes.FORWARD
    # Payment       = [20-MAY-2009, 20-AUG-2009, 20-NOV-2009, 22-FEB-2010]
    # Accrual Start = [20-FEB-2009, 20-MAY-2009, 20-AUG-2009, 20-NOV-2009]
    # Accrual End   = [19-MAY-2009, 19-AUG-2009, 19-NOV-2009, 20-MAR-2010]

        else:
            raise FinError("Unknown DateGenRuleType:" + str(self.dg_type))

        # We only include dates which fall after the CDS start date
        self.payment_dts = adjusted_dts[1:]

        # Accrual start dates run from previous cpn date to penultimate
        # cpn date
        self.accrual_start_dts = adjusted_dts[:-1]

        # Accrual end dates are one day before the start of the next
        # accrual period
        self.accrual_end_dts = [
            date.add_days(-1) for date in self.accrual_start_dts[1:]]

        # Final accrual end date is the maturity date
        self.accrual_end_dts.append(self.maturity_dt)

    ###########################################################################

    # To be continued...