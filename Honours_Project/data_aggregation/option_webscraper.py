from requests_html import HTMLSession
import sqlite3
from datetime import date

# Target https://www.barchart.com/stocks/quotes/stock/options

# link = """https://www.barchart.com/stocks/quotes/{ticker}/options?expiration={expiration_date}-m&view={frmat}&moneyness={moneyness}"""
link = """https://www.barchart.com/stocks/quotes/{symbol}/options?expiration={expiry}-w&view=stacked&moneyness=allRows"""
link2 = """https://www.barchart.com/proxies/core-api/v1/options/get?baseSymbol={symbol}&fields=symbol%2CbaseSymbol%2CstrikePrice%2Cmoneyness%2CbidPrice%2Cmidpoint%2CaskPrice%2ClastPrice%2CpriceChange%2CpercentChange%2Cvolume%2CopenInterest%2CopenInterestChange%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20volumeOpenInterestRatio%2Cvolatility%2CoptionType%2CdaysToExpiration%2CexpirationDate%2CtradeTime%2ChistoricVolatility30d%2CbaseNextEarningsDate%2CsymbolCode%2CsymbolType&groupBy=optionType&expirationDate={expiry}&meta=field.shortName%2Cexpirations%2Cfield.description&orderBy=strikePrice&orderDir=asc&expirationType=weekly&raw=1"""

conn = sqlite3.connect("options_database.db")


def main(session):

    r = session.get(link.format(symbol="AAPL", expiry="2023-05-26"))

    dateOf = r.html.select("#main-content-column > div > div.page-title.symbol-header-info.ng-scope > div.symbol-price-wrapper > div.pricechangerow.ng-scope > span.symbol-trade-time.ng-binding")
    XSRF = r.cookies.get("XSRF-TOKEN")[:-3]
    headers = {"Cookie": f"laravel_token={session.cookies.get('laravel_token')}", "X-Xsrf-Token":XSRF}

    res = session.get(link2.format(symbol="AAPL", expiry="2023-05-26"),  headers=headers)
    insertData(res.json()["data"])

def formatInsertTuple(row, observed_date):
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

def insertData(data):
    cur = conn.cursor()

    full_statement = f"""
        INSERT INTO Contract_Data(Symbol, Contract_Type, Strike, Bid, Midpoint, Ask, Last, Volume, Open_Int, Obs_Date, Exp_Date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    observed_date = getObservedDate()

    for opt in data["Put"]:
        dataTuple = formatInsertTuple(opt, observed_date)
        cur.execute(full_statement, dataTuple)

    for opt in data["Call"]:
        dataTuple = formatInsertTuple(opt)
        cur.execute(full_statement, dataTuple)

    conn.commit()
    cur.close()


if __name__ == "__main__":
    session = HTMLSession()
    main(session)
