import streamlit as st
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

# Define the tickers
tickers = ['MSFT', 'GOOG', 'TSLA', 'NVDA', 'SAN.PA', 'OR.PA']

# Get 10 years of market close data
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=3652)).strftime('%Y-%m-%d')

# Download the data
data = yf.download(tickers, start=start_date, end=end_date)['Close']
st.write(data)
# Reset index to get 'Date' column
data.reset_index(inplace=True)

# Streamlit app layout
st.title('Stock Performance Analysis')

# Line chart with range selection
st.subheader('Stock Closing Prices Over 10 Years')
fig = px.line(data, x='Date', y=tickers)
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig)

# Dropdown for candlestick chart
st.subheader('Detailed View')
selected_ticker = st.selectbox('Select a ticker for detailed view:', tickers)

# Get data for the selected ticker
ticker_data = yf.download(selected_ticker, start=start_date, end=end_date)

# Candlestick chart
fig_candle = px.line(ticker_data, x=ticker_data.index, y='Close')
st.plotly_chart(fig_candle)



