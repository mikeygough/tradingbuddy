# main imports
from config import *
import databento as db
import warnings
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import numpy as np

from fpdf import FPDF
from datetime import date
from collections import OrderedDict
from matplotlib.dates import DateFormatter
from matplotlib.dates import MonthLocator

warnings.filterwarnings('ignore')


def db_download_data(SYMBOLS,
                     SCHEMA,
                     START,
                     END,
                     client=db.Historical(CONSUMER_KEY),
                     safety=True):
    '''
    wrapper for databento data download. returns a dataframe. prints the record count, billable size (bytes) and cost in US Dollars before downloading. if safety is on, prompts for user input before proceeding with the download.
    
    symbols: list of symbols in databento's smart format. for example, ["ES.n.0", "NQ.n.0"] returns the future for each root with the highest open interest
    
    schema: string of data schema. for example "ohlcv-1d"  # open, high, low, close, volume in daily increments

    start: string start date. for example, "2022-03-01T00:00"

    end: string end date. for example, "2022-05-31T00:10"

    client: client object after databento authentication

    safety: boolean, when True prompts the user to enter 'y' to proceed with the data download.
    '''

    # -- get the record count of the time series data query:
    count = client.metadata.get_record_count(
        dataset='GLBX.MDP3',
        symbols=SYMBOLS,
        start=START,
        end=END,
        stype_in='smart',
        schema=SCHEMA
    )
    print("count", count)


    # -- get the billable uncompressed raw binary size: 
    size = client.metadata.get_billable_size(
        dataset='GLBX.MDP3',
        symbols=SYMBOLS,
        start=START,
        end=END,
        stype_in='smart',
        schema=SCHEMA
    )
    print("billable size (bytes)", size)


    # -- get cost estimate in US Dollars:
    cost = client.metadata.get_cost(
        dataset='GLBX.MDP3',
        symbols=SYMBOLS,
        start=START,
        end=END,
        stype_in='smart',
        schema=SCHEMA
    )
    print("cost (US Dollars)", cost)

    # -- get the data
    data = client.timeseries.stream(
        dataset='GLBX.MDP3',
        symbols=SYMBOLS,
        start=START,
        end=END,
        stype_in='smart',
        schema=SCHEMA
    )

    if safety:
        if input("Proceed with the download? (y/n): ") != 'y':
            print("Aborting download...")
            exit()
        else:
            print("Proceeding with download...")
            pass

    # pretty price and time stamps
    df = data.to_df(pretty_px=True, pretty_ts=True)
    return df


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


def create_plot(df):
    '''
    create a time series chart of percent return. uses df generated from za_databento.py for use in the tradingbuddy pdf.
    
    df: pandas dataframe generated from za_databento.py.

    '''
    # format ts_event
    df['ts_event'] = pd.to_datetime(df['ts_event'])

    # calcualate pct change
    first_close = df.iloc[0]['close']
    # pct change = (new - old) / old
    df['cumulative_pct_change'] = ((df['close'] - first_close) / first_close) * 100

    # set font
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams.update({'font.size': 12})

    # create fig, ax
    # by default set in inches...
    # but fpdf is in mm
    fig, ax = plt.subplots(figsize=(3.93701, 1.1811*1.2))

    # plot data
    ax.axhline(y=0, color='#707070', linestyle='--', alpha=0.5)
    ax.plot(df['ts_event'], df['cumulative_pct_change'], color='#53a7db')

    # -- STYLE --
    # remove right and top spines
    ax.spines[['left', 'top']].set_visible(False)
    ax.spines[['right', 'bottom']].set_edgecolor('#707070')

    # set ticks right side
    ax.yaxis.tick_right()
    # hide x and y axis tick marks
    ax.yaxis.set_ticks_position('none') 
    ax.xaxis.set_ticks_position('none') 
    
    # format as percent
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    # format x axis dates
    date_form = DateFormatter("%b")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(MonthLocator())

    return plt


