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
from test_class import pdf


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
    # pdf = FPDF(orientation='L')
    # pdf.set_margin(0)

    # # add page
    # pdf.add_page()

    # # output file
    # pdf.output('static/app.pdf')


if __name__ == '__main__':
    main()
