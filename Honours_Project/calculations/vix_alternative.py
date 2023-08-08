import math, datetime, sys, time
from itertools import groupby
from vix_calc_functions import volatility_methods


class vix_alternative(volatility_methods):
    def select_options(self, data):
        ## TODO
        pass
    
    def calc_inv_contribution(self, option, strike_int, rfr, t):
        ## TODO
        pass
    
    def calc_contributions(self, options, option_first, t, rfr):
        ## TODO
        pass
    
    def calc_all_contributions(self, calls, puts, T, rfr, F):
        ## TODO
        pass
    
    def calc_volatility(self, DT):
        ## TODO
        pass
