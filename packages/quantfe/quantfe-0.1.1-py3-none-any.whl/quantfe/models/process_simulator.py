# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 8. 29
"""

from math import sqrt, exp, log
from enum import Enum

from numba import njit, float64, int64
import numpy as np

from quantfe.market.volatility.fx_volatility_surface import FXVolSurface

from quantfe.utils.error import FinError
from quantfe.utils.qmath import norminvcdf

###############################################################################


class ProcessTypes(Enum):
    GBM = 1 # Geometric Brownian Motion
    CIR = 2 # Cox-Ingersoll-Ross
    HESTON = 3 # Heston
    VASICEK = 4 # Vasicek
    CEV = 5 # Constant Elasticity of Variance
    JUMP_DIFFUSION = 6 # Jump Diffusion

###############################################################################

class ProcessSimulator():
    def __init__(self):
        pass

    def get_process(self,
                    process_type: ProcessTypes,
                    t,
                    model_params,
                    num_annual_steps: int, # number of steps per annual
                    num_paths: int,
                    seed: int = 8086):
        
        if process_type == ProcessTypes.GBM:
            (underlying_price, drift, volatility, scheme) = model_params
            if isinstance(t, float):
                paths = get_gbm_paths(num_paths, num_annual_steps, t, drift, underlying_price, volatility, scheme.value, seed)
            elif isinstance(t, np.ndarray):
                paths = get_gbm_paths_discrete_time(num_paths, t, drift, underlying_price, volatility, scheme.value, seed)
            return paths


###############################################################################


class GBMNumericalScheme(Enum):
    NORMAL = 1
    ANTITHETIC = 2

###############################################################################


# @njit(float64[:, :](int64, int64, float64, float64, float64, float64, int64, int64), cache=True, fastmath=True)
def get_gbm_paths(num_paths, num_annual_steps, tow, mu, stock_price, volatility, scheme, seed):
    np.random.seed(seed)
    dt = 1.0 / num_annual_steps
    num_time_steps = int(tow / dt + 0.50)
    vsqrt_dt = 0.0
    m = 0.0

    if isinstance(volatility, float): # constant volatility
        vsqrt_dt = volatility * sqrt(dt)
        m = exp((mu - volatility * volatility / 2.0) * dt)

        if scheme == GBMNumericalScheme.NORMAL.value:
            s_all = np.empty((num_paths, num_time_steps + 1))
            s_all[:, 0] = stock_price

            for it in range(1, num_time_steps + 1):
                g1D = np.random.standard_normal((num_paths))
                w = np.exp(g1D * vsqrt_dt)
                s_all[:, it] = s_all[:, it - 1] * m * w
                # for ip in range(0, num_paths):
                #     w = np.exp(g1D[ip] * vsqrt_dt)
                #     s_all[ip, it] = s_all[ip, it - 1] * m * w

        elif scheme == GBMNumericalScheme.ANTITHETIC.value:
            s_all = np.empty((2 * num_paths, num_time_steps + 1))
            s_all[:, 0] = stock_price
            for it in range(1, num_time_steps + 1):
                g1D = np.random.standard_normal((num_paths))
                for ip in range(0, num_paths):
                    w = np.exp(g1D[ip] * vsqrt_dt)
                    s_all[ip, it] = s_all[ip, it - 1] * m * w
                    s_all[ip + num_paths, it] = s_all[ip + num_paths, it - 1] * m / w

        else:
            raise FinError("Unknown GBMNumericalScheme")
 
    if isinstance(volatility, FXVolSurface): # volatility surface
        if scheme == GBMNumericalScheme.NORMAL.value:
            s_all = np.empty((num_paths, num_time_steps + 1))
            s_all[:, 0] = stock_price
            for it in range(1, num_time_steps + 1):
                g1D = np.random.standard_normal((num_paths))
                for ip in range(0, num_paths):
                    _vol = volatility.volatility(s_all[ip, it - 1], it * dt)
                    vsqrt_dt = _vol * sqrt(dt)
                    m = exp((mu - _vol * _vol / 2.0) * dt)
                    w = np.exp(g1D[ip] * vsqrt_dt)
                    s_all[ip, it] = s_all[ip, it - 1] * m * w
        
#    m = np.mean(s_all[:, -1])
#    v = np.var(s_all[:, -1]/s_all[:, 0])
#    print("GBM", num_paths, num_annual_steps, t, mu, stock_price, sigma, scheme, m,v)

    return s_all

def get_gbm_paths_discrete_time(num_paths, tow_array, mu, underlying_price, volatility, scheme, seed):
    np.random.seed(seed)

    if isinstance(volatility, float): # constant volatility
        _tow_array = np.insert(tow_array, 0, 0)
        if scheme == GBMNumericalScheme.NORMAL.value:
            s_all = np.empty((num_paths, len(_tow_array)))
            s_all[:, 0] = underlying_price
            # import pdb; pdb.set_trace()
            for it in range(1, len(_tow_array)):
                dt = _tow_array[it] - _tow_array[it - 1]
                vsqrt_dt = volatility * sqrt(dt)
                m = exp((mu - volatility * volatility / 2.0) * dt)
                g1D = np.random.standard_normal((num_paths))
                w = np.exp(g1D * vsqrt_dt)
                s_all[:, it] = s_all[:, it - 1] * m * w

        else:
            raise FinError("Unknown GBMNumericalScheme")
    
    elif isinstance(volatility, FXVolSurface):
        _tow_array = np.insert(tow_array, 0, 0)
        if scheme == GBMNumericalScheme.NORMAL.value:
            s_all = np.empty((num_paths, len(_tow_array)))
            s_all[:, 0] = underlying_price
            for it in range(1, len(_tow_array)):
                g1D = np.random.standard_normal((num_paths))
                dt = _tow_array[it] - _tow_array[it - 1]
                for ip in range(0, num_paths):
                    _vol = volatility.volatility(s_all[ip, it - 1], it * dt)
                    vsqrt_dt = _vol * sqrt(dt)
                    m = exp((mu - _vol * _vol / 2.0) * dt)
                    w = np.exp(g1D[ip] * vsqrt_dt)
                    s_all[ip, it] = s_all[ip, it - 1] * m * w

    else:
        raise FinError("Unknown volatility type")

    return s_all
###############################################################################