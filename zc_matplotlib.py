from config import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.dates import MonthLocator
import matplotlib.ticker as mtick


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


def main():
    # read data
    df = pd.read_csv('static/MES.csv')

    create_plot(df)


if __name__ == '__main__':
    main()
