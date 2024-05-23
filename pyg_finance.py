import os
import math
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

def get_stock_data(ticker, years):
    print(ticker)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=years*365)
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

tickers = np.array['MSFT, 'NVDA', 'ANET', 'TSLA']
years =  3
hist_data, balance_sheet, financials, info, news = get_stock_data(ticker, years)
