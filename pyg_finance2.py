import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
from openbb import obb

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit for Finance",
    layout="wide"
)
df_daily = obb.equity.price.historical(symbol="tsla", 
                                       start_date="2023-01-01", 
                                       end_date="2023-12-31", 
                                       interval="1d", 
                                       provider="yfinance", 
                                       adjusted=True).to_df()
df_daily.drop(['dividends', 'stock_splits'], axis=1, inplace=True)

st.write(df_daily)
pyg_app = StreamlitRenderer(df_daily)
pyg_app.explorer()

