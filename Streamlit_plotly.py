import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Set up the Streamlit app
st.title('Stock Price Viewer')

# Create an input field for the comma-separated list of ticker symbols
tickers = st.text_input('Enter Comma-Separated Stock Ticker Symbols', 'AAPL, MSFT, GOOGL')

# Split the tickers into a list
ticker_list = [ticker.strip() for ticker in tickers.split(',')]

# Retrieve stock data for each ticker
if ticker_list:
    fig = go.Figure()
    
    for ticker in ticker_list:
        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(period='max')
        
        # Check if the data is not empty
        if not hist.empty:
            # Add a trace for each ticker
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=hist['Close'],
                mode='lines',
                name=ticker
            ))
    
    # Add range slider and range selector
    fig.update_layout(
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
        )
    )
    
    st.plotly_chart(fig)
else:
    st.write('Please enter at least one ticker symbol.')

# Run the app using the command: streamlit run stock_price_viewer.py
