from config import *
import databento as db

# authenticate
client = db.Historical(CONSUMER_KEY)

# -- get ESM2 and NQZ2 data in 1-second OHLCV bars:
# data = client.timeseries.stream(
#     dataset="GLBX.MDP3",
#     symbols=["ESM2", "NQZ2"],
#     schema="ohlcv-1s",
#     start="2022-06-06T14:30",
#     end="2022-06-06T14:40",
# )
# data.replay(print)

# -- get the ES future with the highest open interest.
data = client.timeseries.stream(
    dataset="GLBX.MDP3",
    symbols=["ES.n.0"], # smart symbology
    stype_in='smart',
    schema="ohlcv-1d",
    start="2022-06-06T00:00",
    end="2022-06-07T00:10",
    limit=1
)

df = data.to_df()
print(df.iloc[0].to_json(indent=4))

