from config import *
import databento as db
import warnings
warnings.filterwarnings('ignore')

def main():

    #### 1-databento.py ####
    # --------------------
    # first, authenticate to databento
    client = db.Historical(CONSUMER_KEY)




    # 2-pandas.py

    # 3-matplotlib.py

    # 4-fpdf.py

if __name__ == '__main__':
    main()
