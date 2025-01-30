# -*- coding: utf-8 -*-
"""
:Author: Chankyu Choi
:Date: 2024. 7. 15
"""

import numpy as np
import math
import scipy.optimize as so
from numba import njit
from enum import Enum

from quantfe.utils.error import FinError
from quantfe.utils import global_vars, global_types, qmath
from quantfe.market.curves import interpolator as interp

INTERP = interp.InterpType.FLAT_FWD_RATES.value


###############################################################################
# dr = (theta(t) - a * r) dt + sigma * dW
###############################################################################


class HWEuropeanCalcType(Enum):
    JAMSHIDIAN = 1
    EXPIRY_ONLY = 2
    EXPIRT_TREE = 3


def option_exercise_types_to_int(option_exercise_type):
    if option_exercise_type == global_types.ExerciseTypes.EUROPEAN:
        return 1
    elif option_exercise_type == global_types.ExerciseTypes.BERMUDAN:
        return 2
    elif option_exercise_type == global_types.ExerciseTypes.AMERICAN:
        return 3
    else:
        raise FinError("Option exercise type not supported.")
    
@njit(fastmath=True, cache=True)
def p_fast(t, T, r_t, delta, pt, ptd, pT, _sigma, _a):
    """ Forward discount factor as seen at some time t which may be in the future for payment at time T where,
    r_t: the delta-period short rate seen at time t
    pt : the discount factor to time t
    ptd : the one period discount factor to time t+dt
    pT : the discount factor from now until the payment of the 1 dollar of the discount factor.
    """

    if abs(_a) < global_vars.g_small * 100:
        _a = global_vars.g_small * 100

    BtT = (1.0 - np.exp(-_a*(T-t)))/_a
    BtDelta = (1.0 - np.exp(-_a * delta))/_a

    term1 = np.log(pT/pt) - (BtT/BtDelta) * np.log(ptd/pt)

    term2 = (_sigma**2)*(1.0-np.exp(-2.0*_a*t)) * BtT * (BtT - BtDelta)/(4.0*_a)

    logAhat = term1 - term2
    BhattT = (BtT/BtDelta) * delta
    p = np.exp(logAhat - BhattT * r_t)
    return p

###############################################################################

@njit(fastmath=True, cache=True)
def build_tree_fast(a, sigma, tree_times, num_time_steps, discount_factors):
    """ Fast tree construction using Numba. """
    tree_maturity = tree_times[-1]
    dt = tree_maturity / (num_time_steps+1)
    dR = sigma * np.sqrt(3.0 * dt)
    j_max = math.ceil(0.1835/(a * dt))
    N = j_max

    pu = np.zeros(shape=2*j_max+1)
    pm = np.zeros(shape=2*j_max+1)
    pd = np.zeros(shape=2*j_max+1)

    # The short rate goes out one step extra to have the final short rate
    r_t = np.zeros(shape=(num_time_steps+2, 2*j_max+1))

    # probabilities star_t at time 0 and go out to one step before T
    # Branching is simple trinomial out to time step m=1 after which
    # the top node and bottom node connect internally to two lower nodes
    # and two upper nodes respectively. The probabilities only depend on j

    for j in range(-j_max, j_max+1):
        ajdt = a * j * dt
        jN = j + N
        if j == j_max:
            pu[jN] = 7.0/6.0 + 0.50*(ajdt*ajdt - 3.0*ajdt)
            pm[jN] = -1.0/3.0 - ajdt*ajdt + 2.0*ajdt
            pd[jN] = 1.0/6.0 + 0.50*(ajdt*ajdt - ajdt)
        elif j == -j_max:
            pu[jN] = 1.0/6.0 + 0.50*(ajdt*ajdt + ajdt)
            pm[jN] = -1.0/3.0 - ajdt*ajdt - 2.0*ajdt
            pd[jN] = 7.0/6.0 + 0.50*(ajdt*ajdt + 3.0*ajdt)
        else:
            pu[jN] = 1.0/6.0 + 0.50*(ajdt*ajdt - ajdt)
            pm[jN] = 2.0/3.0 - ajdt*ajdt
            pd[jN] = 1.0/6.0 + 0.50*(ajdt*ajdt + ajdt)

    # Arrow-Debreu array
    Q = np.zeros(shape=(num_time_steps+2, 2*N+1))

    # This is the drift adjustment to ensure no arbitrage at each time
    alpha = np.zeros(num_time_steps+1)

    # Time zero is trivial for the Arrow-Debreu price
    Q[0, N] = 1.0

    # Big loop over time steps
    for m in range(0, num_time_steps + 1):

        nm = min(m, j_max)
        sum_qz = 0.0
        for j in range(-nm, nm+1):
            rdt = j*dR*dt
            sum_qz += Q[m, j+N] * np.exp(-rdt)
        alpha[m] = np.log(sum_qz/discount_factors[m+1]) / dt

        for j in range(-nm, nm+1):
            jN = j + N
            r_t[m, jN] = alpha[m] + j*dR

        # Loop over all nodes at time m to calculate next values of Q
        for j in range(-nm, nm+1):
            jN = j + N
            rdt = r_t[m, jN] * dt
            z = np.exp(-rdt)

            if j == j_max:
                Q[m+1, jN] += Q[m, jN] * pu[jN] * z
                Q[m+1, jN-1] += Q[m, jN] * pm[jN] * z
                Q[m+1, jN-2] += Q[m, jN] * pd[jN] * z
            elif j == -j_max:
                Q[m+1, jN] += Q[m, jN] * pd[jN] * z
                Q[m+1, jN+1] += Q[m, jN] * pm[jN] * z
                Q[m+1, jN+2] += Q[m, jN] * pu[jN] * z
            else:
                Q[m+1, jN+1] += Q[m, jN] * pu[jN] * z
                Q[m+1, jN] += Q[m, jN] * pm[jN] * z
                Q[m+1, jN-1] += Q[m, jN] * pd[jN] * z

    return (Q, pu, pm, pd, r_t, dt)

