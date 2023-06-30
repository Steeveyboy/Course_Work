from requests_html import AsyncHTMLSession
from datetime import datetime, timedelta
from time import time
# from option_webscraper import insertData
import sqlite3
import sys, asyncio, json, logging

logging.basicConfig(level=logging.INFO)
# logging.root.setLevel(logging.NOTSET)

LOG = logging.getLogger(__name__)
f_handler = logging.FileHandler('scraper_logs.log')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
LOG.addHandler(f_handler)
LOG.setLevel(logging.NOTSET)
# LOG.

conn = sqlite3.connect("options_database.db")

START_DATE = datetime.strptime('2010-01-01', '%Y-%m-%d').date()
NEAR_TERM = 23
NEXT_TERM = 37
CURR_DATE = datetime.strptime('2023-06-19', '%Y-%m-%d').date()
# CURR_DATE = datetime.today().date()

TOKEN = open('tokens.txt', 'r').read()
# print(fr'{TOKEN}')
# link = "https://api.marketdata.app/v1/options/chain/{ticker}/?token={token}&date={obs_date}&from={from_date}&to={to_date}"
link = "https://api.marketdata.app/v1/stocks/candles/W/{ticker}/?token={token}&from={from_date}&to={to_date}&dateformat=timestamp&format=csv&header=false"

async def fetch_data(ticker, session):
    print(f"fetching data for {ticker}")
    res = await session.get(link.format(ticker=ticker, token=TOKEN, from_date=START_DATE, to_date=CURR_DATE))
    if res.ok:
        insert_all_data(res.text, ticker)
    else:
        print(f"No data for {ticker}")
    return

def insert_all_data(data, ticker):
    print(f'Inserting Data for {ticker}')
    cur = conn.cursor()
    try:
        for row in data.strip().split("\n"):
            insert_row(row, cur, ticker)
        conn.commit()
        print("Success")
        cur.close()
        
    except:
        LOG.warning(msg=f"{ticker} Failed")
        cur.close()
    
def insert_row(row, cur, ticker):
    full_statement = f"""
        INSERT INTO price_data(Symbol, open, close, high, low, volume, date_of)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    # print(tuple([ticker] + row.strip().split(",")))
    cur.execute(full_statement, tuple([ticker] + row.strip().split(",")))
    

async def main(tickers):
    session = AsyncHTMLSession()
    ls = []
    print(len(tickers))
    for ticker in tickers:
        task = asyncio.create_task(fetch_data(ticker, session))
        ls.append(task)
        await asyncio.sleep(0.125)
    # await task
    await asyncio.sleep(0.5)
    await asyncio.gather(*ls)


if __name__ == "__main__":
    
    ticks = json.load(open('resources/tickers.json','r'))
    starttime = time()
    asyncio.run(main(list(ticks.keys())))
    print(f"Final Time {time() - starttime}")
    
    
    # session = HTMLSession()
    # print(link.format(ticker='META', token=TOKEN, from_date=START_DATE, to_date=CURR_DATE))
    # res = session.get(link.format(ticker='META', token=TOKEN, from_date=START_DATE, to_date=CURR_DATE))
    # print(res.ok)
    # print(res.html)

