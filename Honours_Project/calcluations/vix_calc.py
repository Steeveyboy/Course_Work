import sqlite3
import math, datetime
from itertools import groupby
from scipy.interpolate import CubicSpline

PERIODS = {'1mo': 30/365, '2mo': 60/365, '3mo':91/365, '4mo':121/365, '6mo':182/365, '1yr':1, '2yr':2, '3yr':3, '5yr':5, '7yr':7, '10yr':10, '20yr':20, '30yr':30}

def out_of_money(x):
    if x['contract_type'] == 'call':
        if(x['strike'] >= x['stock_price']):
            return True
    else:
        if(x['strike'] <= x['stock_price']):
            return True
    return False

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



def my_row_factory(cur, row):
    d={}
    for idx, col in enumerate(cur.description):
        d[col[0].lower()] = row[idx]
    return d

NEWQUERY = """
with temptable as (
SELECT
	*
FROM contract_data
WHERE 
	contract_data.symbol ='SPY'
    and obs_date = {dt})
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
    conn = sqlite3.connect("../data_aggregation/options_database.db")
    conn.row_factory = my_row_factory
    cursor = conn.cursor()

    query = f"""
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
# '2023-05-12'
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
    x = [PERIODS[i] for i in list(rates.keys())[1:]]
    y = [j for j in list(rates.values())[1:]]
    
    cs = CubicSpline(x, y)
    
    return cs(T)


def calc_forward(calls, puts, rtr, T):
    """Calcluating the forward rate of option"""
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
    return (strike_int / option['strike']**2)*math.e**(rfr*T)*option['midpoint']

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

    all_constributions = sum(ls)

    variance = (1/T) * all_constributions - constraint 
    
    return variance

if __name__ == '__main__':
    DT = '2023-05-12'
    data = query_date(DT)
    print(len(data))
    g = groupby(sorted(data, key=lambda x: x['exp_date']), key=lambda x: x['exp_date'])

    contributions_ls = []
    for exp_dt, opt_dat in g:
        print(exp_dt)
        calls, puts = select_options(list(opt_dat))
        print(len(calls), len(puts))
        T = calc_T(DT, exp_dt)
        rfr = get_rfr(DT, T)
        F = calc_forward(calls, puts, rfr, T)

        contributions_ls.append(calc_all_contributions(calls, puts, T, rfr, F))

    print(contributions_ls)
    
    


    
    # TNear = 
    # TNext = 
    # rfr = get_rfr(date, TNear)
    # rfr = get_rfr(date, TNext)
    # FNear = calc_forward(calls2, puts2, rtr, TNear)
    # FNext = calc_forward(calls2, puts2, rtr, TNear)

    
    