###############################################################################

@njit(fastmath=True, cache=True)
def american_bond_option_tree_fast(t_exp,
                                   strike_price,
                                   face_amount,
                                   cpn_times,
                                   cpn_amounts,
                                   exercise_typeInt,
                                   _sigma,
                                   _a,
                                   _Q,
                                   _pu, _pm, _pd,
                                   _r_t,
                                   _dt,
                                   _tree_times,
                                   _df_times, _df_values):
    """ Value an option on a bond with cpns that can have European or
    American exercise. Some minor issues to do with handling cpns on
    the option expiry date need to be solved. """

    DEBUG = False
    if DEBUG:
        print("Entering AmerBondOption")
        print("Coupon Times", cpn_times)
        print("Coupon Amounts", cpn_amounts)

    num_time_steps, num_nodes = _Q.shape
    dt = _dt
    j_max = math.ceil(0.1835/(_a * dt))
    expiry_step = int(t_exp/dt + 0.50)

    ###########################################################################

    # Want to add cpns before expiry to the grid so that we can value
    # their impact on the decision to exercise the option early
    tree_flows = np.zeros(num_time_steps)
    num_cpns = len(cpn_times)

    # Flows that fall on the expiry date included. The tree only goes out to
    # the expiry date so cpns after this date do not go onto the tree.
    for i in range(0, num_cpns):
        t_cpn = cpn_times[i]
        if t_cpn <= t_exp:
            n = int(t_cpn/dt + 0.50)
            ttree = _tree_times[n]
            df_flow = interp._uinterpolate(t_cpn, _df_times, _df_values, INTERP)
            df_tree = interp._uinterpolate(ttree, _df_times, _df_values, INTERP)
            tree_flows[n] += cpn_amounts[i] * 1.0 * df_flow / df_tree

    ###########################################################################
    # Mapped times stores the mapped times and flows and is used to calculate
    # accrued interest in a consistent manner as using actual flows will
    # result in some convergence noise issues as it is inconsistent
    ###########################################################################

    # I star_t the tree with the previous cpn time and amount
    # (does not matter)
    mapped_times = np.zeros(0)   # CHANGE
    mapped_amounts = np.zeros(0)  # CHANGE
    for n in range(0, len(_tree_times)):
        if tree_flows[n] > 0.0:
            mapped_times = np.append(mapped_times, _tree_times[n])
            mapped_amounts = np.append(mapped_amounts, tree_flows[n])

    # Need future cash flows which are exact time and size for accrued at t_exp
    for n in range(0, num_cpns):
        if cpn_times[n] > t_exp:
            mapped_times = np.append(mapped_times, cpn_times[n])
            mapped_amounts = np.append(mapped_amounts, cpn_amounts[n])

    if DEBUG:
        print("MAPPED TIMES", mapped_times)
        print("MAPPED AMOUNTS", mapped_amounts)

    ###########################################################################

    accrued = np.zeros(num_time_steps)
    for m in range(0, expiry_step+1):
        ttree = _tree_times[m]
        accrued[m] = qmath.accrued_interpolator(ttree, cpn_times, cpn_amounts)
        accrued[m] *= face_amount

        # This is a bit of a hack for when the interpolation does not put the
        # full accrued on flow date. Another scheme may work but so does this
        if tree_flows[m] > 0.0:
            accrued[m] = tree_flows[m] * face_amount

    if DEBUG:
        for i in range(0, expiry_step+1):
            print(i, tree_flows[i], accrued[i])

    ###########################################################################

    call_option_values = np.zeros(shape=(num_time_steps, num_nodes))
    put_option_values = np.zeros(shape=(num_time_steps, num_nodes))
    bond_values = np.zeros(shape=(num_time_steps, num_nodes))

    pt_exp = interp._uinterpolate(t_exp, _df_times, _df_values, INTERP)
    ptdelta = interp._uinterpolate(t_exp+dt, _df_times, _df_values, INTERP)

    cpn = 0.0
    zcb = 0.0

    ###########################################################################
    # As the HW model has a closed form solution for the bond price, I use
    # this fact to calculate the bond price at expiry on the tree nodes
    ###########################################################################

    nm = min(expiry_step, j_max)
    for k in range(-nm, nm+1):
        kN = k + j_max
        r_t = _r_t[expiry_step, kN]
        bond_price = 0.0
        for i in range(0, num_cpns):
            tflow = cpn_times[i]
            if tflow >= t_exp:
                ptflow = interp._uinterpolate(tflow, _df_times, _df_values, INTERP)
                zcb = p_fast(t_exp, tflow, r_t, dt, pt_exp, ptdelta, ptflow,
                             _sigma, _a)
                cpn = cpn_amounts[i]
                bond_price += cpn * face_amount * zcb

        bond_price += zcb * face_amount

        # The flow on this date has been added
        bond_values[expiry_step, kN] = bond_price

    # Now consider exercise of the option on the expiry date
    nm = min(expiry_step, j_max)
    for k in range(-nm, nm+1):
        kN = k + j_max
        dirty_price = bond_values[expiry_step, kN]
        clean_price = dirty_price - accrued[expiry_step]
        call_exercise = max(clean_price - strike_price, 0.0)
        put_exercise = max(strike_price - clean_price, 0.0)
        call_option_values[expiry_step, kN] = call_exercise
        put_option_values[expiry_step, kN] = put_exercise

    m = expiry_step

    if DEBUG:
        print("-----------------------------------------")
        print("EXP", _tree_times[m], accrued[m], dirty_price, clean_price,
              call_exercise, put_exercise)

