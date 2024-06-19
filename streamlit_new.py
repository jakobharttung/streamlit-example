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

# Add buttons for standard yfinance intervals
intervals = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
interval_dict = {'1d': '1 day', '5d': '5 days', '1mo': '1 month', '3mo': '3 months', '6mo': '6 months', '1y': '1 year', '2y': '2 years', '5y': '5 years', '10y': '10 years', 'ytd': 'year to date', 'max': 'maximum'}

# Function to update the chart based on the selected interval
def update_chart(interval):
    start_date = end_date - timedelta(days=interval_dict[interval])
    updated_data = yf.download(tickers, start=start_date, end=end_date)['Close']
    fig = px.line(updated_data, x=updated_data.index, y=tickers)
    st.plotly_chart(fig)

# Display buttons and link them to the update_chart function
for interval in intervals:
    if st.button(interval):
        update_chart(interval)

# Initial chart display
fig = px.line(data, x=data.index, y=tickers)
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig)

# Dropdown for candlestick chart
st.subheader('Candlestick Chart')
selected_ticker = st.selectbox('Select a ticker', tickers)
ticker_data = yf.download(selected_ticker, period='1d', interval='1m')
candlestick = px.line(ticker_data, x=ticker_data.index, y='Close')
st.plotly_chart(candlestick)
