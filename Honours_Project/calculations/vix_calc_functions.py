import sqlite3
import math, datetime
from scipy.interpolate import CubicSpline


class volatility_methods:
    
    """This class implements common methods used in calculating volatility, and should be inherited by other classes that implement volatility calculations."""

    PERIODS = {'1mo': 30/365, '2mo': 60/365, '3mo':91/365, '4mo':121/365, '6mo':182/365, '1yr':1, '2yr':2, '3yr':3, '5yr':5, '7yr':7, '10yr':10, '20yr':20, '30yr':30}


    def calc_T(self, date, exp_date):
        """Calcluating the time to expiration in years"""
        return (datetime.datetime.strptime(exp_date, '%Y-%m-%d') - datetime.datetime.strptime(date, '%Y-%m-%d')).days / 365


    def get_rfr(self, dt, T):
        """
        This function will calculate the risk free rate over a specified time (T in years) for a specified date (dt)
        """
        rates = self.query_treasury_rates(dt)
        if not rates:
            return
        # print(rates)
        x = [self.PERIODS[i] for i,j in list(rates.items())[1:] if j is not None]
        y = [j for j in list(rates.values())[1:]  if j is not None]
        cs = CubicSpline(x, y)
        
        return cs(T) / 100
    
    def calc_forward(self, calls, puts, rtr, T):
        """Calcluating the forward rate of option"""
        F = calls[0]['strike'] + ((math.e ** (rtr*T)) * (calls[0]['midpoint'] - puts[0]['midpoint']))
        return F
    
    
    
    
    def my_row_factory(self, cur, row):
        d={}
        for idx, col in enumerate(cur.description):
            d[col[0].lower()] = row[idx]
        return d
    
    def query_treasury_rates(self, dt):
        conn = sqlite3.connect("../data_aggregation/flow_database.db")
        conn.row_factory = self.my_row_factory
        cursor = conn.cursor()
        
        QUERY = f"""
        Select 
            *
        from treasury_rates
        where date_of = '{dt}'
        """
        cursor.execute(QUERY)
        data = cursor.fetchone()
        self.treasury_data = data
        return data
    
    def query_date(self, dt):
        conn = sqlite3.connect("../data_aggregation/flow_database.db")
        conn.row_factory = self.my_row_factory
        cursor = conn.cursor()
        
        query = f"""
            with temptable as (
            SELECT
                symbol,
                Contract_Type,
                Strike,
                Bid,
                Midpoint,
                Ask,
                Obs_Date,
                Exp_Date
            FROM contract_data
            WHERE 
                contract_data.symbol ='SPY'
                and obs_date = '{dt}')
            select 
                temptable.symbol,
                temptable.Contract_Type,
                temptable.Strike,
                temptable.bid,
                temptable.Midpoint,
                temptable.ask,
                temptable.Obs_Date,
                temptable.Exp_Date,
                price_data.close as stock_price
            from temptable
            join price_data
                on (price_data.Symbol = temptable.Symbol) and (price_data.date_of_close = temptable.Obs_Date)
                where
                    ((Exp_Date = (select min(Exp_Date) from temptable)) or Exp_Date = (select max(Exp_Date) from temptable))
                    and (select COUNT( DISTINCT Exp_Date) from temptable) > 1
            ;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        self.options_data = data
        return data
    
    
    def filter_serious(self, ls):
        ## Takes in a list of options sorted by ascending difference between strike and stock_price.
        new_ls = []
        prev_serious = True
        for opt in ls:
            if self.check_serious(opt['bid'], opt['ask']):
                new_ls.append(opt)
                prev_serious = True
            else:
                if not prev_serious:
                    break
                prev_serious = False
        return new_ls
    
    
    def check_serious(self, bid, ask):
        return (bid > 0 and ask > 0)
    
    
    def out_of_money(self, x):
        """Filters for out of the money options.
        Args:
            x (List): list of options represented as dictionaries.
        Returns:
            Boolean: True if the option is OTM, False otherwise.
        """
        
        if x['contract_type'] == 'call':
            if(x['strike'] >= x['stock_price']):
                return True
        else:
            if(x['strike'] <= (x['stock_price'])):
                return True
        return False

    def in_the_money(self, data):
        """Filters for in the money options.
        Args:
            x (List): list of options represented as dictionaries.
        Returns:
            Boolean: True if the option is ITM, False otherwise.
        """
        
        if data['contract_type'] == 'call':
            if(data['strike'] <= data['stock_price']):
                return True
        else:
            if(data['strike'] >= (data['stock_price'])):
                return True
        return False
    
    
    
    
    def strike_interval(self, option1, option2):
        """Calculates the interval between two strike prices"""
        return abs(option1['strike'] - option2['strike']) / 2
    