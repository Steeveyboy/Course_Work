def out_of_money(x):
    if x['contract_type'] == 'call':
        if(x['strike'] > x['stock_price']):
            return True
    else:
        if(x['strike'] < x['stock_price']):
            return True
    return False

def check_serious(bid, ask):
    return (bid > 0 and ask > 0)

def filter_serious(ls):
    ## Takes in a list of options sorted by ascending difference between strike and stock_price.
    new_ls = []
    prev_serious = True
    for opt in ls:
        if check_serious(opt['bid'], opt['ask']):
            new_ls.append(opt)
            prev_serious = True
        else:
            if not prev_serious:
                break
            prev_serious = False
    return new_ls



def my_row_factory(cur, row):
    d={}
    for idx, col in enumerate(cur.description):
        d[col[0].lower()] = row[idx]
    return d

def query_date(dt):
    conn = sqlite3.connect("../data_aggregation/options_database.db")
    conn.row_factory = my_row_factory
    cursor = conn.cursor()

    query = f"""
    select 
        contract_data.*,
        price_data.close as stock_price
    from contract_data
    join price_data
    on (price_data.Symbol = contract_data.Symbol) and (price_data.date_of_close = contract_data.obs_date)
        where
            contract_data.symbol ='SPY'
            and obs_date = {dt}
    ;
"""
# '2023-05-12'

    cursor.execute(query)
    data = cursor.fetchall()
    return data

if __name__ == '__main__':
    data = query_date('2023-05-12')
    dd = filter(out_of_money, data)

    calls = filter(lambda x: x['contract_type']=='call', dd)
    puts = filter(lambda x: x['contract_type']=='put', dd)

    calls = sorted(calls, key=lambda x: abs(x['strike'] - x['stock_price']))
    puts = sorted(puts, key=lambda x: abs(x['strike'] - x['stock_price']))

    calls2 = filter_serious(calls)
    puts2 = filter_serious(puts)
    
    
    