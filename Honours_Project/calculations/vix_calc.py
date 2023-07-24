import sqlite3
import math, datetime, sys, time
from itertools import groupby
from scipy.interpolate import CubicSpline

PERIODS = {'1mo': 30/365, '2mo': 60/365, '3mo':91/365, '4mo':121/365, '6mo':182/365, '1yr':1, '2yr':2, '3yr':3, '5yr':5, '7yr':7, '10yr':10, '20yr':20, '30yr':30}

def out_of_money(x):
    if x['contract_type'] == 'call':
        if(x['strike'] >= x['stock_price']):
            return True
    else:
        if(x['strike'] <= (x['stock_price'])):
            return True
    return False

def get_period_volatility(VIX, period):
    """Calculates the expected implied volatility for given time period.
        period must be a decimal between 0 and 1 representing a fraction of a year.
        VIX must be the VIX.
    """
    try:
        return VIX/(math.sqrt(1/period))
    except:
        return 0

def check_serious(bid, ask):
    return (bid > 0 and ask > 0)

def filter_serious(ls):
    ## Takes in a list of options sorted by ascending difference between strike and stock_price.
    new_ls = []
    prev_serious = True
    for opt in ls:
        if check_serious(opt['bid'], opt['ask']):
            new_ls.append(opt)
            prev_serious = True
        else:
            if not prev_serious:
                break
            prev_serious = False
    return new_ls

def test_auto():
    return "TEST WOR2342342KED"

def my_row_factory(cur, row):
    d={}
    for idx, col in enumerate(cur.description):
        d[col[0].lower()] = row[idx]
    return d


orig_query = """
select 
    contract_data.*,
    price_data.close as stock_price
from contract_data
join price_data
on (price_data.Symbol = contract_data.Symbol) and (price_data.date_of_close = contract_data.obs_date)
    where
        contract_data.symbol ='SPY'
        and obs_date = '{dt}'
;
"""


query_old = """
with temptable as (
SELECT
    *
FROM contract_data
WHERE 
    contract_data.symbol ='SPY'
    and obs_date = '{dt}')
select 
    temptable.*,
    price_data.close as stock_price
from temptable
join price_data
    on (price_data.Symbol = temptable.Symbol) and (price_data.date_of_close = temptable.Obs_Date)
    where
        (Exp_Date = (select min(Exp_Date) from temptable)) or Exp_Date = (select max(Exp_Date) from temptable)
;
"""

def query_date(dt):
    conn = sqlite3.connect("../data_aggregation/flow_database.db")
    conn.row_factory = my_row_factory
    cursor = conn.cursor()
    
    query = f"""
    with temptable as (
    SELECT
        symbol,
        Contract_Type,
        Strike,
        Bid,
        Midpoint,
        Ask,
        Obs_Date,
        Exp_Date
    FROM contract_data
    WHERE 
        contract_data.symbol ='SPY'
        and obs_date = '{dt}')
    select 
        temptable.symbol,
        temptable.Contract_Type,
        temptable.Strike,
        temptable.bid,
        temptable.Midpoint,
        temptable.ask,
        temptable.Obs_Date,
        temptable.Exp_Date,
        price_data.close as stock_price
    from temptable
    join price_data
        on (price_data.Symbol = temptable.Symbol) and (price_data.date_of_close = temptable.Obs_Date)
        where
            (Exp_Date = (select min(Exp_Date) from temptable)) or Exp_Date = (select max(Exp_Date) from temptable)
    ;
    """

    cursor.execute(query)
    data = cursor.fetchall()
    return data

def query_treasury_rates(dt):
    conn = sqlite3.connect("../data_aggregation/options_database.db")
    conn.row_factory = my_row_factory
    cursor = conn.cursor()
    
    QUERY = f"""
    Select 
        *
    from treasury_rates
    where date_of = '{dt}'
    """
    cursor.execute(QUERY)
    data = cursor.fetchone()
    return data

