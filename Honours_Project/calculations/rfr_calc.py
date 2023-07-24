from scipy.interpolate import CubicSpline

"""This file will handle calculating the risk free rate for a given day over a period of time."""

# PERIODS = {'1mo': 1/12, '2mo': 2/12, '3mo':3/12, '4mo':4/12, '6mo':1/2, '1yr':1, '2yr':2, '3yr':3, '5yr':5, '7yr':7, '10yr':10, '20yr':20, '30yr':30}
PERIODS = {'1mo': 30/365, '2mo': 60/365, '3mo':91/365, '4mo':121/365, '6mo':182/365, '1yr':1, '2yr':2, '3yr':3, '5yr':5, '7yr':7, '10yr':10, '20yr':20, '30yr':30}
# PERIODS = {'1mo': 30, '2mo': 60, '3mo':91, '4mo':121, '6mo':182, '1yr':365, '2yr':365*2, '3yr':365*3, '5yr':365*5, '7yr':365*7, '10yr':365*10, '20yr':365*20, '30yr':365*30}







