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


def main():

    # set file name
    FNAME = 'static/data.csv'

    #### za_databento.py ####
    # --------------------
    # note that authentication is done in the function
    db_download_data(SYMBOLS=["ES.n.0"],
                SCHEMA="ohlcv-1d",
                START="2022-03-01T00:00",
                END="2022-05-31T00:10",
                FNAME=FNAME)


    # zb_pandas.py
    # --------------------
    # create pretty printer
    pp = pprint.PrettyPrinter(depth=4)
    # print
    pp.pprint(calculate_stats(df=pd.read_csv(FNAME)))


    # zc_matplotlib.py
    # --------------------


    # zd_fpdf.py
    # --------------------



if __name__ == '__main__':
    main()
