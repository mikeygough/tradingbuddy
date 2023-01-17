from config import *
import databento as db
from fpdf import FPDF
import pandas as pd
import numpy as np

# authenticate
client = db.Historical(CONSUMER_KEY)

# set attributes
SYMBOLS = ["ES.n.0"]
SCHEMA = "ohlcv-1d"
START = "2022-03-01T00:00" # start date
END = "2022-05-31T00:10" # end date


# -- get the record count of the time series data query:
count = client.metadata.get_record_count(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)
print("count", count)


# -- get the billable uncompressed raw binary size: 
size = client.metadata.get_billable_size(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)
print("billable size (bytes)", size)


# -- get cost estimate in US Dollars:
cost = client.metadata.get_cost(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)
print("cost (US Dollars)", cost)


# -- get the ES future with the highest open interest:
data = client.timeseries.stream(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)

# pretty price and time stamps
df = data.to_df(pretty_px=True, pretty_ts=True)


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
# print('close', CLOSE)
# print('high', HIGH)
# print('low', LOW)
# print('return', RETURN)
# print('one_sd', ONE_SD)
# print('two_sd', TWO_SD)
# print('three_sd', THREE_SD)
# print('historical_vol', HISTORICAL_VOL)
# print('one day upper range', UPPER_1)
# print('two day upper range', UPPER_2)
# print('three day upper range', UPPER_3)
# print('four day upper range', UPPER_4)
# print('five day upper range', UPPER_5)
# print('one day lower range', LOWER_1)
# print('two day lower range', LOWER_2)
# print('three day lower range', LOWER_3)
# print('four day lower range', LOWER_4)
# print('five day lower range', LOWER_5)


# -- generate pdf
title = SYMBOLS[0]
class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

pdf = PDF()
pdf.set_title(title)
pdf.output('tuto1.pdf', 'F')
