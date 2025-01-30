# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 8. 29
"""

import numpy as np
import copy
from scipy.optimize import brentq
from multiprocessing import Pool, cpu_count

from quantfe.market.volatility.fx_volatility_surface import FXVolSurface

from quantfe.models.process_simulator import ProcessSimulator, ProcessTypes

from quantfe.utils import calendar, day_count, frequency
from quantfe.utils.date import Date
from quantfe.utils.schedule import Schedule
from quantfe.utils.error import FinError
from quantfe.utils import global_types, helpers, qmath, global_vars


def calculate_path_value(spot_path, notional, freq_type_value, target_cum_value, df_array, payoff_func):
    cum_positive_value = 0.0
    _pv = 0.0
    for i in range(1, len(spot_path)):
        payoff = payoff_func(spot_path[i])
        leg_payoff = notional / freq_type_value * payoff / spot_path[i]
        if (cum_positive_value + max(payoff, 0)) < target_cum_value:
            _pv += leg_payoff * df_array[i-1]
            cum_positive_value += max(payoff, 0)
        else:   # early redemption
            _pv += notional / freq_type_value * (target_cum_value - cum_positive_value) / spot_path[i] * df_array[i-1]
            cum_positive_value = target_cum_value
            break
    return _pv

###############################################################################

def calculate_vega_for_tenor(i, vol, model_params, value_date, risk_free_rate, process_type, num_ann_obs, num_paths, seed, self):
    up_copied_vol = copy.deepcopy(vol)
    down_copied_vol = copy.deepcopy(vol)
    up_copied_vol.atm_vols[i] += 0.01
    up_copied_vol.build_vol_surface()
    model_params_vol_up = (model_params[0], model_params[1], up_copied_vol, model_params[3])
    price_vol_up = self.value(value_date, risk_free_rate, process_type, model_params_vol_up, num_ann_obs, num_paths, seed)
    down_copied_vol.atm_vols[i] -= 0.01
    down_copied_vol.build_vol_surface()
    model_params_vol_down = (model_params[0], model_params[1], down_copied_vol, model_params[3])
    price_vol_down = self.value(value_date, risk_free_rate, process_type, model_params_vol_down, num_ann_obs, num_paths, seed)
    return vol.tenors[i], (price_vol_up - price_vol_down) / 0.02

###############################################################################


class VanillaTRF:
    """ Class for Target Redemption Forward (TRF). These allows a customer to exchange one currency
    for another at a contract rate that is more attractive compared to the rate on a traditional 
    forward contract. The TARF structure is usually comprised of a series of individual legs that 
    redeem on consecutive expiry dates. 
    """

    def __init__(self,
                long_short_type: global_types.LongShort, 
                strike_fx_rate: float,
                currency_pair: str,
                notional: float,
                notional_currency: str,
                target_cum_value: float,
                start_date: Date,
                maturity_date: Date,
                freq_type: frequency.FrequencyTypes = frequency.FrequencyTypes.MONTHLY,
                dc_type: day_count.DayCountTypes = day_count.DayCountTypes.ACT_365F,
                calendar_type = calendar.CalendarTypes.WEEKEND,
                bda_type = calendar.BusDayAdjustTypes.NONE,
                dg_type = calendar.DateGenRuleTypes.FORWARD,
                settlement_days: int = 2
                ):
        """
        :param 
        - long_short_type: long or short
        - strike_fx_rate: the exchange rate at which the currency pair will be exchanged
        """
        
        helpers.check_argument_types(self.__init__, locals())
        
        self.long_short_type = long_short_type
        self.strike_fx_rate = strike_fx_rate
        self.currency_pair = currency_pair
        self.notional = notional
        self.notional_currency = notional_currency
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.target_cum_value = target_cum_value
        self.freq_type = freq_type
        self.dc_type = dc_type
        self.calendar = calendar_type
        self.bda_type = bda_type
        self.dg_type = dg_type
        self.settlement_days = settlement_days
        self.cum_positive_value = 0.0
        self._calculdate_expiry_dates()

    ###########################################################################

    def _calculdate_expiry_dates(self):
        """ Calculate the expiry dates of the TRF. """
        self.expiry_dates = Schedule(self.start_date, self.maturity_date, self.freq_type, self.calendar, self.bda_type, self.dg_type).generate()[1:]
        unadjusted_dates = Schedule(self.start_date, self.maturity_date, self.freq_type, 
                                    calendar.CalendarTypes.WEEKEND, calendar.BusDayAdjustTypes.NONE, calendar.DateGenRuleTypes.BACKWARD).generate()[1:]
        settlement_dates = []
        cal = calendar.Calendar(self.calendar)
        for _date in unadjusted_dates:
            settlement_date = cal.adjust(_date.add_days(self.settlement_days), calendar.BusDayAdjustTypes.FOLLOWING)
            settlement_dates.append(settlement_date)
        self.settlement_dates = settlement_dates

    ###########################################################################

    def payoff(self, spot: float):
        """ Calculate the payoff of the TRF. """
        if self.long_short_type == global_types.LongShort.LONG:
            return spot - self.strike_fx_rate
        elif self.long_short_type == global_types.LongShort.SHORT:
            return self.strike_fx_rate - spot
        else:
            raise FinError("Invalid long_short_type")
    
    ###########################################################################

    def update_cum_positive_value(self, payoff: float):
        """ Update the cumulative positive value of the TRF. """
        self.cum_positive_value += max(payoff, 0)

    ###########################################################################

    def value(self, 
              value_date: Date, 
              risk_free_rate: float,
              process_type: ProcessTypes,
              model_params,
              num_ann_obs: int = 252,
              num_paths: int = 10000,
              seed: int = 8086):
        """ Value the TRF using Monte Carlo simulation. """

        t = (self.maturity_date - value_date) / global_vars.gDaysInYear
        if t < 0:
            raise FinError("maturity date is before the value date")
        process = ProcessSimulator()
        tows = np.array((np.array(self.expiry_dates) - value_date) / global_vars.gDaysInYear, dtype=np.float64)
        tows = tows[tows > 0]
        settlement_tows = np.array((np.array(self.settlement_dates) - value_date) / global_vars.gDaysInYear, dtype=np.float64)
        settlement_tows = settlement_tows[settlement_tows > 0]
        total_spot_path = process.get_process(process_type, tows, model_params, len(tows), num_paths, seed)
        # Convert risk_free_rate to a numpy array if it's a scalar
        rf = np.full_like(settlement_tows, risk_free_rate)
        df_array = np.exp(np.array(-rf * settlement_tows))

        # Calculate the payoff
        pv = 0.0
        for spot_path in total_spot_path:
            cum_positive_value = self.cum_positive_value
            _pv = 0.0
            for i in range(1, len(spot_path)):
                payoff = self.payoff(spot_path[i])
                leg_payoff = self.notional / self.freq_type.value * payoff / spot_path[i]
                if (cum_positive_value + max(payoff, 0)) < self.target_cum_value:
                    _pv += leg_payoff * df_array[i-1]
                    cum_positive_value += max(payoff, 0)
                else:   # early redemption
                    _pv += self.notional / self.freq_type.value * (self.target_cum_value - cum_positive_value) / spot_path[i] * df_array[i-1]
                    cum_positive_value = self.target_cum_value
                    break
            pv += _pv

        # with Pool(processes=cpu_count()) as pool:
        #     results = pool.starmap(
        #         calculate_path_value,
        #         [(spot_path, self.notional, self.freq_type.value, self.target_cum_value, df_array, self.payoff) for spot_path in total_spot_path]
        #     )
        # pv = sum(results)

        return pv / num_paths

    ###########################################################################

    def find_fair_strike(self, value_date: Date, spot: float, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Find the fair strike of the TRF. """

        def objective(strike):
            self.strike_fx_rate = strike
            return self.value(value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)

        # Define a reasonable range for the strike price
        lower_bound = spot * 0.5
        upper_bound = spot * 2
        
        fair_strike = brentq(objective, lower_bound, upper_bound)
        self.strike_fx_rate = fair_strike
        return fair_strike

    ###########################################################################

    def delta_mc(self, value_date: Date, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Calculate the delta of the TRF using Monte Carlo simulation. """
        spot = model_params[0]
        spot_up = spot * (1 + 0.01)
        spot_down = spot * (1 - 0.01)
        model_params_up = (spot_up,) + model_params[1:]
        model_params_down = (spot_down,) + model_params[1:]

        up_price = self.value(value_date, risk_free_rate, process_type, model_params_up, num_ann_obs, num_paths, seed)
        down_price = self.value(value_date, risk_free_rate, process_type, model_params_down, num_ann_obs, num_paths, seed)
        delta = (up_price - down_price) / (spot_up - spot_down)
        return delta

    def gamma_mc(self, value_date: Date, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Calculate the gamma of the TRF using Monte Carlo simulation. """
        spot = model_params[0]
        spot_up = spot * (1 + 0.01)
        spot_down = spot * (1 - 0.01)
        model_params_up = (spot_up,) + model_params[1:]
        model_params_down = (spot_down,) + model_params[1:]

        price = self.value(value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)
        up_price = self.value(value_date, risk_free_rate, process_type, model_params_up, num_ann_obs, num_paths, seed)
        down_price = self.value(value_date, risk_free_rate, process_type, model_params_down, num_ann_obs, num_paths, seed)
        delta_up = (up_price - price) / (spot_up - spot)
        delta_down = (price - down_price) / (spot - spot_down)
        gamma = (delta_up - delta_down) / (spot_up - spot_down)
        return gamma

    def vega_mc(self, value_date: Date, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Calculate the vega of the TRF using Monte Carlo simulation. """
        vol = model_params[2]
        if isinstance(vol, float):
            vol_up = vol + 0.01
            vol_down = vol - 0.01
            model_params_vol_up = (model_params[0], model_params[1], vol_up, model_params[3])
            model_params_vol_down = (model_params[0], model_params[1], vol_down, model_params[3])
            price_vol_up = self.value(value_date, risk_free_rate, process_type, model_params_vol_up, num_ann_obs, num_paths, seed)
            price_vol_down = self.value(value_date, risk_free_rate, process_type, model_params_vol_down, num_ann_obs, num_paths, seed)
            vega = (price_vol_up - price_vol_down) / 0.02
        elif isinstance(vol, FXVolSurface):
            with Pool(processes=len(vol.atm_vols)) as pool:
                results = pool.starmap(calculate_vega_for_tenor, [(i, vol, model_params, value_date, risk_free_rate, process_type, num_ann_obs, num_paths, seed, self) for i in range(len(vol.atm_vols))])
            vega = dict(results)
            # vega = {}
            # for i in range(len(vol.atm_vols)):
            #     import pdb; pdb.set_trace()
            #     up_copied_vol = copy.deepcopy(vol)
            #     down_copied_vol = copy.deepcopy(vol)
            #     up_copied_vol.atm_vols[i] += 0.01
            #     up_copied_vol.build_vol_surface()
            #     model_params_vol_up = (model_params[0], model_params[1], up_copied_vol, model_params[3])
            #     price_vol_up = self.value(value_date, risk_free_rate, process_type, model_params_vol_up, num_ann_obs, num_paths, seed)
            #     down_copied_vol.atm_vols[i] -= 0.01
            #     down_copied_vol.build_vol_surface()
            #     model_params_vol_down = (model_params[0], model_params[1], down_copied_vol, model_params[3])
            #     price_vol_down = self.value(value_date, risk_free_rate, process_type, model_params_vol_down, num_ann_obs, num_paths, seed)
            #     vega[vol.tenors[i]] = (price_vol_up - price_vol_down) / 0.02
        return vega

    def theta_mc(self, value_date: Date, next_value_date: Date, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Calculate the theta of the TRF using Monte Carlo simulation. """
        if next_value_date >= self.maturity_date:
            raise FinError("next value date is after maturity date")
        price = self.value(value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)
        price_time = self.value(next_value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)
        theta = price_time - price
        return theta

    def get_greeks(self, value_date: Date, next_value_date: Date, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Calculate the greeks of the TRF using Monte Carlo simulation. """
        spot = model_params[0]
        spot_up = spot * (1 + 0.01)
        spot_down = spot * (1 - 0.01)
        model_params_spot_up = (spot_up,) + model_params[1:]
        model_params_spot_down = (spot_down,) + model_params[1:]

        price = self.value(value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)
        price_spot_up = self.value(value_date, risk_free_rate, process_type, model_params_spot_up, num_ann_obs, num_paths, seed)
        price_spot_down = self.value(value_date, risk_free_rate, process_type, model_params_spot_down, num_ann_obs, num_paths, seed)

        delta = (price_spot_up - price_spot_down) / (spot_up - spot_down)
        delta_up = (price_spot_up - price) / (spot_up - spot)
        delta_down = (price - price_spot_down) / (spot - spot_down)
        gamma = (delta_up - delta_down) / (spot_up - spot_down)

        vega = self.vega_mc(value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)

        price_time = self.value(next_value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)
        theta = price_time - price
        return {
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta
        }

###############################################################################


class OptionTRF:
    """ Class for TRF with barrier. """

    def __init__(self,
                 long_short_type: global_types.LongShort, 
                 strike_fx_rate: float,
                 barrier_fx_rate: float,
                 currency_pair: str,
                 notional: float,
                 notional_currency: str,
                 target_cum_value: float,
                 start_date: Date,
                 maturity_date: Date,
                 freq_type: frequency.FrequencyTypes = frequency.FrequencyTypes.MONTHLY,
                 dc_type: day_count.DayCountTypes = day_count.DayCountTypes.ACT_365F,
                 calendar_type = calendar.CalendarTypes.WEEKEND):
        
        helpers.check_argument_types(self.__init__, locals())
        
        self.long_short_type = long_short_type
        self.strike_fx_rate = strike_fx_rate
        self.barrier_fx_rate = barrier_fx_rate
        self.currency_pair = currency_pair
        self.notional = notional
        self.notional_currency = notional_currency
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.target_cum_value = target_cum_value
        self.freq_type = freq_type
        self.dc_type = dc_type
        self.calendar = calendar_type
        self._calculdate_expiry_dates()

    ###########################################################################

    def _calculdate_expiry_dates(self):
        """ Calculate the expiry dates of the TRF. """
        bd_type = calendar.BusDayAdjustTypes.NONE
        dg_type = calendar.DateGenRuleTypes.BACKWARD
        self.expiry_dates = Schedule(self.start_date, self.maturity_date, self.freq_type, self.calendar, bd_type, dg_type).generate()[1:]

    ###########################################################################

    def payoff(self, spot: float):
        """ Calculate the payoff of the TRF. """
        if self.long_short_type == global_types.LongShort.LONG:
            if (spot >= self.barrier_fx_rate) and (spot <= self.strike_fx_rate):
                return 0.0
            else:
                return spot - self.strike_fx_rate
        elif self.long_short_type == global_types.LongShort.SHORT:
            if (spot <= self.barrier_fx_rate) and (spot >= self.strike_fx_rate):
                return 0.0
            else:
                return self.strike_fx_rate - spot
        else:
            raise FinError("Invalid long_short_type")

    ###########################################################################

    def value_mc(self,
                 value_date: Date, 
                 risk_free_rate: float,
                 process_type: ProcessTypes,
                 model_params,
                 num_ann_obs: int = 252,
                 num_paths: int = 10000,
                 seed: int = 8086):
        """ Value the TRF using Monte Carlo simulation. """

        t = (self.maturity_date - value_date) / global_vars.gDaysInYear
        if t < 0:
            raise FinError("Value date is before the start date")
        num_time_steps = int(t * num_ann_obs)

        process = ProcessSimulator()
        total_spot_path = process.get_process(process_type, t, model_params, num_time_steps, num_paths, seed)
        tows = np.array((np.array(self.expiry_dates) - value_date) / global_vars.gDaysInYear, dtype=np.float64)
        # Convert risk_free_rate to a numpy array if it's a scalar
        rf = np.full_like(tows, risk_free_rate)
        df_array = np.exp(np.array(-rf * tows))

        # Calculate the payoff
        pv = 0.0
        for spot_path in total_spot_path:
            cum_positive_value = 0.0
            _pv = 0.0
            for i in range(1, len(spot_path)):
                payoff = self.payoff(spot_path[i])
                # to be continued
                # https://github.com/georgezbh/optionpricing/blob/master/tarf.py
        print("PV: ", pv)
        return pv

    ###########################################################################

    def find_fair_strike(self, value_date: Date, spot: float, risk_free_rate: float, process_type: ProcessTypes, model_params, num_ann_obs: int = 252, num_paths: int = 10000, seed: int = 8086):
        """ Find the fair strike of the TRF. """

        def objective(strike):
            self.strike_fx_rate = strike
            return self.value_mc(value_date, risk_free_rate, process_type, model_params, num_ann_obs, num_paths, seed)

        # Define a reasonable range for the strike price
        lower_bound = spot * 0.5
        upper_bound = spot * 1.5
        
        fair_strike = brentq(objective, lower_bound, upper_bound)
        return fair_strike