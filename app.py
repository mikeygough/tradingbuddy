# main imports
from config import *
import databento as db
import warnings
warnings.filterwarnings('ignore')
import pprint
import pandas as pd

# function imports
from za_databento import db_download_data
from zb_pandas import expected_range, calculate_stats
from zc_matplotlib import create_plot
from zd_fpdf import PDF


def main():

    # set file name
    FNAME = 'static/data.csv'

    #### za_databento.py ####
    # --------------------
    # note that authentication is done in the function

    # ----- for testing we can turn this off ----- #
    # db_download_data(SYMBOLS=["ES.n.0"],
    #             SCHEMA="ohlcv-1d",
    #             START="2022-03-01T00:00",
    #             END="2022-05-31T00:10",
    #             FNAME=FNAME)
    # ----- for testing we can turn this off ----- #


    #### zb_pandas.py ####
    # --------------------
    # read in data
    df = pd.read_csv(FNAME)

    # calculate stats
    stats = calculate_stats(df)
    
    # create pretty printer
    pp = pprint.PrettyPrinter(depth=4)
    
    # print
    pp.pprint(stats)


    #### zc_matplotlib.py ####
    # --------------------
    create_plot(df, FNAME='static/chart.png')


    #### zd_fpdf.py ####
    # --------------------
    # create pdf
    pdf = PDF()

    # first symbol
    # symbol circle
    pdf.draw_circle(xpos=10, ypos=10, symbol='/ES', name='Micro S&P')

    # draw sd
    pdf.draw_sd(xpos=105, ypos=7, sd=stats['one_sd'])

    # high low close
    pdf.draw_hilo(high=stats['high'], low=stats['low'], close=stats['close'], 
              xpos_start=55, ypos_start=22,
              xpos_end=100, ypos_end=22)
    
    # add chart
    # pdf.image('static/chart.png', x=190, y=8,
    # h=30, w=100)

    # output file
    pdf.output('static/app.pdf')


if __name__ == '__main__':
    main()
