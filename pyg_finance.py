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
    print(ticker)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=years*365)
    print(start_date)
    stock = yf.Ticker(ticker)

    # Retrieve historical price data
    hist_data = stock.history(start=start_date, end=end_date)

    # Retrieve balance sheet
    balance_sheet = stock.balance_sheet

    # Retrieve financial statements
    financials = stock.financials

    # Retrieve financial info
    info = stock.info

    # Retrieve news articles
    news = stock.news

    return hist_data, balance_sheet, financials, info, news
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
# Import your data
tickers = ["MSFT", "NVDA", "ANET", "TSLA"]
years =  3

for ticker in tickers:
    hist_data, balance_sheet, financials, info, news = get_stock_data(ticker, years)
    
pyg_app = StreamlitRenderer(financials)
 
pyg_app.explorer()

