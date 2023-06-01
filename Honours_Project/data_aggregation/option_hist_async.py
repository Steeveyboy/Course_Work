from requests_html import HTMLSession, AsyncHTMLSession
from datetime import datetime, timedelta
# from option_webscraper import insertData
import asyncio
import sqlite3


conn = sqlite3.connect("options_database.db")


START_DATE = datetime.strptime('2023-05-27', '%Y-%m-%d').date()
NEAR_TERM = 23
NEXT_TERM = 37
CURR_DATE = datetime.today().date()

link = "https://api.marketdata.app/v1/options/chain/{ticker}/?date={obs_date}&from={from_date}&to={to_date}"

async def fetch_data(ticker, obs_date, s):
    ## TODO create request to server for data
    print(f"fetching data for {obs_date}")
    near_date = obs_date + timedelta(days=NEAR_TERM)
    next_date = obs_date + timedelta(days=NEXT_TERM)
    res = await s.get(link.format(ticker=ticker, obs_date=obs_date, from_date=near_date, to_date=next_date))
    # return res
    if res.ok:
        insert_all_data(res.json())
    return
    
def format_data_tuple(data):
    ## TODO format data into tuple
    return (data['underlying'], data['side'], data['strike'],
            data['bid'], data['mid'], data['ask'],
            data['last'], data['volume'], data['openInterest'], 
            datetime.fromtimestamp(data['updated']).strftime("%Y-%m-%d"), 
            datetime.fromtimestamp(data['expiration']).strftime("%Y-%m-%d"))

def insert_all_data(data):
    cur = conn.cursor()
    data.pop("s")
    pivoted_data = [dict(zip(data.keys(), col)) for col in zip(*data.values())]
    print(f'inserting data for {dataTuple[-2]}', end='\t')
    for option in pivoted_data:
        dataTuple = format_data_tuple(option)
        insertData(dataTuple, cur)
    conn.commit()
    print(f'Success', end='\n')
    cur.close()
    

def insertData(dataTuple, cur):
    # print(type(dataTuple))
    # cur = conn.cursor()
    full_statement = f"""
        INSERT INTO Contract_Data(Symbol, Contract_Type, Strike, Bid, Midpoint, Ask, Last, Volume, Open_Int, Obs_Date, Exp_Date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cur.execute(full_statement, dataTuple)
    # conn.commit()
    # cur.close()

async def main(ticker):
    # cur = dbconn.cursor()
    s = AsyncHTMLSession()
    obs_date = START_DATE
    while obs_date < CURR_DATE:
        await fetch_data(ticker, obs_date, s)
        # if res.ok:
        #     insert_all_data(res.json(), dbconn)
        #     try:
        #         dbconn.commit()
        #         print("successs", end='\n')
        #     except:
        #         print("fail", end='\n')
        
        obs_date += timedelta(days=1)
        
    # cur.close()
        
if __name__ == "__main__":
    tick = "AAPL"
    # conn = sqlite3.connect("options_database.db")
    asyncio.run(main(tick))
    