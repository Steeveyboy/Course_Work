from requests_html import AsyncHTMLSession
from datetime import datetime, timedelta
from time import time
# from option_webscraper import insertData
import sqlite3
import sys, asyncio, json, logging

"""_summary_: This program will asyncronously fetch historical stock price data from the marketdata.app API and insert it into the database.
    To run this program, you must insure tokens.txt contains a valid API token for marketdata.app.
"""

logging.basicConfig(level=logging.INFO)


LOG = logging.getLogger(__name__)
f_handler = logging.FileHandler('scraper_logs.log')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
LOG.addHandler(f_handler)
LOG.setLevel(logging.NOTSET)

conn = sqlite3.connect("options_database.db")

START_DATE = datetime.strptime('2010-01-01', '%Y-%m-%d').date()
NEAR_TERM = 23
NEXT_TERM = 37
CURR_DATE = datetime.strptime('2023-06-19', '%Y-%m-%d').date()
# CURR_DATE = datetime.today().date()

TOKEN = open('tokens.txt', 'r').read()
LINK = "https://api.marketdata.app/v1/stocks/candles/W/{ticker}/?token={token}&from={from_date}&to={to_date}&dateformat=timestamp&format=csv&header=false"

async def fetch_data(ticker, session, link):
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
    if "o" in row:
        # Checking if the row is the header
        return
    
    full_statement = f"""
        INSERT INTO price_data(Symbol, open, close, high, low, volume, date_of)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """

    cur.execute(full_statement, tuple([ticker] + row.strip().split(",")))
    

async def main(tickers):
    session = AsyncHTMLSession()
    ls = []
    print(len(tickers))
    for ticker in tickers:
        task = asyncio.create_task(fetch_data(ticker, session, LINK))
        ls.append(task)
        await asyncio.sleep(0.125)
    # await task
    await asyncio.sleep(0.5)
    await asyncio.gather(*ls)

async def fetch_vix():
    vix_link = f'https://api.marketdata.app/v1/indices/candles/W/VIX/?from={START_DATE}&to={CURR_DATE}&dateformat=timestamp&format=csv&header=false'
    session = AsyncHTMLSession()
    task = asyncio.create_task(fetch_data('VIX', session, vix_link))
    await asyncio.sleep(0.1)
    await asyncio.gather(*[task])
    
if __name__ == "__main__":

    starttime = time()
    tickers = json.load(open('../resources/tickers.json', 'r'))
    main(tickers)
    print(f"Final Time {time() - starttime}")
    
    
    
    


