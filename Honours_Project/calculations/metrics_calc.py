import pandas as pd
from datetime import datetime, timedelta
from vix_calc_functions import volatility_methods
import vix_calc_class as vix_calc
import sqlite3, math, random

def calc_accuracy(df, real_col='change_ytd', vix_t='vix_t') -> (int, int):
    """"""
    bounded = df[real_col] <=df[vix_t]
    vals = dict(bounded.value_counts())
    within = vals.get(True, 0)
    exceeded = vals.get(False, 0)
    # exceeded = bounded.value_counts().loc[False]

    return within, exceeded


def calc_auc_aoc(df, curveA='change_ytd', curveB='vix_t'):
    """This function will calculate select areas between two curve.
        Returning both the area found under curve B between curve A
        and the area curve B occupies over curve A.
        The two can be summed to get the overall area between the curves
    """

    total_auc = (df[curveB] - df[curveA]).loc[lambda x: x>0].sum()
    total_aoc = (df[curveB] - df[curveA]).loc[lambda x: x<0].sum()
    return total_auc, total_aoc


def query_spy(vix_method, DT):
    """This function will calculate the vix for a particular date,
        and return a dataframe of the data with a few added columns.
    """
    conn = sqlite3.connect("../data_aggregation/flow_database.db")
    conn.row_factory = vix_method.my_row_factory
    cursor = conn.cursor()

    d = datetime.strptime(DT, '%Y-%m-%d')
    for_dt = (d + timedelta(days=365)).strftime('%Y-%m-%d')
    query = f"""
    select
        open,
        close,
        date_of,
        date_of_close
    from price_data

    where symbol = 'SPY'
    and date_of_close >= '{DT}'
    and date_of_close <= '{for_dt}'
    ;
    """

    cursor.execute(query)
    data = cursor.fetchall()
    data = pd.DataFrame.from_records(data)

    conn.close()
    
    data['date_of_close'] = data.date_of_close.apply(pd.to_datetime)
    data['annual_'] = (data.date_of_close - d).dt.days / 365
    
    return data

def get_period_volatility(VIX, period):
    """Calculates the expected implied volatility for given time period.
        period must be a decimal between 0 and 1 representing a fraction of a year.
        VIX must be the VIX.
    """
    try:
        return VIX/(math.sqrt(1/period))
    except:
        return 0

def observe_vix_acc(DT, vix_method: volatility_methods):
    """This function will calculate thee """
    # VIX = vix_calc.main(DT)
    
    VIX = vix_method.calc_volatility(DT)
    data = query_spy(vix_method, DT)
    start_close = data.iloc[0].close
    
    data['vix_t'] = data.annual_.apply(lambda x: get_period_volatility(VIX, x))
    
    data['price_up'] = (data.vix_t / 100 + 1) * start_close
    data['price_down'] = (-data.vix_t / 100 + 1) * start_close
    data['change_ytd'] = abs(data.close / start_close - 1) * 100
    return (data, VIX)

def sample_random_dates(n: int):
    """This function will return a list of n random dates between 2015 and 2022"""
    start = "2015-01-09"
    startdt = datetime.strptime(start, '%Y-%m-%d')
    total_dates = 390
    
    print()

    random_dates = [(startdt + timedelta(weeks=random.randint(0,total_dates))).strftime('%Y-%m-%d') for _ in range(n)]

    return random_dates


class aggregate_metrics:
    def agg_metrics(df):
        within, exceeded = calc_accuracy(df)
        accuracy = round(within/(within+exceeded), 4)
        
        stddev = df.close.std()
        auc, aoc = calc_auc_aoc(df)
        yearopen = df.iloc[0].close
        yearclose = df.iloc[-1].close
        vixtotal = df.vix_t.sum()
        return {"accuracy": accuracy, "stddev":stddev, "auc":auc, "aoc":aoc, "yearopen": yearopen,"yearclose":yearclose, "vixtotal":vixtotal}

    def curve_areas(mm, verbose=False):
        mm['abc'] = mm.auc + mm.aoc
        mm['rd'] = mm.abc / mm.vixtotal
        
        if verbose:
            print(f"Mean Area Under Curve: {mm.auc.mean()}")
            print(f"Mean Area Over Curve: {mm.aoc.mean()}")
            print(f"Mean Area Between Curves: {(mm.abc).mean()}")
            print(f'Ratio : {mm.rd.mean()}')
