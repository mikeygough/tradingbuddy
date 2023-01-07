from config import *
import databento as db

# authenticate
client = db.Historical(CONSUMER_KEY)

# set attributes
SYMBOLS = ["ES.n.0", "NQ.n.0"] # smart symbology
SYMBOLS = ["ES.n.0"]
SCHEMA = "ohlcv-1d"
START = "2022-03-01T00:00" # start date
END = "2022-05-31T00:10" # end date


# -- get the record count of the time series data query:
count = client.metadata.get_record_count(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)
print("count", count)


# -- get the billable uncompressed raw binary size: 
size = client.metadata.get_billable_size(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)
print("billable size (bytes)", size)


# -- get cost estimate in US Dollars:
cost = client.metadata.get_cost(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)
print("cost (US Dollars)", cost)

# -- get the ES future with the highest open interest:
data = client.timeseries.stream(
    dataset="GLBX.MDP3",
    symbols=SYMBOLS,
    start=START,
    end=END,
    stype_in='smart',
    schema="ohlcv-1d"
)

# pretty price and time stamps
df = data.to_df(pretty_px=True, pretty_ts=True)
# print(df)
df.to_csv('static/data.csv')
