from config import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


def create_plot(df, FNAME):
    ''' create a time series chart of close prices saved to FNAME. for use in tradingbuddy pdf. uses df generated from za_databento.py
    
    df: pandas dataframe generated from za_databento.py.

    FNAME: filename to save to. for example, 'static/chart.png'

    '''
    # format ts_event
    df['ts_event'] = pd.to_datetime(df['ts_event'])

    # calcualate pct change
    first_close = df.iloc[0]['close']
    # pct change = (new - old) / old
    df['cumulative_pct_change'] = ((df['close'] - first_close)) / first_close

    # create fig, ax
    # by default set in inches...
    # but fpdf is in mm
    fig, ax = plt.subplots(figsize=(3.93701, 1.1811*1.2))

    # plot data
    ax.plot(df['ts_event'], df['cumulative_pct_change'])

    # -- STYLE --
    # remove right and top spines
    ax.spines[['left', 'top']].set_visible(False)

    # set ticks right side
    ax.yaxis.tick_right()

    # format x axis dates
    date_form = DateFormatter("%m-%d")
    ax.xaxis.set_major_formatter(date_form)

    plt.savefig(FNAME, bbox_inches='tight', transparent=True)
    # plt.show()

def main():
    FNAME = 'static/chart.png'

    # read data
    df = pd.read_csv('static/data.csv')

    create_plot(df, FNAME)


if __name__ == '__main__':
    main()
