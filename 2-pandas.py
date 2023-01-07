from config import *
import pandas as pd
import numpy as np
import databento as db

df = pd.read_csv('static/data.csv')

# -- calculate statistics
# close, high, low
CLOSE = df.iloc[-1]['close']
HIGH = round(df['close'].max(), 2)
LOW = round(df['close'].min(), 2)

# percent return over period (3 months)
# add rounding and formatting
RETURN = (df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[-1]['close']

# daily move standard deviations
ONE_SD = int(df['close'].diff(1).std())
TWO_SD = int(ONE_SD * 2.)
THREE_SD = int(ONE_SD * 3.)
HISTORICAL_VOL = np.sqrt(252) * np.std(df['close'].pct_change(1))

# 1-5 day expected range
def expected_range(s, v, dte, y=365):
    ''' compute the expected range
    s: stock price
    v: annualized volatility
    dte: days to expiration
    y: trading period (one year) '''
    return s * v * np.sqrt(dte / y)
    
UPPER_1 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 1)
UPPER_2 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 2)
UPPER_3 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 3)
UPPER_4 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 4)
UPPER_5 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 5)
LOWER_1 = CLOSE - expected_range(CLOSE, HISTORICAL_VOL, 1)
LOWER_2 = CLOSE - expected_range(CLOSE, HISTORICAL_VOL, 2)
LOWER_3 = CLOSE - expected_range(CLOSE, HISTORICAL_VOL, 3)
LOWER_4 = CLOSE - expected_range(CLOSE, HISTORICAL_VOL, 4)
LOWER_5 = CLOSE - expected_range(CLOSE, HISTORICAL_VOL, 5)

# print
print('close', CLOSE)
print('high', HIGH)
print('low', LOW)
print('return', RETURN)
print('one_sd', ONE_SD)
print('two_sd', TWO_SD)
print('three_sd', THREE_SD)
print('historical_vol', HISTORICAL_VOL)
print('one day upper range', UPPER_1)
print('two day upper range', UPPER_2)
print('three day upper range', UPPER_3)
print('four day upper range', UPPER_4)
print('five day upper range', UPPER_5)
print('one day lower range', LOWER_1)
print('two day lower range', LOWER_2)
print('three day lower range', LOWER_3)
print('four day lower range', LOWER_4)
print('five day lower range', LOWER_5)

