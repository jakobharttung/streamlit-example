import streamlit as st
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

# Define the ticker symbols
tickers = ['MSFT', 'GOOG', 'TSLA', 'NVDA', 'SAN.PA', 'OR.PA']

# Get 10 years of market close data
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# Retrieve stock data
data = yf.download(tickers, start=start_date, end=end_date)['Close']

# Line chart with range selection
st.title('Stock Performance Analysis')
st.subheader('10 Year Market Close Data')
fig = px.line(data, x=data.index, y=tickers)
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig)

# Add buttons for standard yfinance intervals
intervals = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
for interval in intervals:
    st.button(interval)

# Dropdown for candlestick chart
st.subheader('Candlestick Chart')
selected_ticker = st.selectbox('Select a ticker', tickers)
ticker_data = yf.download(selected_ticker, period='1d', interval='1m')
candlestick = px.line(ticker_data, x=ticker_data.index, y='Close')
st.plotly_chart(candlestick)
