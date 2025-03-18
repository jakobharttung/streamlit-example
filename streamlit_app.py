import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# --------------------------------------------------------------------------
# Streamlit Title
# --------------------------------------------------------------------------
st.title("L’Oréal (OR.PA) - Daily Candlestick Chart")

# --------------------------------------------------------------------------
# Define the date range (past year)
# --------------------------------------------------------------------------
end_date = date.today()
start_date = end_date - relativedelta(years=1)

# --------------------------------------------------------------------------
# Download data from Yahoo Finance
# --------------------------------------------------------------------------
with st.spinner("Fetching L’Oréal (OR.PA) data..."):
    data = yf.download("OR.PA", start=start_date, end=end_date, interval="1d")

if data.empty:
    st.error("No data found for L’Oréal (OR.PA). Please try again later.")
else:
    # Display a success message showing the date range
    st.success(f"Data fetched from {start_date} to {end_date}.")
    
    # ----------------------------------------------------------------------
    # Ensure all critical columns are numeric
    # ----------------------------------------------------------------------
    for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    
    # ----------------------------------------------------------------------
    # Drop any rows with NaN in the critical columns
    # ----------------------------------------------------------------------
    data.dropna(subset=["Open", "High", "Low", "Close", "Volume"], inplace=True)
    
    if data.empty:
        st.error("After cleaning, no valid data remains to plot.")
    else:
        # ------------------------------------------------------------------
        # Plot candlestick chart using mplfinance
        # ------------------------------------------------------------------
        fig, axlist = mpf.plot(
            data,
            type="candle",
            style="yahoo",
            title=f"L’Oréal (OR.PA) from {start_date} to {end_date}",
            volume=True,
            mav=(20, 50),  # Plot 20-day and 50-day moving averages
            figsize=(10, 6),
            returnfig=True
        )
        
        # ------------------------------------------------------------------
        # Render the chart in Streamlit
        # ------------------------------------------------------------------
        st.pyplot(fig)
