from config import *
import databento as db

# authenticate
client = db.Historical(CONSUMER_KEY)

# set attributes
SYMBOLS = ["ES.n.0", "NQ.n.0"] # smart symbology
SCHEMA = "ohlcv-1d"
START = "2022-06-01T00:00" # start date
END = "2022-06-30T00:10" # end date

# -- [TEST] get ESM2 and NQZ2 data in 1-second OHLCV bars:
# data = client.timeseries.stream(
#     dataset="GLBX.MDP3",
#     symbols=["ESM2", "NQZ2"],
#     schema="ohlcv-1s",
#     start="2022-06-06T14:30",
#     end="2022-06-06T14:40",
# )
# data.replay(print)

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
df = data.to_df()
print(df)
# print(df.iloc[0].to_json(indent=4))
df.to_csv('test-export.csv')
