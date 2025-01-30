# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 7. 12
"""

import numpy as np
import scipy.stats as ss

from quantfe.utils.error import FinError
from quantfe.utils import global_types, helpers

class Bachelier():
    """Bachelier's Model which prices call and put options in the forward
    measure assuming the underlying rate follows a normal process.
    """

    def __init__(self, volatility):
        """Create FinModel black using parameters."""
        self.volatility = volatility

###############################################################################

    def value(self,
              forward_rate,   # Forward rate F
              strike_rate,    # Strike Rate K
              time_to_expiry,  # Time to Expiry (years)
              df,            # Discount Factor to expiry date
              call_or_put):    # Call or put
        """Price a call or put option using Bachelier's model."""
        f = forward_rate
        t = time_to_expiry
        k = strike_rate
        root_t = np.sqrt(t)
        v = self.volatility
        d = (f-k) / (v * root_t)

        if call_or_put == global_types.OptionTypes.EUROPEAN_CALL:
            return df * ((f - k) * ss.norm.cdf(d) + v * root_t * ss.norm.pdf(d))
        elif call_or_put == global_types.OptionTypes.EUROPEAN_PUT:
            return df * ((k - f) * ss.norm.cdf(-d) + v * root_t * ss.norm.pdf(d))
        else:
            raise FinError("Option type must be a European Call(C) or Put(P)")

###############################################################################

    def __repr__(self):
        s = helpers.label_to_string("OBJECT TYPE", type(self).__name__)
        s += helpers.label_to_string("VOLATILITY", self.volatility)
        return s

###############################################################################