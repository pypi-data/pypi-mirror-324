# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 9. 3
"""

import numpy as np
from enum import Enum

from quantfe.utils import helpers, global_types
from quantfe.utils.error import FinError

from quantfe.models.model import Model
from quantfe.models.black_scholes_analytic import bs_value, baw_value, bjerksund_stensland_value
from quantfe.models.equity_crr_tree import crr_tree_val_avg
from quantfe.models.finite_difference import black_scholes_fd


class BlackScholesTypes(Enum):
    DEFAULT = 0
    ANALYTICAL = 1
    CRR_TREE = 2
    BARONE_ADESI = 3
    LSMC = 4
    Bjerksund_Stensland = 5
    FINITE_DIFFERENCE = 6
    PSOR = 7

###############################################################################


class BlackScholes(Model):
    def __init__(self,
                 volatility: (float, np.ndarray),
                 bs_type: BlackScholesTypes = BlackScholesTypes.DEFAULT,
                 num_steps_per_year=52,
                 num_paths=10000,
                 seed=42,
                 use_sobol=False,
                 params=None):
        
        helpers.check_argument_types(self.__init__, locals())

        self.volatility = volatility
        self.bs_type = bs_type
        self.num_steps_per_year = num_steps_per_year
        self.num_paths = num_paths
        self.seed = seed
        self.use_sobol = use_sobol
        self.params = params if params else {}
        self.poly_degree = None
        self.fit_type = None

    ###########################################################################

    def value(self,
              spot_price: float,
              time_to_expiry: float,
              strike_price: float,
              risk_free_rate: float,
              dividend_rate: float,
              option_type: global_types.OptionTypes):
        
        if option_type == global_types.OptionTypes.EUROPEAN_CALL or option_type == global_types.OptionTypes.EUROPEAN_PUT:
            if self.bs_type is BlackScholesTypes.DEFAULT:
                self.bs_type = BlackScholesTypes.ANALYTICAL

            if self.bs_type == BlackScholesTypes.ANALYTICAL:
                v = bs_value(spot_price,
                             time_to_expiry,
                             strike_price,
                             risk_free_rate,
                             dividend_rate,
                             self.volatility,
                             option_type.value)

                return v

            elif self.bs_type == BlackScholesTypes.CRR_TREE:
                v = crr_tree_val_avg(spot_price,
                                     risk_free_rate,
                                     dividend_rate,
                                     self.volatility,
                                     self.num_steps_per_year,
                                     time_to_expiry,
                                     option_type.value,
                                     strike_price)['value']

                return v

            elif self.bs_type == BlackScholesTypes.FINITE_DIFFERENCE:
                v = black_scholes_fd(spot_price=spot_price,
                                     time_to_expiry=time_to_expiry,
                                     strike_price=strike_price,
                                     risk_free_rate=risk_free_rate,
                                     dividend_yield=dividend_rate,
                                     volatility=self.volatility,
                                     option_type=option_type.value,
                                     **self.params)

                return v 
            
            else:
                raise FinError("Implementation not available for this product")

        elif option_type == global_types.OptionTypes.AMERICAN_CALL or option_type == global_types.OptionTypes.AMERICAN_PUT:
            if self.bs_type is BlackScholesTypes.DEFAULT:
                self.bs_type = BlackScholesTypes.CRR_TREE

            if self.bs_type == BlackScholesTypes.BARONE_ADESI:
                if option_type == global_types.OptionTypes.AMERICAN_CALL:
                    phi = +1
                elif option_type == global_types.OptionTypes.AMERICAN_PUT:
                    phi = -1

                v = baw_value(spot_price,
                              time_to_expiry,
                              strike_price,
                              risk_free_rate,
                              dividend_rate,
                              self.volatility,
                              phi)

                return v

            elif self.bs_type == BlackScholesTypes.CRR_TREE:
                v = crr_tree_val_avg(spot_price,
                                     risk_free_rate,
                                     dividend_rate,
                                     self.volatility,
                                     self.num_steps_per_year,
                                     time_to_expiry,
                                     option_type.value,
                                     strike_price)['value']

                return v

            elif self.bs_type == BlackScholesTypes.Bjerksund_Stensland:
                v = bjerksund_stensland_value(spot_price,
                                              time_to_expiry,
                                              strike_price,
                                              risk_free_rate,
                                              dividend_rate,
                                              self.volatility,
                                              option_type.value)
                return v

            elif self.bs_type == BlackScholesTypes.FINITE_DIFFERENCE:
                v = black_scholes_fd(spot_price=spot_price,
                                     time_to_expiry=time_to_expiry,
                                     strike_price=strike_price,
                                     risk_free_rate=risk_free_rate,
                                     dividend_yield=dividend_rate,
                                     volatility=self.volatility,
                                     option_type=option_type.value,
                                     **self.params)
                return v

            else:
                raise FinError("Implementation not available for this product")
        else:
            raise FinError("Should not be here")

###############################################################################