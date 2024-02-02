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
fig.show()

# %%
# Create a trace for volume as a bar chart
trace_volume = go.Bar(x=pdat['date'], y=pdat['Volume'], name='Volume', opacity=0.7, yaxis='y2')

# %%
traces = []
trace_candlestick = go.Candlestick(x=df['date'],
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'],
                                    name='WMT - Candlestick')


# %%
# Create the layout
layout_close = go.Layout(title='Closing Price Over Time',
                         xaxis=dict(title='Date'),
                         yaxis=dict(title='Closing Price'),
                         yaxis2=dict(title='Volume', overlaying='y', side='right'),
                         legend=dict(x=0, y=1, traceorder='normal'))


traces.extend([trace_candlestick, trace_volume])
# Create the figure
fig_close = go.Figure(data=traces, layout=layout_close)

# Show the interactive plot
fig_close.show()
# %%
pdat = pdat.with_columns(
    Price_Difference=(pdat['Close'] - pdat['Open']) /  pdat['Open']
)
# %%
price_rise_pdat = pdat.filter(pdat['Price_Difference'] >= 0)
price_stay_pdat = pdat.filter(pdat['Price_Difference'] == 0)
price_drop_pdat = pdat.filter(pdat['Price_Difference'] < 0)
# %%
price_rise_pdat.select(['Volume', 'Price_Difference']).describe()
# %%
price_drop_pdat.select(['Volume', 'Price_Difference']).describe()
# %%
price_stay_pdat.select(['Volume', 'Price_Difference']).describe()
# %%
tar_drop = pdat.filter(pdat['Price_Difference'] < -0.05)

# %%
tar_rise = pdat.filter(pdat['Price_Difference'] > 0.05)
# %%
rise = go.Scatter(x=tar_rise['Volume'],
                    y=tar_rise['Price_Difference'],
                    mode='markers',
                    text=tar_rise['date'],  # 在鼠标悬停时显示日期
                    marker=dict(size=10, color='blue'),  # 设置散点的大小和颜色
                    )

drop = go.Scatter(x=tar_drop['Volume'],
                    y=tar_drop['Price_Difference'],
                    mode='markers',
                    text=tar_drop['date'],  # 在鼠标悬停时显示日期
                    marker=dict(size=10, color='blue'),  # 设置散点的大小和颜色
                    )

layout_rise = go.Layout(title='Volume vs Daily Return',
                   xaxis=dict(title='Volume'),
                   yaxis=dict(title='Daily Return (%)'),
                   )
# %%
go.Figure(data=rise, layout=layout_rise)
# %%
go.Figure(data=drop, layout=layout_rise)
# %%
a = pdat.filter(pdat['Price_Difference'] < 0.02)
a =  a.filter(a['Price_Difference'] > -0.02)
a = go.Scatter(x=a['Volume'],
                    y=a['Price_Difference'],
                    mode='markers',
                    text=a['date'],  # 在鼠标悬停时显示日期
                    marker=dict(size=10, color='blue'),  # 设置散点的大小和颜色
                    )
# %%
go.Figure(data=a, layout=layout_rise)
# %%
