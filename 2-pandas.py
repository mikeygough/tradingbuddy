from config import *
import pandas as pd
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

print('close', CLOSE)
print('high', HIGH)
print('low', LOW)
print('return', RETURN)
print('one_sd', ONE_SD)
print('two_sd', TWO_SD)
print('three_sd', THREE_SD)
