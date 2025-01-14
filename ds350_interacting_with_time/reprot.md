## "How to use Volume in Trading Strategy"


### Question:
__"How does trading volume correlate with price movements? Are there specific instances of high volume coinciding with significant price changes, providing potential signals for an investor's trading strategy?"__

```{python}
# %%
import polars as pl
import pandas as pd

import plotly.graph_objects as go
from datetime import datetime
from lets_plot import *
LetsPlot.setup_html()
```

I created a new column called Price_Difference to support my study. I calculated the magnitude of the move by dividing the daily price change by the opening price
```{python}
# %%
pdat = pl.read_parquet("stock.parquet")

pdat = pdat.with_columns(
    Price_Difference=(pdat['Close'] - pdat['Open']) /  pdat['Open']
)
```

Let's first use describe() to study the Volume and Price_Difference data to help us find how to define significant price changes. We sperate the dataset into three parts according to the daily rise and fall of price.

```{python}
# %%
price_rise_pdat = pdat.filter(pdat['Price_Difference'] > 0)
price_stay_pdat = pdat.filter(pdat['Price_Difference'] == 0)
price_drop_pdat = pdat.filter(pdat['Price_Difference'] < 0)
# %%
price_rise_pdat.select(['Volume', 'Price_Difference']).describe()
# %%
price_drop_pdat.select(['Volume', 'Price_Difference']).describe()
```

After studying the data, I am going to use five percent as an indicator to explore.

```{python}
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
fig_rise = go.Figure(data=rise, layout=layout_rise)
# %%
fig_drop = go.Figure(data=drop, layout=layout_rise)
```

```{python}
fig_rise.show()
```

```{python}
fig_drop.show()
```

## Summary
From these two figures, we can find that when the rise and fall are large, there is indeed a certain relationship between the rise and fall and the volume. When the volume is small, the stock price is more likely to move significantly, and when the volume is large, the stock price is more likely to move smaller.