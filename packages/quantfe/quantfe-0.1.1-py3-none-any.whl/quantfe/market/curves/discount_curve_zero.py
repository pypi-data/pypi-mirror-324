# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 9. 3
"""

import numpy as np
from typing import Union

from quantfe.market.curves.discount_curve import DiscountCurve
from quantfe.market.curves.interpolator import InterpTypes, Interpolator

from quantfe.utils import helpers
from quantfe.utils.frequency import FrequencyTypes
from quantfe.utils.day_count import DayCountTypes
from quantfe.utils.error import FinError
from quantfe.utils.date import Date
from quantfe.utils.qmath import test_monotonicity


class DiscountCurveZeros(DiscountCurve):
    """ This is a curve calculated from a set of dates and zero rates. As we
    have rates as inputs, we need to specify the corresponding compounding
    frequency. Also to go from rates and dates to discount factors we need to
    compute the year fraction correctly and for this we require a day count
    convention. Finally, we need to interpolate the zero rate for the times
    between the zero rates given and for this we must specify an interpolation
    convention. The class inherits methods from FinDiscountCurve. """

    ###############################################################################

    def __init__(self,
                 value_dt: Date,
                 zero_dts: list,
                 zero_rates: Union[list, np.ndarray],
                 freq_type: FrequencyTypes = FrequencyTypes.ANNUAL,
                 dc_type: DayCountTypes = DayCountTypes.ACT_ACT_ISDA,
                 interp_type: InterpTypes = InterpTypes.FLAT_FWD_RATES):
        """ Create the discount curve from a vector of dates and zero rates
        factors. The first date is the curve anchor. Then a vector of zero
        dates and then another same-length vector of rates. The rate is to the
        corresponding date. We must specify the compounding frequency of the
        zero rates and also a day count convention for calculating times which
        we must do to calculate discount factors. Finally we specify the
        interpolation scheme for off-grid dates."""

        helpers.check_argument_types(self.__init__, locals())

        # Validate curve
        if len(zero_dts) == 0:
            raise FinError("Dates has zero length")

        if len(zero_dts) != len(zero_rates):
            raise FinError("Dates and Rates are not the same length")

        if freq_type not in FrequencyTypes:
            raise FinError("Unknown Frequency type " + str(freq_type))

        if dc_type not in DayCountTypes:
            raise FinError("Unknown Cap Floor DayCountRule type " + str(dc_type))

        self.value_dt = value_dt
        self.freq_type = freq_type
        self.dc_type = dc_type
        self._zero_rates = np.array(zero_rates)
        self._zero_dts = zero_dts
        self._times = helpers.times_from_dates(zero_dts, value_dt, dc_type)

        if test_monotonicity(self._times) is False:
            raise FinError("Times or dates are not sorted in increasing order")

        dfs = self._zero_to_df(self.value_dt,
                               self._zero_rates,
                               self._times,
                               self.freq_type,
                               self.dc_type)

        self._dfs = np.array(dfs)
        self._interp_type = interp_type
        self._interpolator = Interpolator(self._interp_type)
        self._interpolator.fit(self._times, self._zero_rates)

    # ###############################################################################

    # def bump(self, bump_size):
    #     """ Calculate the continuous forward rate at the forward date. """

    #     times = self.times.copy()
    #     discount_factors = self._discount_factors.copy()

    #     n = len(self.times)
    #     for i in range(0, n):
    #         t = times[i]
    #         discount_factors[i] = discount_factors[i] * np.exp(-bump_size*t)

    #     disc_curve = FinDiscountCurve(self.value_dt, times,
    #                                  discount_factors,
    #                                  self._interp_type)

    #     return disc_curve

    # ##############################################################################

    def __repr__(self):
        s = helpers.label_to_string("OBJECT TYPE", type(self).__name__)
        s += helpers.label_to_string("VALUATION DATE", self.value_dt)
        s += helpers.label_to_string("FREQUENCY TYPE", (self.freq_type))
        s += helpers.label_to_string("DAY COUNT TYPE", (self.dc_type))
        s += helpers.label_to_string("INTERP TYPE", (self._interp_type))
        s += helpers.label_to_string("DATES", "ZERO RATES")
        num_points = len(self._times)
        for i in range(0, num_points):
            s += helpers.label_to_string("%12s" % self._zero_dts[i], "%10.7f" % self._zero_rates[i])

        return s

    ###############################################################################

    def _print(self):
        """ Simple print function for backward compatibility. """
        print(self)

###############################################################################