from requests_html import HTMLSession
import sqlite3
from datetime import date

"""_summary_: This program will fetch historical option data from barchart.com and insert it into the database.
    This program can be run from the command line or imported into another program and called using the main function.
"""

link = """https://www.barchart.com/stocks/quotes/{symbol}/options?expiration={expiry}-w&view=stacked&moneyness=allRows"""
link2 = """https://www.barchart.com/proxies/core-api/v1/options/get?baseSymbol={symbol}&fields=symbol%2CbaseSymbol%2CstrikePrice%2Cmoneyness%2CbidPrice%2Cmidpoint%2CaskPrice%2ClastPrice%2CpriceChange%2CpercentChange%2Cvolume%2CopenInterest%2CopenInterestChange%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20volumeOpenInterestRatio%2Cvolatility%2CoptionType%2CdaysToExpiration%2CexpirationDate%2CtradeTime%2ChistoricVolatility30d%2CbaseNextEarningsDate%2CsymbolCode%2CsymbolType&groupBy=optionType&expirationDate={expiry}&meta=field.shortName%2Cexpirations%2Cfield.description&orderBy=strikePrice&orderDir=asc&expirationType=weekly&raw=1"""


def main(session, db_conn):

    r = session.get(link.format(symbol="AMZN", expiry="2023-06-02"))

    XSRF = r.cookies.get("XSRF-TOKEN")[:-3]
    headers = {"Cookie": f"laravel_token={session.cookies.get('laravel_token')}", "X-Xsrf-Token":XSRF}

    res = session.get(link2.format(symbol="AMZN", expiry="2023-06-02"),  headers=headers)
    insertDataAll(res.json()["data"], db_conn)

def _formatInsertTuple(row, observed_date):
    return (row['baseSymbol'], 
        row['optionType'],
        row['strikePrice'],
        row['bidPrice'], row['midpoint'],
        row['askPrice'], row['lastPrice'],
        row['volume'], row['openInterest'],
        observed_date, row['expirationDate'])
    # row['tradeTime']

def getObservedDate():
    return date.today().strftime("%m/%d/%Y") 


def insertData(dataTuple, cur):
    # print(type(dataTuple))
    full_statement = f"""
        INSERT INTO Contract_Data(Symbol, Contract_Type, Strike, Bid, Midpoint, Ask, Last, Volume, Open_Int, Obs_Date, Exp_Date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cur.execute(full_statement, dataTuple)
    return
    
def insertDataAll(data, db_conn):
    cur = db_conn.cursor()

    observed_date = getObservedDate()

    for opt in data["Put"][:2]:
        dataTuple = _formatInsertTuple(opt, observed_date)
        insertData(dataTuple, cur)

    for opt in data["Call"]:
        dataTuple = _formatInsertTuple(opt, observed_date)
        insertData(dataTuple, cur)

    db_conn.commit()
    cur.close()


if __name__ == "__main__":
    session = HTMLSession()
    conn = sqlite3.connect("options_database.db")
    main(session, conn)
