# %%
import polars as pl
import pandas as pd

import plotly.graph_objects as go
from datetime import datetime
from lets_plot import *
LetsPlot.setup_html()

# %%
pdat = pl.read_parquet("stock.parquet")

# %%
# Create a time series chart that shows performance of all 10 stocks.


# %%
# now fix the html size and only show the last year and save the chart

# %%
## plotly candlestick chart
# https://plotly.com/python/candlestick-charts/



# %%
# Create a time series chart that shows performance of all 10 stocks.
ggplot(pdat, aes(x="date", y="AdjClose", color = "ticker")) + \
    geom_line() + \
    scale_x_datetime() + \
    labs(
        x="Date",
        y="Adjusted Close",
        title="Top 10 Stocks in the past 5 years",
    )
# %%
# now fix the html size and only show the last year and save the chart
# %%
## plotly candlestick chart
# https://plotly.com/python/candlestick-charts/
df = pdat.filter(pl.col("ticker") == "WMT")
fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.show()'