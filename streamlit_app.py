import streamlit as st
import yfinance as yf
import mplfinance as mpf
from datetime import date
from dateutil.relativedelta import relativedelta

# ----------------------------------------------------
# Streamlit App Title
# ----------------------------------------------------
st.title("L’Oréal (OR.PA) - Daily Candlestick Chart")

# ----------------------------------------------------
# Set the date range (past 1 year)
# ----------------------------------------------------
end_date = date.today()
start_date = end_date - relativedelta(years=1)

# ----------------------------------------------------
# Fetch data from Yahoo Finance
# ----------------------------------------------------
with st.spinner("Fetching data..."):
    data = yf.download("OR.PA", start=start_date, end=end_date, interval="1d")

# ----------------------------------------------------
# Check if data is retrieved successfully
# ----------------------------------------------------
if data.empty:
    st.error("No data found for L’Oréal (OR.PA). Please try again later.")
else:
    st.success(f"Data fetched from {start_date} to {end_date}.")
    
    # ----------------------------------------------------
    # Plot the Candlestick Chart using mplfinance
    # ----------------------------------------------------
    fig, axlist = mpf.plot(
        data,
        type="candle",
        style="yahoo",
        title=f"L’Oréal (OR.PA) - {start_date} to {end_date}",
        volume=True,
        mav=(20, 50),  # Moving averages: 20-day & 50-day
        figsize=(10, 6),
        returnfig=True
    )
    
    # ----------------------------------------------------
    # Display the chart in Streamlit
    # ----------------------------------------------------
    st.pyplot(fig)