#        print(kN, bond_values[expiry_step, kN], "CLEAN", clean_price)
#        print("EXPIRY DATE", kN, clean_price, accrued[expiry_step], strike_price)

    # Now step back to today considering exercise at expiry and before
    for m in range(expiry_step-1, -1, -1):
        nm = min(m, j_max)
        flow = tree_flows[m] * face_amount

        for k in range(-nm, nm+1):
            kN = k + j_max
            r = _r_t[m, kN]
            df = np.exp(-r*dt)

            pu = _pu[kN]
            pm = _pm[kN]
            pd = _pd[kN]

            if k == j_max:
                vu = bond_values[m+1, kN]
                vm = bond_values[m+1, kN-1]
                vd = bond_values[m+1, kN-2]
                v = (pu*vu + pm*vm + pd*vd) * df
                bond_values[m, kN] = v
            elif k == -j_max:
                vu = bond_values[m+1, kN+2]
                vm = bond_values[m+1, kN+1]
                vd = bond_values[m+1, kN]
                v = (pu*vu + pm*vm + pd*vd) * df
                bond_values[m, kN] = v
            else:
                vu = bond_values[m+1, kN+1]
                vm = bond_values[m+1, kN]
                vd = bond_values[m+1, kN-1]
                v = (pu*vu + pm*vm + pd*vd) * df
                bond_values[m, kN] = v

            bond_values[m, kN] += flow

            vcall = 0.0
            vput = 0.0

            if k == j_max:
                vu = call_option_values[m+1, kN]
                vm = call_option_values[m+1, kN-1]
                vd = call_option_values[m+1, kN-2]
                vcall = (pu*vu + pm*vm + pd*vd) * df
            elif k == -j_max:
                vu = call_option_values[m+1, kN+2]
                vm = call_option_values[m+1, kN+1]
                vd = call_option_values[m+1, kN]
                vcall = (pu*vu + pm*vm + pd*vd) * df
            else:
                vu = call_option_values[m+1, kN+1]
                vm = call_option_values[m+1, kN]
                vd = call_option_values[m+1, kN-1]
                vcall = (pu*vu + pm*vm + pd*vd) * df

            call_option_values[m, kN] = vcall

            if k == j_max:
                vu = put_option_values[m+1, kN]
                vm = put_option_values[m+1, kN-1]
                vd = put_option_values[m+1, kN-2]
                vput = (pu*vu + pm*vm + pd*vd) * df
            elif k == -j_max:
                vu = put_option_values[m+1, kN+2]
                vm = put_option_values[m+1, kN+1]
                vd = put_option_values[m+1, kN]
                vput = (pu*vu + pm*vm + pd*vd) * df
            else:
                vu = put_option_values[m+1, kN+1]
                vm = put_option_values[m+1, kN]
                vd = put_option_values[m+1, kN-1]
                vput = (pu*vu + pm*vm + pd*vd) * df

            put_option_values[m, kN] = vput

            dirty_price = bond_values[m, kN]
            clean_price = dirty_price - accrued[m]
            call_exercise = max(clean_price - strike_price, 0.0)
            put_exercise = max(strike_price - clean_price, 0.0)

            hold_call = call_option_values[m, kN]
            hold_put = put_option_values[m, kN]

            if m == expiry_step:

                call_option_values[m, kN] = max(call_exercise, hold_call)
                put_option_values[m, kN] = max(put_exercise, hold_put)

            elif exercise_typeInt == 3 and m < expiry_step:  # AMERICAN

                call_option_values[m, kN] = max(call_exercise, hold_call)
                put_option_values[m, kN] = max(put_exercise, hold_put)

        if DEBUG:
            print(m, _tree_times[m], accrued[m], dirty_price, clean_price,
                  call_exercise, put_exercise)

    return call_option_values[0, j_max], put_option_values[0, j_max]

