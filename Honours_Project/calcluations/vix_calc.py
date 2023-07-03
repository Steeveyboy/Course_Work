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
            and obs_date = {dt}
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
    dd = filter(out_of_money, data)

    calls = filter(lambda x: x['contract_type']=='call', dd)
    puts = filter(lambda x: x['contract_type']=='put', dd)

    calls = sorted(calls, key=lambda x: abs(x['strike'] - x['stock_price']))
    puts = sorted(puts, key=lambda x: abs(x['strike'] - x['stock_price']))

    calls2 = filter_serious(calls)
    puts2 = filter_serious(puts)
    
    return calls2, puts2

def calc_contributions(calls, puts, T, rfr, F):
    """Calculating the individual contribution of each option returning a list"""
    pass

if __name__ == '__main__':
    DT = '2023-05-12'
    data = query_date(DT)

    g = groupby(sorted(data, lambda x: x['exp_date']), key=lambda x: x['exp_date'])

    contributions_ls = []
    for exp_dt, opt_dat in g:
        calls, puts = select_options(data)
        T = calc_T(DT, exp_dt)
        rfr = get_rfr(DT, T)
        F = calc_forward(calls, puts, rfr, T)

        contributions_ls.append(calc_contributions(calls, puts, T, rfr, F))




    
    # TNear = 
    # TNext = 
    # rfr = get_rfr(date, TNear)
    # rfr = get_rfr(date, TNext)
    # FNear = calc_forward(calls2, puts2, rtr, TNear)
    # FNext = calc_forward(calls2, puts2, rtr, TNear)

    
    