import math, datetime, sys, time
from itertools import groupby
from vix_calc_functions import volatility_methods


class vix_alternative(volatility_methods):
    
    
    def get_intrisic_price(self, data):
        if data['contract_type'] == 'call':
            return data["stock_price"] - data["strike"]
        else:
            return data["strike"] - data["stock_price"]
    
    def calc_uncertain_all(self, data):
        for i in range(len(data)):
            data[i]['midpoint'] = data[i]['midpoint'] - self.get_intrisic_price(data[i])
        return data
    
    def select_options(self, data, moneyness):
        
        calls = filter(lambda x: x['contract_type']=='call', data)
        puts = filter(lambda x: x['contract_type']=='put', data)
        
        calls = filter(moneyness, calls)
        puts = filter(moneyness, puts)
        
        calls = sorted(calls, key=lambda x: abs(x['strike'] - x['stock_price']))
        puts = sorted(puts, key=lambda x: abs(x['strike'] - x['stock_price']))
        
        calls2 = self.filter_serious(calls)
        puts2 = self.filter_serious(puts)
        
        return calls2, puts2
        
    
    def calc_inv_contribution(self, option, strike_int, rfr, T):
        
        return (strike_int / (option['strike']**2))*(math.e**(rfr*T))*option['midpoint']
    
    def calc_contributions(self, options, option_first, T, rfr):
        ls = []
        
        first_cont = self.calc_inv_contribution(options[0], self.strike_interval(option_first, options[1]), rfr, T)
        ls.append(first_cont)
        
        for i in range(1, len(options)-1):
            ls.append(self.calc_inv_contribution(options[i], self.strike_interval(options[i-1], options[i+1]), rfr, T))
        
        return ls
    
    def calc_all_contributions(self, calls, puts, T, rfr, F):
        
        ls = []
        Call_first = calls[0]
        Puts_first = puts[0]
        
        ls.extend(self.calc_contributions(calls, Puts_first, T, rfr))
        ls.extend(self.calc_contributions(puts, Call_first, T, rfr))
        
        return ls
    
    def calc_variances(self, contributions, K_zero, T, rfr, F):
        
        constraint = (1/T)*((F/K_zero - 1) ** 2)
        all_contributions = sum(contributions)
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
            options_data = list(opt_dat)
            # print(exp_dt)
            calls, puts = self.select_options(options_data, moneyness=self.out_of_money)
            calls_in, puts_in = self.select_options(options_data, moneyness=self.in_the_money)

            calls_in = self.calc_uncertain_all(calls_in)
            puts_in = self.calc_uncertain_all(puts_in)
            
            T = self.calc_T(DT, exp_dt)
            
            rfr = self.get_rfr(DT, T)
            if not rfr:
                return
            
            F = self.calc_forward(calls, puts, rfr, T)
            
            K_zero = calls[0]['strike']
            
            key_vars.append({'T': T, 'rfr': rfr, 'F':F, 'N': (T*525600)})
            out_contributions = self.calc_all_contributions(calls, puts, T, rfr, F)
            in_contributions = self.calc_all_contributions(calls_in, puts_in, T, rfr, F)

            variance_all = self.calc_variances(out_contributions+in_contributions, K_zero, T, rfr, F)
   
            contributions_ls.append(variance_all)
            
        time_diff1 = (abs(key_vars[1]['N'] - 43200)/(key_vars[1]['N'] - key_vars[0]['N']))
        time_diff2 = (abs(key_vars[0]['N'] - 43200)/(key_vars[1]['N'] - key_vars[0]['N']))

        VIX = 100 * math.sqrt( ((key_vars[0]['T'] * contributions_ls[0] * time_diff1) + (key_vars[1]['T'] * contributions_ls[1]*time_diff2)) * (525600/43200) )
        return VIX

if __name__ == '__main__':
    v = vix_alternative()
    
    DT = '2023-03-17'
    if len(sys.argv) > 1:
        DT = sys.argv[1]
    print(f'calculating VIX for {DT}')
    starttime = time.time()
    VIX = v.calc_volatility(DT)
    print(VIX)
    print(f'Finished in {time.time() - starttime} seconds')
