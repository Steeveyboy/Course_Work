from requests_html import HTMLSession
from datetime import datetime, timedelta
from time import time
# from option_webscraper import insertData
import sqlite3
import sys


conn = sqlite3.connect("options_database.db")


START_DATE = datetime.strptime('2020-01-03', '%Y-%m-%d').date()
NEAR_TERM = 23
NEXT_TERM = 37
CURR_DATE = datetime.today().date()

token = open('tokens.txt', 'r').read()

link = "https://api.marketdata.app/v1/options/chain/{ticker}/?token={token}&date={obs_date}&from={from_date}&to={to_date}"

def fetch_data(ticker, obs_date, s):
    starttime = time()
    ## TODO create request to server for data
    print(f"fetching data for {obs_date}", end = '\t')
    near_date = obs_date + timedelta(days=NEAR_TERM)
    next_date = obs_date + timedelta(days=NEXT_TERM)
    res = s.get(link.format(ticker=ticker, token=token, obs_date=obs_date, from_date=near_date, to_date=next_date))

    if res.ok:
        insert_all_data(res.json())
    print(f"Total Time: {time()-starttime}")
    return
    
def format_data_tuple(data):
    ## TODO format data into tuple
    return (data['underlying'], data['side'], data['strike'],
            data['bid'], data['mid'], data['ask'],
            data['last'], data['volume'], data['openInterest'], 
            datetime.fromtimestamp(data['updated']).strftime("%Y-%m-%d"), 
            datetime.fromtimestamp(data['expiration']).strftime("%Y-%m-%d"))

def insert_all_data(data):
    starttime = time()
    cur = conn.cursor()
    data.pop("s")
    pivoted_data = [dict(zip(data.keys(), col)) for col in zip(*data.values())]
    print(f'inserting data for {datetime.fromtimestamp(pivoted_data[0]["updated"]).strftime("%Y-%m-%d")}', end='\t')
    for option in pivoted_data:
        dataTuple = format_data_tuple(option)
        insertData(dataTuple, cur)
    try:
        conn.commit()
        print(f'Success {time() - starttime}', end='\t')
    except:
        print("Failed", end='\t')
    cur.close()
    

def insertData(dataTuple, cur):

    full_statement = f"""
        INSERT INTO Contract_Data(Symbol, Contract_Type, Strike, Bid, Midpoint, Ask, Last, Volume, Open_Int, Obs_Date, Exp_Date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cur.execute(full_statement, dataTuple)


def main(ticker):
    s = HTMLSession()
    obs_date = START_DATE
    while obs_date < CURR_DATE:
        fetch_data(ticker, obs_date, s)
        obs_date += timedelta(days=7)

        
if __name__ == "__main__":
    tick = "AAPL"
    starttime = time()
    if len(sys.argv) > 1:
        print(sys.argv)
        tick = sys.argv[1]
    conn = sqlite3.connect("options_database.db")
    main(tick)
    print(f"Final Time {time() - starttime}")
    