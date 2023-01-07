from config import *
import pandas as pd
import numpy as np
import databento as db

df = pd.read_csv('static/data.csv')


print(df.head())

CLOSE = df.iloc[-1]['close']
HIGH = round(df['close'].max(), 2)
LOW = round(df['close'].min(), 2)
# add rounding and formatting
RETURN = (df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[-1]['close']
ONE_SD = int(df['close'].diff(1).std())
TWO_SD = int(ONE_SD * 2.)
THREE_SD = int(ONE_SD * 3.)
HISTORICAL_VOL = np.sqrt(252) * np.std(df['close'].pct_change(1))
UPPER_1 = CLOSE + (CLOSE * HISTORICAL_VOL * np.sqrt(1/365))
UPPER_2 = CLOSE + (CLOSE * HISTORICAL_VOL * np.sqrt(2/365))
UPPER_3 = CLOSE + (CLOSE * HISTORICAL_VOL * np.sqrt(3/365))
UPPER_4 = CLOSE + (CLOSE * HISTORICAL_VOL * np.sqrt(4/365))
UPPER_5 = CLOSE + (CLOSE * HISTORICAL_VOL * np.sqrt(5/365))
LOWER_1 = CLOSE - (CLOSE * HISTORICAL_VOL * np.sqrt(1/365))
LOWER_2 = CLOSE - (CLOSE * HISTORICAL_VOL * np.sqrt(2/365))
LOWER_3 = CLOSE - (CLOSE * HISTORICAL_VOL * np.sqrt(3/365))
LOWER_4 = CLOSE - (CLOSE * HISTORICAL_VOL * np.sqrt(4/365))
LOWER_5 = CLOSE - (CLOSE * HISTORICAL_VOL * np.sqrt(5/365))

print('close', CLOSE)
print('high', HIGH)
print('low', LOW)
print('return', RETURN)
print('one_sd', ONE_SD)
print('two_sd', TWO_SD)
print('three_sd', THREE_SD)
print('historical_vol', HISTORICAL_VOL)
print('upper one', UPPER_1)
print('upper two', UPPER_2)
print('upper three', UPPER_3)
print('upper four', UPPER_4)
print('upper five', UPPER_5)
print('lower one', LOWER_1)
print('lower two', LOWER_2)
print('lower three', LOWER_3)
print('lower four', LOWER_4)
print('lower five', LOWER_5)