###############################################################################

@njit(fastmath=True, cache=True)
def bermudan_swaption_tree_fast(t_exp, t_mat, strike_price, face_amount,
                                cpn_times, cpn_flows,
                                exercise_typeInt,
                                _df_times, _df_values,
                                _tree_times, _Q, _pu, _pm, _pd, _r_t, _dt, _a):
    """ Option to enter into a swap that can be exercised on cpn payment
    dates after the star_t of the exercise period. Due to multiple exercise
    times we need to extend tree out to bond maturity and take into account
    cash flows through time. """

    num_time_steps, num_nodes = _Q.shape
    j_max = math.ceil(0.1835/(_a * _dt))
    expiry_step = int(t_exp/_dt + 0.50)
    maturity_step = int(t_mat/_dt + 0.50)

    ###########################################################################

    fixed_leg_flows = np.zeros(num_time_steps)
    float_leg_values = np.zeros(num_time_steps)
    num_cpns = len(cpn_times)

    # Tree flows go all the way out to the bond maturity date
    for i in range(0, num_cpns):
        t_cpn = cpn_times[i]
        n = int(round(t_cpn/_dt, 0))
        ttree = _tree_times[n]
        df_flow = interp._uinterpolate(t_cpn, _df_times, _df_values, INTERP)
        df_tree = interp._uinterpolate(ttree, _df_times, _df_values, INTERP)
        fixed_leg_flows[n] += cpn_flows[i] * 1.0 * df_flow / df_tree
        float_leg_values[n] = strike_price * df_flow / df_tree

    ###########################################################################
    # Mapped times stores the mapped times and flows and is used to calculate
    # accrued interest in a consistent manner as using actual flows will
    # result in some convergence noise issues as it is inconsistent
    ###########################################################################

    mapped_times = np.array([0.0])
    mapped_amounts = np.array([0.0])

    for n in range(1, len(_tree_times)):

        accd_at_expiry = 0.0
        if _tree_times[n-1] < t_exp and _tree_times[n] >= t_exp:
            mapped_times = np.append(mapped_times, t_exp)
            mapped_amounts = np.append(mapped_amounts, accd_at_expiry)

        if fixed_leg_flows[n] > 0.0:
            mapped_times = np.append(mapped_times, _tree_times[n])
            mapped_amounts = np.append(mapped_amounts, fixed_leg_flows[n])

    ###########################################################################

    accrued = np.zeros(num_time_steps)
    for m in range(0, maturity_step+1):
        ttree = _tree_times[m]
        accrued[m] = qmath.accrued_interpolator(ttree, mapped_times, mapped_amounts)
        accrued[m] *= face_amount

        # This is a bit of a hack for when the interpolation does not put the
        # full accrued on flow date. Another scheme may work but so does this
        if fixed_leg_flows[m] > global_vars.g_small:
            accrued[m] = fixed_leg_flows[m] * face_amount

    ###########################################################################

    # The value of the swap at each time and node. Principal is exchanged.
    fixed_leg_values = np.zeros(shape=(num_time_steps, num_nodes))
    # The value of the option to enter into a payer swap
    pay_values = np.zeros(shape=(num_time_steps, num_nodes))
    # The value of the option to enter into a receiver swap
    rec_values = np.zeros(shape=(num_time_steps, num_nodes))

    # Star_t with the value of the bond at maturity
    for k in range(0, num_nodes):
        flow = 1.0 + fixed_leg_flows[maturity_step]
        fixed_leg_values[maturity_step, k] = flow * face_amount

    N = j_max

    # Now step back to today considering early exercise
    for m in range(maturity_step-1, -1, -1):
        nm = min(m, j_max)
        flow = fixed_leg_flows[m] * face_amount

        for k in range(-nm, nm+1):
            kN = k + N
            r_t = _r_t[m, kN]
            df = np.exp(-r_t * _dt)
            pu = _pu[kN]
            pm = _pm[kN]
            pd = _pd[kN]

            if k == j_max:
                vu = fixed_leg_values[m+1, kN]
                vm = fixed_leg_values[m+1, kN-1]
                vd = fixed_leg_values[m+1, kN-2]
                v = (pu*vu + pm*vm + pd*vd) * df
                fixed_leg_values[m, kN] = v
            elif k == -j_max:
                vu = fixed_leg_values[m+1, kN+2]
                vm = fixed_leg_values[m+1, kN+1]
                vd = fixed_leg_values[m+1, kN]
                v = (pu*vu + pm*vm + pd*vd) * df
                fixed_leg_values[m, kN] = v
            else:
                vu = fixed_leg_values[m+1, kN+1]
                vm = fixed_leg_values[m+1, kN]
                vd = fixed_leg_values[m+1, kN-1]
                v = (pu*vu + pm*vm + pd*vd) * df
                fixed_leg_values[m, kN] = v

            fixed_leg_values[m, kN] += flow
            vpay = 0.0
            vrec = 0.0

            if k == j_max:
                vu = pay_values[m+1, kN]
                vm = pay_values[m+1, kN-1]
                vd = pay_values[m+1, kN-2]
                vpay = (pu*vu + pm*vm + pd*vd) * df
            elif k == -j_max:
                vu = pay_values[m+1, kN+2]
                vm = pay_values[m+1, kN+1]
                vd = pay_values[m+1, kN]
                vpay = (pu*vu + pm*vm + pd*vd) * df
            else:
                vu = pay_values[m+1, kN+1]
                vm = pay_values[m+1, kN]
                vd = pay_values[m+1, kN-1]
                vpay = (pu*vu + pm*vm + pd*vd) * df

            pay_values[m, kN] = vpay

            if k == j_max:
                vu = rec_values[m+1, kN]
                vm = rec_values[m+1, kN-1]
                vd = rec_values[m+1, kN-2]
                vrec = (pu*vu + pm*vm + pd*vd) * df
            elif k == -j_max:
                vu = rec_values[m+1, kN+2]
                vm = rec_values[m+1, kN+1]
                vd = rec_values[m+1, kN]
                vrec = (pu*vu + pm*vm + pd*vd) * df
            else:
                vu = rec_values[m+1, kN+1]
                vm = rec_values[m+1, kN]
                vd = rec_values[m+1, kN-1]
                vrec = (pu*vu + pm*vm + pd*vd) * df

            rec_values[m, kN] = vrec

            hold_pay = pay_values[m, kN]
            hold_rec = rec_values[m, kN]

            # The floating value is clean and so must be the fixed value
            fixed_leg_value = fixed_leg_values[m, kN] - accrued[m]
            float_leg_value = float_leg_values[m]

            pay_exercise = max(float_leg_value - fixed_leg_value, 0.0)
            rec_exercise = max(fixed_leg_value - float_leg_value, 0.0)

            if m == expiry_step:

                pay_values[m, kN] = max(pay_exercise, hold_pay)
                rec_values[m, kN] = max(rec_exercise, hold_rec)

            elif exercise_typeInt == 2 and flow > global_vars.g_small and m >= expiry_step:

                pay_values[m, kN] = max(pay_exercise, hold_pay)
                rec_values[m, kN] = max(rec_exercise, hold_rec)

            elif exercise_typeInt == 3 and m >= expiry_step:

                pay_values[m, kN] = max(pay_exercise, hold_pay)
                rec_values[m, kN] = max(rec_exercise, hold_rec)

                # Need to define floating value on all grid dates

                raise FinError("American optionality not tested.")

    return pay_values[0, j_max], rec_values[0, j_max]

