from config import *
import pandas as pd
import numpy as np
import databento as db
from fpdf import FPDF

# --define functions--
def draw_circle(xpos, ypos, rad=25, symbol=''):
    '''
    draws a filled in circle of radius rad as xpos, ypos
    xpos: abscissa of upper-left bounding box
    ypos: ordinate of upper-left bounding box
    rad: radius of circle, default 25
    '''
    pdf.set_line_width(1)
    pdf.set_draw_color(240)
    pdf.set_fill_color(r=230, g=30, b=180)
    pdf.circle(x=xpos, y=ypos, r=rad, style='F')

    # add text annotation
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_xy(xpos, ypos)
    pdf.cell(w=rad, h=rad-2, txt='{}'.format(symbol), align='C')


def draw_hilo(high, low, close,
              xpos_start, ypos_start,
              xpos_end, ypos_end):
    '''
    draws a high-low-close line with circle at the current price
    high: underlying high price
    low: underlying low price
    xpos_start: abscissa of first point
    ypos_start: ordinate of first point
    xpos_end: abscissa of second point
    ypos_end: ordinate of second point
    '''
    # draw line
    pdf.set_line_width(1)
    pdf.set_draw_color(r=230, g=30, b=180)
    pdf.line(x1=xpos_start, y1=ypos_start,
             x2=xpos_end, y2=ypos_end)

    # calculate line length
    length = np.sqrt((xpos_end - xpos_start) ** 2 + (ypos_end - ypos_start) ** 2)
    # calculate position percent
    close_pct = close / high
    # calculate additional line pos
    additional_pos = close_pct * length
    # calculate circle position
    circle_x_position = additional_pos + xpos_start

    # draw circle at position
    draw_circle(xpos=circle_x_position, ypos=ypos_start-1.5, rad=3)

    # add annotations
    pdf.set_font('Helvetica', 'B', 12)
    
    # draw low text
    pdf.set_xy(xpos_start - pdf.get_string_width('{}'.format(low)) - 2,
               ypos_start-8)
    pdf.cell(h=10, txt='{}'.format(low), align='L')
    pdf.set_xy(xpos_start - pdf.get_string_width('Low') - 2, ypos_start-2)
    pdf.cell(h=10, txt='Low', align='L')

    # draw high text
    pdf.set_xy(xpos_end, ypos_end-8)
    pdf.cell(h=10, txt='{}'.format(high), align='L')
    pdf.set_xy(xpos_end, ypos_end-2)
    pdf.cell(h=10, txt='High', align='L')
    
    # draw close text
    pdf.set_font('Helvetica', 'B', 14)

    pdf.set_xy(circle_x_position - (pdf.get_string_width('{}'.format(close)) / 2),       ypos_end-12)
    pdf.cell(h=10, txt='{}'.format(close), align='C')
    # pdf.set_xy(circle_x_position - (pdf.get_string_width('Close') / 2), ypos_end-2)
    # pdf.cell(h=10, txt='Close', align='C')

def draw_sd(xpos, ypos):
    '''
    draws a normal distribution with 1, 2 & 3 sd movement values
    '''
    # standard deviation
    # std lines
    pdf.set_line_width(0.5)
    pdf.set_draw_color(37, 37, 37)
    
    #155 is the middle
    middle = xpos + 50
    
    # ~1 sd
    pdf.line(x1=xpos+43, y1=ypos+16,
             x2=xpos+43, y2=ypos+28)
    pdf.line(x1=xpos+59, y1=ypos+15,
             x2=xpos+59, y2=ypos+28)
    # ~2 sd
    pdf.set_draw_color(82, 82, 82)
    pdf.line(x1=xpos+35, y1=ypos+24,
             x2=xpos+35, y2=ypos+28)
    pdf.line(x1=xpos+67, y1=ypos+23.5,
             x2=xpos+67, y2=ypos+28)
    # ~3 sd
    pdf.set_draw_color(115, 115, 115)
    pdf.line(x1=xpos+25, y1=ypos+27,
             x2=xpos+25, y2=ypos+28)
    pdf.line(x1=xpos+77, y1=ypos+27.5,
             x2=xpos+77, y2=ypos+28)

    # base line
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x1=xpos+20, y1=ypos+28,
             x2=xpos+81, y2=ypos+28)

    # standard curve
    pdf.image('static/normal_distribution.png', x=xpos, y=ypos,
    h=30, w=100)

def main():
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
    pdf.set_margin(0)
    # pdf.set_line_width(0)
    # add page
    pdf.add_page()

    # set font
    pdf.set_font('Arial', 'B', 16)

    # high low close
    draw_hilo(high=HIGH, low=LOW, close=CLOSE, 
              xpos_start=55, ypos_start=22,
              xpos_end=100, ypos_end=22)

    pdf.output('21-pandas-fpdf.pdf')

if __name__ == '__main__':
    main()
