# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 9. 19
"""

import numpy as np
from typing import Union

from ...market.curves.discount_curve import DiscountCurve
from ...market.curves.interpolator import InterpTypes

from ...utils.date import Date
from ...utils.day_count import DayCountTypes
from ...utils.frequency import FrequencyTypes
from ...utils import helpers



class DiscountCurveFlat(DiscountCurve):
    """A very simple discount curve based on a single zero rate with its
    own specified compounding method. Hence, the curve is assumed to be flat.
    It is used for quick and dirty analysis and when limited information is
    available. It inherits several methods from DiscountCurve. """

    ###############################################################################

    def __init__(self,
                 value_dt: Date,
                 flat_rate: Union[float, np.ndarray],
                 freq_type: FrequencyTypes = FrequencyTypes.CONTINUOUS,
                 dc_type: DayCountTypes = DayCountTypes.ACT_ACT_ISDA):
        """ Create a discount curve which is flat. This is very useful for
        quick testing and simply requires a curve date a rate and a compound
        frequency. As we have entered a rate, a corresponding day count
        convention must be used to specify how time periods are to be measured.
        As the curve is flat, no interpolation scheme is required.
        """
#        super().__init__()

        helpers.check_argument_types(self.__init__, locals())

        self.value_dt = value_dt
        self.flat_rate = flat_rate
        self.freq_type = freq_type
        self.dc_type = dc_type

        # This is used by some inherited functions, so we choose the simplest
        self._interp_type = InterpTypes.FLAT_FWD_RATES

        # Need to set up a grid of times and discount factors
        years = np.linspace(0.0, 10.0, 41)
        dts = self.value_dt.add_years(years)

        # Set up a grid of times and discount factors for functions
        self._dfs = self.cal_df(dts)
        self._times = helpers.times_from_dates(dts, self.value_dt, dc_type)

    ###############################################################################

    def bump(self, bump_size: float):
        """ Create a new FinDiscountCurveFlat object with the entire curve
        bumped up by the bumpsize. All other parameters are preserved."""

        rate_bumped = self.flat_rate + bump_size
        disc_curve = DiscountCurveFlat(self.value_dt,
                                       rate_bumped,
                                       freq_type=self.freq_type,
                                       dc_type=self.dc_type)
        return disc_curve

    ###############################################################################

    def cal_df(self, dts: Union[Date, list]):
        """ Return discount factors given a single or vector of dts. The
        discount factor depends on the rate and this in turn depends on its
        compounding frequency, and it defaults to continuous compounding. It
        also depends on the day count convention. This was set in the
        construction of the curve to be ACT_ACT_ISDA. """

        # Get day count times to use with curve day count convention
        dc_times = helpers.times_from_dates(dts, self.value_dt, self.dc_type)

        dfs = self._zero_to_df(self.value_dt,
                               self.flat_rate,
                               dc_times,
                               self.freq_type,
                               self.dc_type)

        if isinstance(dts, Date):
            return dfs[0]

        return np.array(dfs)

    ###############################################################################

    def __repr__(self):
        s = helpers.label_to_string("OBJECT TYPE", type(self).__name__)
        s += helpers.label_to_string("VALUE DATE", (self.value_dt))
        s += helpers.label_to_string("FLAT RATE", (self.flat_rate))
        s += helpers.label_to_string("FREQUENCY", (self.freq_type))
        s += helpers.label_to_string("DAY COUNT", (self.dc_type))
        return s

    ###############################################################################

    def _print(self):
        """ Simple print function for backward compatibility. """
        print(self)

###############################################################################