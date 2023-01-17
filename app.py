from config import *
import databento as db
from fpdf import FPDF
import pandas as pd
import numpy as np

# read data
df = pd.read_csv('static/data.csv')

# initialize dictionary of statistics given list of keys
statkeys = ['close', 'high', 'low', 'return',
            'one_sd', 'two_sd', 'three_sd', 'historical_vol',
            'upper_1', 'upper_2', 'upper_3', 'upper_4', 'upper_5',
            'lower_1', 'lower_2', 'lower_3', 'lower_4', 'lower_5'] 

# using fromkeys() method
stats = dict.fromkeys(statkeys, None)

# -- calculate statistics
# close, high, low
stats['close'] = df.iloc[-1]['close']
stats['high'] = round(df['close'].max(), 2)
stats['low'] = round(df['close'].min(), 2)

# percent return over period (3 months)
# add rounding and formatting
stats['return'] = (df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[-1]['close']

# daily move standard deviations
stats['one_sd'] = int(df['close'].diff(1).std())
stats['two_sd'] = int(stats['one_sd'] * 2.)
stats['three_sd'] = int(stats['one_sd'] * 3.)
stats['historical_vol'] = np.sqrt(252) * np.std(df['close'].pct_change(1))

# 1-5 day expected range
def expected_range(s, v, dte, y=365):
    ''' compute the expected range
    s: stock price
    v: annualized volatility
    dte: days to expiration
    y: trading period (one year) '''
    return s * v * np.sqrt(dte / y)
    
stats['upper_1'] = stats['close'] + expected_range(stats['close'], 
                   stats['historical_vol'], 1)
stats['upper_2'] = stats['close'] + expected_range(stats['close'], 
                   stats['historical_vol'], 2)
stats['upper_3'] = stats['close'] + expected_range(stats['close'], 
                   stats['historical_vol'], 3)
stats['upper_4'] = stats['close'] + expected_range(stats['close'], 
                   stats['historical_vol'], 4)
stats['upper_5'] = stats['close'] + expected_range(stats['close'], 
                   stats['historical_vol'], 5)
stats['lower_1'] = stats['close'] - expected_range(stats['close'], 
                   stats['historical_vol'], 1)
stats['lower_2'] = stats['close'] - expected_range(stats['close'], 
                   stats['historical_vol'], 2)
stats['lower_3'] = stats['close'] - expected_range(stats['close'], 
                   stats['historical_vol'], 3)
stats['lower_4'] = stats['close'] - expected_range(stats['close'], 
                   stats['historical_vol'], 4)
stats['lower_5'] = stats['close'] - expected_range(stats['close'], 
                   stats['historical_vol'], 5)

# print
for k, v in stats.items():
    print(k, v)

# # -- generate pdf
# title = SYMBOLS[0]
# class PDF(FPDF):
#     def header(self):
#         # Arial bold 15
#         self.set_font('Arial', 'B', 15)
#         # Calculate width of title and position
#         w = self.get_string_width(title) + 6
#         self.set_x((210 - w) / 2)
#         # Colors of frame, background and text
#         self.set_draw_color(0, 80, 180)
#         self.set_fill_color(230, 230, 0)
#         self.set_text_color(220, 50, 50)
#         # Thickness of frame (1 mm)
#         self.set_line_width(1)
#         # Title
#         self.cell(w, 9, title, 1, 1, 'C', 1)
#         # Line break
#         self.ln(10)

# pdf = PDF()
# pdf.set_title(title)
# pdf.output('tuto1.pdf', 'F')