class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L')
        self.add_page()
        self.set_margin(0)


    def draw_circle(self, xpos, ypos, rad=25, symbol='', name=''):
        '''
        draws a filled circle of radius rad at xpos, ypos
        xpos: abscissa of upper-left bounding box
        ypos: ordinate of upper-left bounding box
        rad: radius of circle. for example, 25
        symbol: product symbol. for example '/MES'
        name: product name. for example, 'Micro S&P'
        '''

        # draw circle
        self.set_line_width(1)
        self.set_draw_color(240)
        self.set_fill_color(r=83, g=167, b=219)
        self.circle(x=xpos, y=ypos, r=rad, style='F')

        # add text annotation
        self.set_font('Arial', 'B', 16)
        self.set_xy(xpos, ypos)
        self.cell(w=rad, h=rad-2, txt='{}'.format(symbol), align='C')

        self.set_font('Arial', '', 14)
        self.set_xy(xpos, ypos*2.85)
        self.cell(w=rad, h=rad-2, txt='{}'.format(name), align='C')


    def draw_hilo(self, high, low, close,
              x_start, y_start,
              x_end, y_end):
        '''
        draws a high-low-close line with circle at the most recent close price
        high: underlying high price
        low: underlying low price
        x_start: abscissa of first point
        y_start: ordinate of first point
        x_end: abscissa of second point
        y_end: ordinate of second point
        '''
        
        # draw line
        self.set_line_width(1)
        self.set_draw_color(r=112, g=112, b=112)
        self.line(x1=x_start, y1=y_start,
                 x2=x_end, y2=y_end)

        # calculate close position
        length = x_end - x_start
        high_low = high - low
        close_low = close - low
        circle_x_position = x_start + ((close_low / high_low) * length)

        # draw circle at close position
        self.draw_circle(xpos=circle_x_position, ypos=y_start-1.5, rad=3)

        # add annotations
        self.set_font('Arial', '', 12)
        
        # draw low text
        self.set_xy(x_start - self.get_string_width('{:,.0f}'.format(low)) - 2,
                   y_start-8)
        self.cell(h=10, txt='{:,.0f}'.format(low), align='L')
        self.set_xy(x_start - self.get_string_width('Low') - 2, y_start-2)
        self.cell(h=10, txt='Low', align='L')

        # draw high text
        self.set_xy(x_end, y_end-8)
        self.cell(h=10, txt='{:,.0f}'.format(high), align='L')
        self.set_xy(x_end, y_end-2)
        self.cell(h=10, txt='High', align='L')
        
        # draw close text
        self.set_font('Arial', '', 14)
        self.set_xy(circle_x_position - (self.get_string_width('{:,.0f}'.format(close)) / 2),       y_end-12)
        self.cell(h=10, txt='{:,.0f}'.format(close), align='C')


    def draw_sd(self, xpos, ypos, sd):
        '''
        plots a normal distribution with one, two and three standard deviation movement values.
        xpos: x position
        ypos: y position
        sd: float standard deviation value
        '''

        # plot the standard curve
        self.image('static/distribution.png', x=xpos, y=ypos,
                  h=30, w=100)

        # add annotations
        self.set_font('Arial', '', 12)
        
        # write lows
        sd_one_len = self.get_string_width(str(int(sd)))
        sd_two_len = self.get_string_width(str(int(sd * 2.0)))
        sd_three_len = self.get_string_width(str(int(sd * 3.0)))
        
        # low 3
        self.set_xy(xpos*1.05, ypos+28)
        self.cell(h=10, txt='{:,.0f}'.format(int(sd * 3.0)), align='L')

        # low 2
        self.set_xy(xpos*1.19, ypos+28)
        self.cell(h=10, txt='{:,.0f}'.format(int(sd * 2.0)), align='L')

        # low 1
        self.set_xy(xpos*1.35, ypos+28)
        self.cell(h=10, txt='{:,.0f}'.format(int(sd)), align='L')

        # write highs
        # high 1
        self.set_xy(xpos*1.53, ypos+28)
        self.cell(h=10, txt='{:,.0f}'.format(int(sd)), align='L')

        # high 2
        self.set_xy(xpos*1.66, ypos+28)
        self.cell(h=10, txt='{:,.0f}'.format(int(sd * 2.0)), align='L')

        # high 3
        self.set_xy(xpos*1.80, ypos+28)
        self.cell(h=10, txt='{:,.0f}'.format(int(sd * 3.0)), align='L')