###############################################################################

@njit(fastmath=True, cache=True)
def callable_puttable_bond_tree_fast(cpn_times, cpn_flows,
                                     call_times, call_prices,
                                     put_times, put_prices, face,
                                     _sigma, _a, _Q,  # IS SIGMA USED ?
                                     _pu, _pm, _pd, _r_t, _dt, _tree_times,
                                     _df_times, _df_values):
    """ Value an option on a bond with cpns that can have European or
    American exercise. Some minor issues to do with handling cpns on
    the option expiry date need to be solved. """

#    print("Coupon Times:", cpn_times)
#    print("Coupon Flows:", cpn_flows)

#    print("DF Times:", _df_times)
#    print("DF Values:", _df_values)

    if np.any(cpn_times < 0.0):
        raise FinError("No cpn times can be before the value date.")

    num_time_steps, num_nodes = _Q.shape
    dt = _dt
    j_max = math.ceil(0.1835/(_a * dt))
    t_mat = cpn_times[-1]
    maturity_step = int(t_mat/dt + 0.50)

    ###########################################################################
    # Map cpns onto tree while preserving their present value
    ###########################################################################

    tree_flows = np.zeros(num_time_steps)

    num_cpns = len(cpn_times)
    for i in range(0, num_cpns):
        t_cpn = cpn_times[i]
        n = int(round(t_cpn/dt, 0))
        ttree = _tree_times[n]
        df_flow = interp._uinterpolate(t_cpn, _df_times, _df_values, INTERP)
        df_tree = interp._uinterpolate(ttree, _df_times, _df_values, INTERP)
        tree_flows[n] += cpn_flows[i] * 1.0 * df_flow / df_tree

