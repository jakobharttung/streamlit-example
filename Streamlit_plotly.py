import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Set up the Streamlit app
st.title('Stock Price and Market Capitalization Viewer')

# Create an input field for the comma-separated list of ticker symbols
tickers = st.text_input('Enter Comma-Separated Stock Ticker Symbols', 'AAPL, MSFT, GOOGL')

# Split the tickers into a list
ticker_list = [ticker.strip() for ticker in tickers.split(',')]

# Retrieve and plot stock price data for each ticker
if ticker_list:
    price_fig = go.Figure()
    market_cap_fig = go.Figure()
    
    for ticker in ticker_list:
        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(period='max')
        
        # Check if the data is not empty
        if not hist.empty:
            # Add a trace for each ticker in the price chart
            price_fig.add_trace(go.Scatter(
                x=hist.index,
                y=hist['Close'],
                mode='lines',
                name=ticker
            ))
            
            # Calculate market capitalization and add a trace for each ticker in the market cap chart
            shares_outstanding = stock_data.info.get('sharesOutstanding')
            if shares_outstanding:
                hist['Market Cap'] = hist['Close'] * shares_outstanding
                market_cap_fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=hist['Market Cap'],
                    mode='lines',
                    name=ticker
                ))
    
    # Add range slider and range selector to the price chart
    price_fig.update_layout(
        title='Stock Prices',
        xaxis_title='Date',
        yaxis_title='Close Price',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=3, label='3m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False  # Allow the range to dynamically adjust
        )
    )
    
    # Add range slider and range selector to the market cap chart
    market_cap_fig.update_layout(
        title='Market Capitalization',
        xaxis_title='Date',
        yaxis_title='Market Cap',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=3, label='3m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False  # Allow the range to dynamically adjust
        )
    )
    
    st.plotly_chart(price_fig)
    st.plotly_chart(market_cap_fig)
    
    # Add dropdown to select a ticker and resampling interval
    selected_ticker = st.selectbox('Select Ticker for Candlestick Chart', ticker_list)
    resample_interval = st.selectbox('Select Resampling Interval', ['D', 'W', 'M'])
    
    if selected_ticker:
        selected_stock_data = yf.Ticker(selected_ticker)
        selected_hist = selected_stock_data.history(period='max')
        
        if not selected_hist.empty:
            # Ensure the index is a DateTimeIndex and handle resampling
            selected_hist.index = pd.to_datetime(selected_hist.index)
            
            if resample_interval != 'D':
                resampled_hist = selected_hist.resample(resample_interval).agg({
                    'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last',
                    'Volume': 'sum'
                }).dropna()
            else:
                resampled_hist = selected_hist
            
            # Create a candlestick chart
            candlestick_fig = go.Figure(data=[go.Candlestick(
                x=resampled_hist.index,
                open=resampled_hist['Open'],
                high=resampled_hist['High'],
                low=resampled_hist['Low'],
                close=resampled_hist['Close'],
                name=selected_ticker
            )])
            
            candlestick_fig.update_layout(
                title=f'{selected_ticker} Candlestick Chart',
                xaxis_title='Date',
                yaxis_title='Price',
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label='1m', step='month', stepmode='backward'),
                            dict(count=3, label='3m', step='month', stepmode='backward'),
                            dict(count=6, label='6m', step='month', stepmode='backward'),
                            dict(count=1, label='YTD', step='year', stepmode='todate'),
                            dict(count=1, label='1y', step='year', stepmode='backward'),
                            dict(step='all')
                        ])
                    ),
                    rangeslider=dict(
                        visible=True
                    ),
                    type='date'
                ),
                yaxis=dict(
                    autorange=True,
                    fixedrange=False  # Allow the range to dynamically adjust
                )
            )
            
            st.plotly_chart(candlestick_fig)
else:
    st.write('Please enter at least one ticker symbol.')

# Run the app using the command: streamlit run stock_price_viewer.py
