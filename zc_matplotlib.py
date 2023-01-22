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

    # create fig, ax
    # by default set in inches...
    # but fpdf is in mm
    fig, ax = plt.subplots(figsize=(3.93701, 1.1811))

    # plot data
    ax.plot(df['ts_event'], df['close'])

    # -- STYLE --
    # remove right and top spines
    ax.spines[['right', 'top']].set_visible(False)

    # format x axis dates
    date_form = DateFormatter("%m-%d")
    ax.xaxis.set_major_formatter(date_form)

    plt.savefig(FNAME, bbox_inches='tight')
    # plt.show()

def main():
    FNAME = 'static/chart.png'

    # read data
    df = pd.read_csv('static/data.csv')

    create_plot(df, FNAME)


if __name__ == '__main__':
    main()