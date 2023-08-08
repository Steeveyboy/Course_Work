
WHERE 
    contract_data.symbol ='SPY'
    and obs_date = '2023-03-17')
SELECT
    temptable.symbol,
    temptable.Contract_Type,
    temptable.Midpoint as calls_mid,
	temptable.Strike,
	puts.Contract_Type as Contract_Type2,
	puts.Midpoint as puts_mid,
    temptable.Obs_Date,
    temptable.Exp_Date,
	Price_Data.close,

from temptable
join (select * from temptable where Contract_Type='put') puts on puts.strike = temptable.strike and puts.Exp_Date = temptable.Exp_Date
join price_data on (price_data.Symbol = temptable.Symbol) and (price_data.date_of_close = temptable.Obs_Date)
where temptable.Contract_Type = 'call'
and temptable.Exp_Date = ( SELECT min(Exp_Date) from temptable)
order by temptable.strike
;
