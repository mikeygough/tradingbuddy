# main imports
from config import *
import pandas as pd
import numpy as np
import pprint
from collections import OrderedDict


def expected_range(s, v, dte, y=365):
    ''' 
    compute the expected range over dte days.
    
    s: stock price. for example, 1915.50
    v: annualized volatility. for example, 0.22 (22%)
    dte: days to expiration. for example, 1 will give the one day expected move.
    y: trading period (one year). for example, 365. 
    '''

    return s * v * np.sqrt(dte / y)

def calculate_stats(df):
    '''
    given a dataframe from za_databento.py, return a dictionary of calculated statistics including: close, high, low, % return, one_sd, two_sd, three_sd, % historical_vol, upper_1, upper_2, upper_3, upper_4, upper_5, lower_1, lower_2, lower_3, lower_4 and lower_5.
    
    dataframe: df of data. for example, df.
    '''

    # create ordered dict, stats
    stats = OrderedDict()

    # -- calculate statistics and add to dict
    # close, high, low
    stats['close'] = df.iloc[-1]['close']
    stats['high'] = round(df['close'].max(), 0)
    stats['low'] = round(df['close'].min(), 0)

    # percent return over period (3 months)
    # add rounding and formatting
    stats['return'] = round((df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[-1]['close'], 4)

    # daily move standard deviations
    stats['one_sd'] = int(df['close'].diff(1).std())
    stats['two_sd'] = int(stats['one_sd'] * 2.)
    stats['three_sd'] = int(stats['one_sd'] * 3.)
    stats['historical_vol'] = round(np.sqrt(252) * np.std(df['close'].pct_change(1)), 4)

    # upper and lower n day limits
    stats['upper_1'] = int(stats['close'] + expected_range(stats['close'], 
                       stats['historical_vol'], 1))
    stats['upper_2'] = int(stats['close'] + expected_range(stats['close'], 
                       stats['historical_vol'], 2))
    stats['upper_3'] = int(stats['close'] + expected_range(stats['close'], 
                       stats['historical_vol'], 3))
    stats['upper_4'] = int(stats['close'] + expected_range(stats['close'], 
                       stats['historical_vol'], 4))
    stats['upper_5'] = int(stats['close'] + expected_range(stats['close'], 
                       stats['historical_vol'], 5))
    stats['lower_1'] = int(stats['close'] - expected_range(stats['close'], 
                       stats['historical_vol'], 1))
    stats['lower_2'] = int(stats['close'] - expected_range(stats['close'], 
                       stats['historical_vol'], 2))
    stats['lower_3'] = int(stats['close'] - expected_range(stats['close'], 
                       stats['historical_vol'], 3))
    stats['lower_4'] = int(stats['close'] - expected_range(stats['close'], 
                       stats['historical_vol'], 4))
    stats['lower_5'] = int(stats['close'] - expected_range(stats['close'], 
                       stats['historical_vol'], 5))

    return stats


def main():
    # pretty print
    pp = pprint.PrettyPrinter(depth=4)
    pp.pprint(calculate_stats(df=pd.read_csv('static/MES.csv')))


if __name__ == '__main__':
    main()
