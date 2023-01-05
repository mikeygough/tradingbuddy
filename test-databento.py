from config import *
import databento as db

client = db.Historical(CONSUMER_KEY)
data = client.timeseries.stream(
    dataset="GLBX.MDP3",
    symbols="ESZ2",
    start="2022-06-02T14:20",
    end="2022-06-02T14:30",
)

data.replay(print)
