import math, datetime, sys, time
from itertools import groupby
from vix_calc_functions import volatility_methods


class vix_calc(volatility_methods):
    def select_options(self, data):
        calls = filter(lambda x: x['contract_type']=='call', data)
        puts = filter(lambda x: x['contract_type']=='put', data)
    
        calls = filter(self.out_of_money, calls)
        puts = filter(self.out_of_money, puts)

        calls = sorted(calls, key=lambda x: abs(x['strike'] - x['stock_price']))
        puts = sorted(puts, key=lambda x: abs(x['strike'] - x['stock_price']))
        
        calls2 = self.filter_serious(calls)
        puts2 = self.filter_serious(puts)
        
        return calls2, puts2
    
    
    def calc_inv_contribution(self, option, strike_int, rfr, T):
        # print(rfr, T, math.e**(rfr*T))
        return (strike_int / (option['strike']**2))*(math.e**(rfr*T))*option['midpoint']
        
    def calc_contributions(self, options, option_first, T, rfr):
        ls = []

        first_cont = self.calc_inv_contribution(options[0], self.strike_interval(option_first, options[1]), rfr, T)
        # first_contribution = strike_interval(option_first, options[1]) / (options[0]['strike']**2) * math.e**(rfr*T)*options[0] - constraint
        ls.append(first_cont)

        for i in range(1, len(options)-1):
            ls.append(self.calc_inv_contribution(options[i], self.strike_interval(options[i-1], options[i+1]), rfr, T))
        
        return ls
    
    def calc_all_contributions(self, calls, puts, T, rfr, F):
        """Calculating the individual contribution of each option returning a list"""
        ls = []
        Call_first = calls[0]
        Puts_first = puts[0]
        K_zero = calls[0]['strike']
        constraint = (1/T)*((F/K_zero - 1) ** 2)

        ls.extend(self.calc_contributions(calls, Puts_first, T, rfr))
        ls.extend(self.calc_contributions(puts, Call_first, T, rfr))

        all_contributions = sum(ls)
        variance = (2/T) * all_contributions - constraint 
        
        return variance
    
    
    def calc_volatility(self, DT):
        data = self.query_date(DT)
        
        if len(data) == 0:
            return None
        
        g = groupby(sorted(data, key=lambda x: x['exp_date']), key=lambda x: x['exp_date'])
        contributions_ls = []
        key_vars = []
        
        
        for exp_dt, opt_dat in g:
                # print(exp_dt)
                calls, puts = self.select_options(list(opt_dat))
                T = self.calc_T(DT, exp_dt)
                
                rfr = self.get_rfr(DT, T)
                if not rfr:
                    return
                
                F = self.calc_forward(calls, puts, rfr, T)
                
                key_vars.append({'T': T, 'rfr': rfr, 'F':F, 'N': (T*525600)})
                contributions_ls.append(self.calc_all_contributions(calls, puts, T, rfr, F))

        time_diff1 = (abs(key_vars[1]['N'] - 43200)/(key_vars[1]['N'] - key_vars[0]['N']))
        time_diff2 = (abs(key_vars[0]['N'] - 43200)/(key_vars[1]['N'] - key_vars[0]['N']))
        
        VIX = 100 * math.sqrt( ((key_vars[0]['T'] * contributions_ls[0] * time_diff1) + (key_vars[1]['T'] * contributions_ls[1]*time_diff2)) * (525600/43200) )
        return VIX

if __name__ == '__main__':
    v = vix_calc()
    
    DT = '2023-03-17'
    if len(sys.argv) > 1:
        DT = sys.argv[1]
    print(f'calculating VIX for {DT}')
    starttime = time.time()
    VIX = v.calc_volatility(DT)
    print(VIX)
    print(f'Finished in {time.time() - starttime} seconds')
    
    