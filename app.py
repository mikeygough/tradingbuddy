# main imports
from config import *
import databento as db
import warnings
warnings.filterwarnings('ignore')
# function imports
from za_databento import db_download_data

def main():

    #### 1-databento.py ####
    # --------------------
    # note that authentication is done in the function
    db_download_data(SYMBOLS=["ES.n.0"],
                SCHEMA="ohlcv-1d",
                START="2022-03-01T00:00",
                END="2022-05-31T00:10",
                FNAME="static/data.csv")

    # 2-pandas.py

    # 3-matplotlib.py

    # 4-fpdf.py

if __name__ == '__main__':
    main()
