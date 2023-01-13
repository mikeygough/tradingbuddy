from config import *
import pandas as pd
import numpy as np
import databento as db
from fpdf import FPDF

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

UPPER_2 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 2)
UPPER_3 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 3)
UPPER_1 = CLOSE + expected_range(CLOSE, HISTORICAL_VOL, 1)
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

# -- initialize pdf
pdf = FPDF(orientation='L')

# the origin is at the upper-left corner and the current position is by default placed at 1 cm from the borders; the margins can be changed with set_margins.
pdf.add_page()

# set font
pdf.set_font('Arial', 'B', 16)

# a cell is a rectangular area, possibly framed, which contains some text. It is output at the current position. We specify its dimensions, its text (centered or aligned), if borders should be drawn, and where the current position moves after it (to the right, below or to the beginning of the next line)
# TITLE
pdf.cell(w=40, h=10, txt='/ES',
         border=0, ln=0, align='',
         fill=False, link='')
# add line break
# h = the height of the break.
pdf.ln(h='')

# STATISTICS
# print('close', CLOSE)# close
pdf.cell(w=40, h=10, txt='Close: {:.2f}'.format(CLOSE),
         border=0, ln=1, align='',
         fill=False, link='')

# print('high', HIGH)
pdf.cell(w=40, h=10, txt='Period High: {:.2f}'.format(HIGH),
    ln=1)

# print('low', LOW)
pdf.cell(w=40, h=10, txt='Period Low: {:.2f}'.format(LOW),
    ln=1)

# print('return', RETURN)
pdf.cell(w=40, h=10, txt='Period Return: {:.2%}'.format(RETURN),
    ln=1)

# print('one_sd', ONE_SD)
pdf.cell(w=42, h=10, txt='One Sd.: +/-{}'.format(ONE_SD),
    ln=0)

print(pdf.get_x())

# print('two_sd', TWO_SD)
pdf.cell(w=40, h=10, txt='Two Sd.: +/-{}'.format(TWO_SD),
    ln=0)

print(pdf.get_x())

# print('three_sd', THREE_SD)
pdf.cell(w=40, h=10, txt='Three Sd.: +/-{}'.format(THREE_SD),
    ln=1)

# print('historical_vol', HISTORICAL_VOL)
pdf.cell(w=40, h=10, txt='Historical Volatility: {:.2f}'.format(HISTORICAL_VOL),
    ln=1)

# print('one day upper range', UPPER_1)
pdf.cell(w=40, h=10, txt='Upper 1: {:.2f}'.format(UPPER_1),
    ln=1)

# print('two day upper range', UPPER_2)
pdf.cell(w=40, h=10, txt='Upper 2: {:.2f}'.format(UPPER_2),
    ln=1)

# print('three day upper range', UPPER_3)
pdf.cell(w=40, h=10, txt='Upper 3: {:.2f}'.format(UPPER_3),
    ln=1)

# print('four day upper range', UPPER_4)
pdf.cell(w=40, h=10, txt='Upper 4: {:.2f}'.format(UPPER_4),
    ln=1)

# print('five day upper range', UPPER_5)
pdf.cell(w=40, h=10, txt='Upper 5: {:.2f}'.format(UPPER_5),
    ln=1)

# print('one day lower range', LOWER_1)
pdf.cell(w=40, h=10, txt='Lower 1: {:.2f}'.format(LOWER_1),
    ln=1)

# print('two day lower range', LOWER_2)
pdf.cell(w=40, h=10, txt='Lower 2: {:.2f}'.format(LOWER_2),
    ln=1)

# print('three day lower range', LOWER_3)
pdf.cell(w=40, h=10, txt='Lower 3: {:.2f}'.format(LOWER_3),
    ln=1)

# print('four day lower range', LOWER_4)
pdf.cell(w=40, h=10, txt='Lower 4: {:.2f}'.format(LOWER_4),
    ln=1)

# print('five day lower range', LOWER_5)
pdf.cell(w=40, h=10, txt='Lower 5: {:.2f}'.format(LOWER_5),
    ln=1)

pdf.output('2-pandas-fpdf.pdf', 'F')
