#    print("Tree flows:", tree_flows)

    ###########################################################################
    # Mapped times stores the mapped times and flows and is used to calculate
    # accrued interest in a consistent manner as using actual flows will
    # result in some convergence noise issues as it is inconsistent
    ###########################################################################

    mapped_times = np.array([0.0])
    mapped_amounts = np.array([0.0])

    for n in range(1, len(_tree_times)):
        if tree_flows[n] > 0.0:
            mapped_times = np.append(mapped_times, _tree_times[n])
            mapped_amounts = np.append(mapped_amounts, tree_flows[n])

    accrued = np.zeros(num_time_steps)
    for m in range(0, num_time_steps):
        ttree = _tree_times[m]
        accrued[m] = qmath.accrued_interpolator(ttree, mapped_times, mapped_amounts)
        accrued[m] *= face

        # This is a bit of a hack for when the interpolation does not put the
        # full accrued on flow date. Another scheme may work but so does this
        if tree_flows[m] > 0.0:
            accrued[m] = tree_flows[m] * face

    ###########################################################################
    # map call onto tree - must have no calls at high value
    ###########################################################################

    tree_call_value = np.ones(num_time_steps) * face * 1000.0
    num_calls = len(call_times)
    for i in range(0, num_calls):
        call_time = call_times[i]
        n = int(round(call_time/dt, 0))
        tree_call_value[n] = call_prices[i]

    # map puts onto tree
    tree_put_value = np.zeros(num_time_steps)
    num_puts = len(put_times)
    for i in range(0, num_puts):
        put_time = put_times[i]
        n = int(round(put_time/dt, 0))
        tree_put_value[n] = put_prices[i]

    ###########################################################################
    # Value the bond by backward induction star_ting at bond maturity
    ###########################################################################

    call_put_bond_values = np.zeros(shape=(num_time_steps, num_nodes))
    bond_values = np.zeros(shape=(num_time_steps, num_nodes))

    DEBUG = True
    if DEBUG:
        df = 1.0
        px = 0.0
        for i in range(0, maturity_step+1):
            flow = tree_flows[i]
            t = _tree_times[i]
            df = interp._uinterpolate(t, _df_times, _df_values, INTERP)

            if flow > global_vars.g_small:
                pv = flow * df
                px += pv

        px += df

    ###########################################################################
    # Now step back to today considering early exercise
    ###########################################################################

    m = maturity_step
    nm = min(maturity_step, j_max)
    vcall = tree_call_value[m]
    vput = tree_put_value[m]
    vhold = (1.0 + tree_flows[m]) * face
    vclean = vhold - accrued[m]
    value = min(max(vclean, vput), vcall) + accrued[m]

    for k in range(-nm, nm+1):
        kN = k + j_max
        bond_values[m, kN] = (1.0 + tree_flows[m]) * face
        call_put_bond_values[m, kN] = value

    # Now step back to today considering early put and call
    for m in range(maturity_step-1, -1, -1):
        nm = min(m, j_max)
        flow = tree_flows[m] * face
        vcall = tree_call_value[m]
        vput = tree_put_value[m]

        for k in range(-nm, nm+1):
            kN = k + j_max
            r_t = _r_t[m, kN]
            df = np.exp(-r_t*dt)
            pu = _pu[kN]
            pm = _pm[kN]
            pd = _pd[kN]

            if k == j_max:
                vu = bond_values[m+1, kN]
                vm = bond_values[m+1, kN-1]
                vd = bond_values[m+1, kN-2]
            elif k == -j_max:
                vu = bond_values[m+1, kN+2]
                vm = bond_values[m+1, kN+1]
                vd = bond_values[m+1, kN]
            else:
                vu = bond_values[m+1, kN+1]
                vm = bond_values[m+1, kN]
                vd = bond_values[m+1, kN-1]

            v = (pu*vu + pm*vm + pd*vd) * df
            bond_values[m, kN] = v
            bond_values[m, kN] += flow

            if k == j_max:
                vu = call_put_bond_values[m+1, kN]
                vm = call_put_bond_values[m+1, kN-1]
                vd = call_put_bond_values[m+1, kN-2]
            elif k == -j_max:
                vu = call_put_bond_values[m+1, kN+2]
                vm = call_put_bond_values[m+1, kN+1]
                vd = call_put_bond_values[m+1, kN]
            else:
                vu = call_put_bond_values[m+1, kN+1]
                vm = call_put_bond_values[m+1, kN]
                vd = call_put_bond_values[m+1, kN-1]

            vhold = (pu*vu + pm*vm + pd*vd) * df
            # Need to make add on cpns paid if we hold
            vhold = vhold + flow
            value = min(max(vhold - accrued[m], vput), vcall) + accrued[m]
            call_put_bond_values[m, kN] = value

    return {'bondwithoption': call_put_bond_values[0, j_max],
            'bondpure': bond_values[0, j_max]}

