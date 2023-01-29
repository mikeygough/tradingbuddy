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
        # db_download_data(SYMBOLS=[symbols[symbol]],
        #         SCHEMA='ohlcv-1d',
        #         START='2022-03-01T00:00',
        #         END='2022-05-31T00:10',
        #         FNAME=fname,
        #         safety=False)
        # read in data
        df = pd.read_csv(fname)
        # calculate stats
        stats = calculate_stats(df)
        # append to allstats
        all_stats['{}'.format(symbol)] = stats
        # create plot
        create_plot(df, FNAME='static/{}_chart.png'.format(symbol))

    # create pdf
    pdf = PDF()
    # prevent auto page break
    pdf.set_auto_page_break(auto=False)
    # set initial start positions
    xpos_start = 10
    ypos_start = 10
    # write to pdf
    for stats in all_stats:
        print('xpos_start', xpos_start)
        print('ypos_start', ypos_start)
        # symbol circle
        pdf.draw_circle(xpos=xpos_start, ypos=ypos_start, symbol='{}'.format(stats), 
            name='')

        # draw sd
        pdf.draw_sd(xpos=xpos_start+95, ypos=ypos_start-3, sd=all_stats[stats]['one_sd'])

        # high low close
        pdf.draw_hilo(high=all_stats[stats]['high'], 
                      low=all_stats[stats]['low'], 
                      close=all_stats[stats]['close'], 
                      x_start=xpos_start+45, y_start=ypos_start+12,
                      x_end=xpos_start+90, y_end=ypos_start+12)
    
        # add chart
        pdf.image('static/{}_chart.png'.format(stats), 
                  x=xpos_start+198, y=ypos_start-1, h=35, w=85)

        ypos_start += 45

    # output file
    pdf.output('static/app.pdf')
    

    # # set file name
    # FNAME = 'static/data.csv'

    # #### za_databento.py ####
    # # --------------------
    # # note that authentication is done in the function

    # # ----- for testing we can turn this off ----- #
    # db_download_data(SYMBOLS=['ES.n.0'],
    #             SCHEMA='ohlcv-1d',
    #             START='2022-03-01T00:00',
    #             END='2022-05-31T00:10',
    #             FNAME=FNAME)
    # # ----- for testing we can turn this off ----- #


    # #### zb_pandas.py ####
    # # --------------------
    # # read in data
    # df = pd.read_csv(FNAME)

    # # calculate stats
    # stats = calculate_stats(df)
    
    # # create pretty printer
    # pp = pprint.PrettyPrinter(depth=4)
    
    # # print
    # pp.pprint(stats)


    # #### zc_matplotlib.py ####
    # # --------------------
    # create_plot(df, FNAME='static/chart.png')


    #### zd_fpdf.py ####
    # --------------------
    # # create pdf
    # pdf = PDF()

    # # first symbol
    # # symbol circle
    # pdf.draw_circle(xpos=10, ypos=10, symbol='/ES', name='Micro S&P')

    # # draw sd
    # pdf.draw_sd(xpos=105, ypos=7, sd=stats['one_sd'])

    # # high low close
    # pdf.draw_hilo(high=stats['high'], low=stats['low'], close=stats['close'], 
    #           xpos_start=55, ypos_start=22,
    #           xpos_end=100, ypos_end=22)
    
    # # add chart
    # pdf.image('static/chart.png', x=208, y=9,
    # h=35, w=85)

    # # output file
    # pdf.output('static/app.pdf')


if __name__ == '__main__':
    main()
