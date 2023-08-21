BEGIN TRANSACTION;

ATTACH "options_database.db" as db2;

INSERT into main.Contract_Data(Symbol, Contract_Type, Strike, Bid, Midpoint, Ask, volume, obs_date, Exp_Date)
select
    symbol,
    Contract_Type,
    strike, 
    Bid,
    Midpoint,
    Ask, 
    volume, 
    obs_date,
    Exp_Date
from db2.Contract_Data
where Obs_Date > '2015-01-01'
and Symbol == "SPY"
;

INSERT into main.price_data(Symbol, open, close, volume, date_of, date_of_close)
select
    symbol,
    open,
    close,
    volume,
    date_of,
    date_of_close
from db2.price_data
where symbol in ("SPY","VIX")
and date_of > '2015-01-01'
;


INSERT into main.treasury_rates(date_of, '1Mo','2Mo','3Mo','4Mo','6Mo','1Yr','2Yr','3Yr','5Yr','7Yr','10Yr','20Yr','30Yr')
select
    "date_of",
    "1Mo",
    "2Mo",
    "3Mo",
    "4Mo",
    "6Mo",
    "1Yr",
    "2Yr",
    "3Yr",
    "5Yr",
    "7Yr",
    "10Yr",
    "20Yr",
    "30Yr"
from db2.treasury_rates
;

END TRANSACTION;