import sqlite3
import math, datetime, sys, time
from itertools import groupby
from scipy.interpolate import CubicSpline
# import vix_calc_functions as vix_funcs
from vix_calc_functions import *


def get_intrisic_price(data):
    if data['contract_type'] == 'call':
        return data["stock_price"] - data["strike"]
    else:
        return data["strike"] - data["stock_price"]
    
def calc_uncertain_all(data):
    for i in range(len(data)):
        data[i]['uncert'] = data[i]['midpoint'] - get_intrisic_price(data[i])
    return data
    

def calc_all_contributions(calls, puts, T, rfr, F, cont_func=calc_contributions):
    """Calculating the individual contribution of each option returning a list"""
    ls = []
    Call_first = calls[0]
    Puts_first = puts[0]
    # K_zero = calls[0]['strike']
    # constraint = (1/T)*((F/K_zero - 1) ** 2)

    ls.extend(cont_func(calls, Puts_first, T, rfr))
    ls.extend(cont_func(puts, Call_first, T, rfr))

    # all_contributions = sum(ls)
    # variance = (2/T) * all_contributions - constraint 
    
    # return variance

    return ls


def transform_to_variance(contributions, K_zero, T, rfr, F):
    
    constraint = (1/T)*((F/K_zero - 1) ** 2)
    
    all_contributions = sum(contributions)
    variance = (2/T) * all_contributions - constraint
    return variance

def select_options(data, moneyness=out_of_money):
    
    calls = filter(lambda x: x['contract_type']=='call', data)
    puts = filter(lambda x: x['contract_type']=='put', data)
    
    calls = filter(moneyness, calls)
    puts = filter(moneyness, puts)
    
    calls = sorted(calls, key=lambda x: abs(x['strike'] - x['stock_price']))
    puts = sorted(puts, key=lambda x: abs(x['strike'] - x['stock_price']))
    
    calls2 = filter_serious(calls)
    puts2 = filter_serious(puts)
    
    return calls2, puts2

def main(DT):
    
    data = query_date(DT)
    
    if len(data) == 0:
        return None
    
    g = groupby(sorted(data, key=lambda x: x['exp_date']), key=lambda x: x['exp_date'])
    contributions_ls = []
    key_vars = []
    for exp_dt, opt_dat in g:
        options_data = list(opt_dat)
        calls, puts = select_options(options_data, moneyness=out_of_money)
        calls_in, puts_in = select_options(options_data, moneyness=in_the_money)

        calls_in = calc_uncertain_all(calls_in)
        puts_in = calc_uncertain_all(puts_in)
        
        T = calc_T(DT, exp_dt)
        
        rfr = get_rfr(DT, T)
        if not rfr:
            return
        
        F = calc_forward(calls, puts, rfr, T)
        
        K_zero = calls[0]['strike']
        
        key_vars.append({'T': T, 'rfr': rfr, 'F':F, 'N': (T*525600)})
        out_contributions = calc_all_contributions(calls, puts, T, rfr, F)
        in_contributions = calc_all_contributions(calls_in, puts_in, T, rfr, F, cont_func=calc_contributions_itm)
        # in_contributions = []
        print(sum(in_contributions), sum(out_contributions))
        variance_all = transform_to_variance(out_contributions+in_contributions, K_zero, T, rfr, F)
        
        contributions_ls.append(variance_all)
        
    time_diff1 = (abs(key_vars[1]['N'] - 43200)/(key_vars[1]['N'] - key_vars[0]['N']))
    time_diff2 = (abs(key_vars[0]['N'] - 43200)/(key_vars[1]['N'] - key_vars[0]['N']))
    
    VIX = 100 * math.sqrt( ((key_vars[0]['T'] * contributions_ls[0] * time_diff1) + (key_vars[1]['T'] * contributions_ls[1]*time_diff2)) * (525600/43200) )
    return VIX
    
if __name__ == '__main__':
    DT = '2023-03-17'
    if len(sys.argv) > 1:
        DT = sys.argv[1]
    print(f'calculating VIX for {DT}')
    starttime = time.time()
    VIX = main(DT)
    print(VIX)
    print(f'Finished in {time.time() - starttime} seconds')