###############################################################################

def fwd_dirty_bond_price(r_t, *args):
    """ Price a cpn bearing bond on the option expiry date and return
    the difference from a strike price. This is used in a root search to
    find the future expiry time short rate that makes the bond price equal
    to the option strike price. It is a key step in the Jamshidian bond
    decomposition approach. The strike is a clean price. """

    self = args[0]
    t_exp = args[1]
    cpn_times = args[2]
    cpn_amounts = args[3]
    df_times = args[4]
    df_values = args[5]
    strike_price = args[6]
    face = args[7]

    dt = 0.001
    tdelta = t_exp + dt
    pt_exp = interp._uinterpolate(t_exp, df_times, df_values, INTERP)
    ptdelta = interp._uinterpolate(tdelta, df_times, df_values, INTERP)

#    print("TEXP", t_exp, pt_exp)

    num_flows = len(cpn_times)
    pv = 0.0

    for i in range(1, num_flows):

        t_cpn = cpn_times[i]
        cpn = cpn_amounts[i]

        if t_cpn > t_exp:
            pt_cpn = interp._uinterpolate(t_cpn, df_times, df_values, INTERP)
            zcb = p_fast(t_exp, t_cpn, r_t, dt, pt_exp, ptdelta, pt_cpn,
                         self.sigma, self.a)
            pv = pv + zcb * cpn