def main():

    # set symbols dict
    symbols = {'/MES': 'ES.n.0',
               '/MNQ': 'MNQ.n.0',
               '/MYM': 'MYM.n.0',
               '/M2K': 'M2K.n.0'}
    all_stats = {}

    for symbol in symbols:
        # set output file name
        fname = 'static/{}.csv'.format(symbol)
        # download data
        # ----- for testing we can turn this off ----- #
        db_download_data(SYMBOLS=[symbols[symbol]],
                SCHEMA='ohlcv-1d',
                START='2022-10-30T00:00',
                END='2023-01-30T00:10',
                safety=False).to_csv(fname)
        # ----- for testing we can turn this off ----- #
        # read in data
        df = pd.read_csv(fname)
        # calculate stats
        stats = calculate_stats(df)
        # append to allstats
        all_stats['{}'.format(symbol)] = stats
        # create plot
        create_plot(df).savefig('static/{}_chart.png'.format(symbol), bbox_inches='tight', transparent=True)

    # create pdf
    pdf = PDF()
    # prevent auto page break
    pdf.set_auto_page_break(auto=False)
    
    # add header
    pdf.set_font('Arial', 'B', 22)
    pdf.set_xy(8, 5)
    pdf.cell(30, 10, 'Trading Buddy', align='L')

    # add date
    pdf.set_font('Arial', '', 12)
    pdf.set_xy(-40, 5)
    pdf.cell(30, 10, '{}'.format(date.today().strftime('%B %d, %Y')), align='L')
    
    # add subheader
    pdf.set_font('Arial', 'I', 18)
    pdf.set_text_color(r=112, g=112, b=112)
    pdf.set_xy(8, 15)
    pdf.cell(30, 10, 'Equity Markets', align='L')

    # add footer
    pdf.set_font('Arial', 'I', 6)
    pdf.set_xy(8, -10)
    pdf.multi_cell(275, txt='*All statistics measure the last three months of data unless otherwise stated.\n© The information in this advertisement is current as of the date noted, is for informational purposes only, and does not contend to address the financial objectives, situation, or specific needs of any individual investor.Trading futures involves the risk of loss, including the possibility of loss greater than your initial investment.', align='L')
    pdf.set_text_color(r=0, g=0, b=0)

    # set initial start positions
    xpos_start = 10
    ypos_start = 40
    # write to pdf
    for stats in all_stats:
        # draw symbol circle
        pdf.draw_circle(xpos=xpos_start, ypos=ypos_start, symbol='{}'.format(stats), 
            name='')

        # draw sd
        pdf.draw_sd(xpos=xpos_start+95, ypos=ypos_start-3, sd=all_stats[stats]['one_sd'])

        # draw high low close
        pdf.draw_hilo(high=all_stats[stats]['high'], 
                      low=all_stats[stats]['low'], 
                      close=all_stats[stats]['close'], 
                      x_start=xpos_start+45, y_start=ypos_start+12,
                      x_end=xpos_start+90, y_end=ypos_start+12)
    
        # add chart
        pdf.image('static/{}_chart.png'.format(stats), 
                  x=xpos_start+198, y=ypos_start-1, h=35, w=85)

        ypos_start += 40

    # add content explainers
    pdf.set_font('Arial', 'I', 10)
    pdf.set_xy(50, 28)
    pdf.multi_cell(60, txt='Current prices relative to recent highs and lows*',
             align='C')

    pdf.set_xy(125, 28)
    pdf.multi_cell(60, txt='Probability of daily net change inside these ranges', align='C')

    pdf.set_xy(215, 28)
    pdf.multi_cell(60, txt='Percentage path taken to current overall return', align='C')

    # output file
    pdf.output('static/project_app.pdf')


if __name__ == '__main__':
    main()
