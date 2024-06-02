import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta

# Define stock tickers
stock_tickers = ["MSFT", "GOOG", "TSLA", "NVDA", "SAN.PA", "OR.PA"]

# Set the start and end date for data fetching (10 years of data)
end_date = date.today()
start_date = end_date - timedelta(days=365*10)

# Fetch stock data
def get_stock_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# Fetch data for all stock tickers
data = {ticker: get_stock_data(ticker, start_date, end_date) for ticker in stock_tickers}

# Plot line chart for market close data
st.title("Stock Performance Analysis")
st.subheader("Market Close Data (Last 10 Years)")

# Create a line chart for multiple stock tickers
fig = go.Figure()
for ticker in stock_tickers:
    fig.add_trace(go.Scatter(x=data[ticker].index, y=data[ticker]['Close'], mode='lines', name=ticker))

# Adding range sliders and buttons
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Market Close Price',
    xaxis_rangeslider_visible=True,
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(count=10, label='10y', step='year', stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(visible=True)
    ),
    template='plotly_dark'
)
st.plotly_chart(fig)

# Dropdown to select a stock ticker for candlestick chart
selected_ticker = st.selectbox("Select a stock ticker for candlestick chart", stock_tickers)

# Fetch selected stock data
selected_data = data[selected_ticker]

# Plot candlestick chart for selected stock ticker
st.subheader(f"Candlestick Chart for {selected_ticker}")
candlestick_fig = go.Figure(data=[go.Candlestick(
    x=selected_data.index,
    open=selected_data['Open'],
    high=selected_data['High'],
    low=selected_data['Low'],
    close=selected_data['Close']
)])
candlestick_fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Price',
    template='plotly_dark'
)
st.plotly_chart(candlestick_fig)

