from config import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# read data
df = pd.read_csv('static/data.csv')

# format ts_event
df['ts_event'] = pd.to_datetime(df['ts_event'])

# create fig, ax
# by default set in inches...
# but fpdf is in mm
fig, ax = plt.subplots(figsize=(3.93701, 1.1811))

# plot data
ax.plot(df['ts_event'], df['close'])

# -- STYLE --
# remove right and top spines
ax.spines[['right', 'top']].set_visible(False)

# format x axis dates
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)

plt.savefig('static/chart.png', bbox_inches='tight')
# plt.show()

