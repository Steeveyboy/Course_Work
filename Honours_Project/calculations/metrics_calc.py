import pandas as pd
from datetime import datetime, timedelta
import vix_calc
import sqlite3

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


def query_spy(DT):
    """This function will calculate the vix for a particular date,
        and return a dataframe of the data with a few added columns.
    """
    conn = sqlite3.connect("../data_aggregation/flow_database.db")
    conn.row_factory = vix_calc.my_row_factory
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
    cursor.close()
    conn.close()
    data = pd.DataFrame.from_records(data)
    
    data['date_of_close'] = data.date_of_close.apply(pd.to_datetime)
    data['annual_'] = (data.date_of_close - d).dt.days / 365
    
    return data

def observe_vix_acc(DT, vix_formula=vix_calc.main):
    """This function will calculate thee """
    # VIX = vix_calc.main(DT)
    VIX = vix_formula(DT)
    data = query_spy(DT)
    start_close = data.iloc[0].close
    
    data['vix_t'] = data.annual_.apply(lambda x: vix_calc.get_period_volatility(VIX, x))
    
    data['price_up'] = (data.vix_t / 100 + 1) * start_close
    data['price_down'] = (-data.vix_t / 100 + 1) * start_close
    data['change_ytd'] = abs(data.close / start_close - 1) * 100
    return (data, VIX)
