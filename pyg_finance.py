import os
import math
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st

def get_stock_data(ticker, years):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=years*365)
    stock = yf.Ticker(ticker)
    # Retrieve historical price data
    hist_data = stock.history(start=start_date, end=end_date)
    return hist_data
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
# Import your data
tickers = ["MSFT", "NVDA", "ANET", "TSLA", "GFS"]
years =  3
hist = pd.DataFrame()
first = 0
for ticker in tickers:
    data = get_stock_data(ticker, 3)
    data['date'] = data.index
    data['ticker'] = ticker
    if first == 0:
        hist = data
        first = 1
    else:
        hist = pd.concat([hist, data])
        st.write(hist.ticker.drop_duplicates())
          
hist['daily change'] = (hist.Close - hist.Open)/hist.Open
hist['volatility'] = (hist.High - hist.Low)/hist.Open
pyg_app = StreamlitRenderer(hist)
 
pyg_app.explorer()

