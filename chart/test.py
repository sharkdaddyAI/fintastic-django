import plotly.plotly as py
import plotly.graph_objs as go

import pandas_datareader as web
from datetime import datetime

df = web.DataReader("aapl", 'morningstar').reset_index()

trace = go.Candlestick(x=df.Date,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
py.iplot(data, filename='simple_candlestick')