#            print("TCPN", t_cpn, "ZCB", zcb, "CPN", cpn, "PV", pv)

    if t_cpn >= t_exp:
        pv = pv + zcb

#    print("TCPN", t_cpn, "ZCB", zcb, "PRI", 1.0, "PV", pv)

    accd = qmath.accrued_interpolator(t_exp, cpn_times, cpn_amounts)
#    print("Accrued:", accd)
#    print("t_exp:", t_exp)
#    print("cpn_times:", cpn_times)
#    print("cpn_amounts:", cpn_amounts)

    pv_clean = pv - accd
    obj = face * pv_clean - strike_price

#    print("FWD PRICE", r_t, pv, accd, strike_price, obj)
    return obj

###############################################################################


class HWTree():
    def __init__(self, sigma, a, num_time_steps=100, european_calc_type=HWEuropeanCalcType.EXPIRY_TREE):
        """ Constructs the Hull-White rate model. The speed of mean reversion
        a and volatility are passed in. The short rate process is given by
        dr = (theta(t) - ar) * dt  + sigma * dW. The model will switch to use
        Jamshidian's approach where possible unless the useJamshidian flag is
        set to false in which case it uses the trinomial Tree. """

        if sigma < 0.0:
            raise FinError("Sigma must be positive.")
        
        if a < 0.0:
            raise FinError("Mean reversion must be positive.")

        self.sigma = sigma
        self.a = a
        self.num_time_steps = num_time_steps
        self.european_calc_type = european_calc_type

        self.Q = None
        self.r = None
        self.tree_times = None
        self.pu = None
        self.pm = None
        self.pd = None
        self.discount_curve = None
        self.tree_built = False
        self.df_times = None
        self.dfs = None
        self.r_t = None
        self.dt = None

    def option_on_zcb(self, t_exp, t_mat, strike, face_amount, df_times, df_values):
        """ Price an option on a zero cpn bond using analytical solution of
        Hull-White model. User provides bond face and option strike and expiry
        date and maturity date. """

        if t_exp >= t_mat:
            raise FinError("Expiry date must be before maturity date.")
