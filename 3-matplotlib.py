from config import *
import pandas as pd
import numpy as np
import databento as db
from fpdf import FPDF
import matplotlib.pyplot as plt

df = pd.read_csv('static/data.csv')
df['ts_event'] = pd.to_datetime(df['ts_event'])

# create pdf
pdf = FPDF(orientation='L')
pdf.set_margin(0)

# add page
pdf.add_page()

print(df.head())

fig, ax = plt.subplots()
ax.plot(df['ts_event'], df['close'])
plt.savefig('static/chart.png', bbox_inches='tight')
# plt.show()

