import streamlit as st
import yfinance as yf
import mplfinance as mpf

def load_data(ticker):
    stock_data = yf.Ticker(ticker)
    data = stock_data.history(period="5y")
    return data

st.title("Stock Price Visualization")

ticker = st.text_input("Enter stock ticker (e.g., AAPL, GOOGL):", "AAPL")

data = load_data(ticker)

if not data.empty:
    st.write(f"Displaying data for {ticker}")

    st.write(data.tail())

    fig, axlist = mpf.plot(data, type='candle', volume=True, returnfig=True)
    st.pyplot(fig)
else:
    st.write("Invalid ticker or no data available.")

