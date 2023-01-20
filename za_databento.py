# main imports
from config import *
import databento as db
import warnings
warnings.filterwarnings('ignore')


def db_download_data(SYMBOLS,
                     SCHEMA,
                     START,
                     END,
                     FNAME,
                     client=db.Historical(CONSUMER_KEY)):
    '''
    wrapper for databento data download. exports the downloaded data to fname. prints the record count, billable size (bytes) and cost in US Dollars before downloading. user must enter 'y' to proceed with download.
    
    symbols: list of symbols in smart format. for example, ["ES.n.0", "NQ.n.0"] returns the future for each root with the highest open interest
    
    schema: string of data schema. for example "ohlcv-1d"  # open, high, low, close, volume in daily increments

    start: string start date. for example, "2022-03-01T00:00"

    end: string end date. for example, "2022-05-31T00:10"

    fname: string file export name. for example, "static/data.csv". must include .csv.

    client: client object after databento authentication
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

    if input("Proceed with the download? (y/n): ") != 'y':
        print("Aborting download...")
        exit()
    else:
        print("Proceeding with download...")
        pass

    # pretty price and time stamps
    df = data.to_df(pretty_px=True, pretty_ts=True)
    df.to_csv('{}'.format(FNAME))

    print("Saved to {}".format(FNAME))


def main():

    # note that authentication is done in the function
    db_download_data(SYMBOLS=["ES.n.0"],
                SCHEMA="ohlcv-1d",
                START="2022-03-01T00:00",
                END="2022-05-31T00:10",
                FNAME="static/data.csv")


if __name__ == '__main__':
    main()
