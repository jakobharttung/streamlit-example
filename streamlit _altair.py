import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# Set up the Streamlit app
st.title('Stock Price and Market Capitalization Viewer')

# Create an input field for the comma-separated list of ticker symbols
tickers = st.text_input('Enter Comma-Separated Stock Ticker Symbols', 'AAPL, MSFT, GOOGL')

# Split the tickers into a list
ticker_list = [ticker.strip() for ticker in tickers.split(',')]

# Date range input
start_date = st.date_input('Start date', pd.to_datetime('2020-01-01'))
end_date = st.date_input('End date', pd.to_datetime('today'))

# Retrieve and plot stock price data for each ticker
if ticker_list:
    price_data = []
    market_cap_data = []
    
    for ticker in ticker_list:
        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(start=start_date, end=end_date)
        
        # Check if the data is not empty
        if not hist.empty:
            hist['Ticker'] = ticker
            price_data.append(hist[['Close', 'Ticker']])
            
            shares_outstanding = stock_data.info.get('sharesOutstanding')
            if shares_outstanding:
                hist['Market Cap'] = hist['Close'] * shares_outstanding
                market_cap_data.append(hist[['Market Cap', 'Ticker']])
    
    if price_data:
        price_df = pd.concat(price_data)
        
        # Create an Altair line chart for stock prices
        price_chart = alt.Chart(price_df.reset_index()).mark_line().encode(
            x='Date:T',
            y='Close:Q',
            color='Ticker:N',
            tooltip=['Date:T', 'Close:Q', 'Ticker:N']
        ).interactive().properties(
            title='Stock Prices'
        )
        
        st.altair_chart(price_chart, use_container_width=True)
    
    if market_cap_data:
        market_cap_df = pd.concat(market_cap_data)
        
        # Create an Altair line chart for market capitalization
        market_cap_chart = alt.Chart(market_cap_df.reset_index()).mark_line().encode(
            x='Date:T',
            y='Market Cap:Q',
            color='Ticker:N',
            tooltip=['Date:T', 'Market Cap:Q', 'Ticker:N']
        ).interactive().properties(
            title='Market Capitalization'
        )
        
        st.altair_chart(market_cap_chart, use_container_width=True)
    
    # Add dropdown to select a ticker and resampling interval
    selected_ticker = st.selectbox('Select Ticker for Candlestick Chart', ticker_list)
    resample_interval = st.selectbox('Select Resampling Interval', ['D', 'W', 'M'])
    
    if selected_ticker:
        selected_stock_data = yf.Ticker(selected_ticker)
        selected_hist = selected_stock_data.history(start=start_date, end=end_date)
        
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
            
            # Create a candlestick chart with Altair
            candlestick_df = resampled_hist.reset_index().melt(
                id_vars=['Date'], value_vars=['Open', 'High', 'Low', 'Close'], var_name='Type', value_name='Price'
            )
            
            candlestick_chart = alt.Chart(candlestick_df).mark_line().encode(
                x='Date:T',
                y='Price:Q',
                color='Type:N',
                tooltip=['Date:T', 'Type:N', 'Price:Q']
            ).interactive().properties(
                title=f'{selected_ticker} Candlestick Chart'
            )
            
            st.altair_chart(candlestick_chart, use_container_width=True)
else:
    st.write('Please enter at least one ticker symbol.')

# Run the app using the command: streamlit run stock_price_viewer.py
