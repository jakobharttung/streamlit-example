import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Set up the Streamlit app
st.title('Stock Price Viewer')

# Create an input field for the ticker symbol
ticker = st.text_input('Enter Stock Ticker Symbol', 'AAPL')

# Create a select box for interval
interval = st.selectbox('Select Interval', [
    '1m', '2m', '5m', '15m', '30m', '60m', '90m',
    '1h', '1d', '5d', '1wk', '1mo', '3mo'
])
# Retrieve stock data
if ticker:
    stock_data = yf.Ticker(ticker)
    hist = stock_data.history(period='max', interval=interval)

    # Check if the data is not empty
    if not hist.empty:
        # Plot the time series data with Plotly
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist['Close'],
            mode='lines',
            name='Close Price'
        ))

        # Add range slider and range selector
        fig.update_layout(
            title=f'{ticker} Stock Price',
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
        st.write('No data found for the selected ticker.')
        
# Run the app using the command: streamlit run stock_price_viewer.py