def get_rfr(dt, T):
    """
    This function will calculate the risk free rate over a specified time (T in years) for a specified date (dt)
    """
    rates = query_treasury_rates(dt)
    if not rates:
        return
    # print(rates)
    x = [PERIODS[i] for i,j in list(rates.items())[1:] if j is not None]
    y = [j for j in list(rates.values())[1:]  if j is not None]
    # print(x)
    # print(y)
    cs = CubicSpline(x, y)
    
    return cs(T) / 100


def calc_forward(calls, puts, rtr, T):
    """Calcluating the forward rate of option"""
    # print(calls[0], '\n', puts[0])
    F = calls[0]['strike'] + ((math.e ** (rtr*T)) * (calls[0]['midpoint'] - puts[0]['midpoint']))
    return F

def calc_T(date, exp_date):
    """Calcluating the time to expiration in years"""
    return (datetime.datetime.strptime(exp_date, '%Y-%m-%d') - datetime.datetime.strptime(date, '%Y-%m-%d')).days / 365

def select_options(data):
    """Select valid options from input data"""
    calls = filter(lambda x: x['contract_type']=='call', data)
    puts = filter(lambda x: x['contract_type']=='put', data)
    
    calls = filter(out_of_money, calls)
    puts = filter(out_of_money, puts)

    calls = sorted(calls, key=lambda x: abs(x['strike'] - x['stock_price']))
    puts = sorted(puts, key=lambda x: abs(x['strike'] - x['stock_price']))

    calls2 = filter_serious(calls)
    puts2 = filter_serious(puts)
    
    return calls2, puts2

def strike_interval(option1, option2):
    """Calculates the interval between two strike prices"""
    return abs(option1['strike'] - option2['strike']) / 2

def calc_inv_contribution(option, strike_int, rfr, T):
    # print(rfr, T, math.e**(rfr*T))
    return (strike_int / (option['strike']**2))*(math.e**(rfr*T))*option['midpoint']

def calc_contributions(options, option_first, T, rfr):
    ls = []

    first_cont = calc_inv_contribution(options[0], strike_interval(option_first, options[1]), rfr, T)
    # first_contribution = strike_interval(option_first, options[1]) / (options[0]['strike']**2) * math.e**(rfr*T)*options[0] - constraint
    ls.append(first_cont)

    for i in range(1, len(options)-1):
        ls.append(calc_inv_contribution(options[i], strike_interval(options[i-1], options[i+1]), rfr, T))
    
    return ls

def calc_all_contributions(calls, puts, T, rfr, F):
    """Calculating the individual contribution of each option returning a list"""
    ls = []
    Call_first = calls[0]
    Puts_first = puts[0]
    K_zero = calls[0]['strike']
    constraint = (1/T)*((F/K_zero - 1) ** 2)

    ls.extend(calc_contributions(calls, Puts_first, T, rfr))
    ls.extend(calc_contributions(puts, Call_first, T, rfr))

    all_contributions = sum(ls)
    # print("contributions:", all_contributions, "CONSTRAINT:", constraint, f"F {F}    K_Zero {K_zero}   T {T}")
    variance = (2/T) * all_contributions - constraint 
    
    return variance


def main(DT):
    print(f'calculating VIX for {DT}')
    data = query_date(DT)
    # print(len(data))
    
    if len(data) == 0:
        return None
    
    g = groupby(sorted(data, key=lambda x: x['exp_date']), key=lambda x: x['exp_date'])
    contributions_ls = []
    key_vars = []
    for exp_dt, opt_dat in g:
        print(exp_dt)
        calls, puts = select_options(list(opt_dat))
        # print(len(calls), len(puts))
        T = calc_T(DT, exp_dt)
        
        rfr = get_rfr(DT, T)
        if not rfr:
            return
        
        F = calc_forward(calls, puts, rfr, T)
        
        # F = 0.00
        # print(F, "FFFFF")
        key_vars.append({'T': T, 'rfr': rfr, 'F':F, 'N': (T*525600)})
        contributions_ls.append(calc_all_contributions(calls, puts, T, rfr, F))

    # print(contributions_ls)
    # print(key_vars)
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


