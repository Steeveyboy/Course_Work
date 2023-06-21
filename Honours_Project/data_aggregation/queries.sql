
select 
    contract_data.*,
    price_data.close as stock_price
from contract_data
join price_data
-- on price_data.Symbol = contract_data.Symbol
on (price_data.Symbol = contract_data.Symbol) and (price_data.date_of_close = contract_data.obs_date)
    where
        contract_data.symbol ='SPY'
        and obs_date between '2023-05-01' and '2023-06-21'
;
