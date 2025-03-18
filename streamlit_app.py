import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# --------------------------------------------------------------------------
# Streamlit Title
# --------------------------------------------------------------------------
st.title("📈 L’Oréal (OR.PA) - Candlestick Chart")

# --------------------------------------------------------------------------
# Define the date range (past year)
# --------------------------------------------------------------------------
end_date = date.today()
start_date = end_date - relativedelta(years=1)

# --------------------------------------------------------------------------
# Download data from Yahoo Finance
# --------------------------------------------------------------------------
st.subheader("Fetching Data from Yahoo Finance...")

with st.spinner("Fetching L’Oréal (OR.PA) stock data..."):
    data = yf.download("OR.PA", start=start_date, end=end_date, interval="1d")

# --------------------------------------------------------------------------
# Debugging Step 1: Show Raw Data
# --------------------------------------------------------------------------
st.subheader("🔍 Raw Data Preview")
st.write(data.head())

# --------------------------------------------------------------------------
# Validate Data
# --------------------------------------------------------------------------
if data.empty:
    st.error("❌ No stock data found for L’Oréal (OR.PA).")
    st.stop()

# --------------------------------------------------------------------------
# Ensure Data Has a Proper DateTime Index
# --------------------------------------------------------------------------
if not isinstance(data.index, pd.DatetimeIndex):
    st.warning("⚠️ Converting index to DateTime format.")
    data.index = pd.to_datetime(data.index)

# --------------------------------------------------------------------------
# Fix Column Order for mplfinance
# --------------------------------------------------------------------------
required_columns = ["Open", "High", "Low", "Close", "Volume"]

# Ensure only required columns exist and are in the correct order
if not all(col in data.columns for col in required_columns):
    st.error(f"⚠️ Missing required columns: {set(required_columns) - set(data.columns)}")
    st.stop()

# Reconstruct the DataFrame explicitly for mplfinance
ohlc = data[required_columns].copy()  # Ensure it's a new DataFrame

# --------------------------------------------------------------------------
# Debugging Step 2: Show Cleaned Data Before Plotting
# --------------------------------------------------------------------------
st.subheader("🔍 Cleaned Data Preview")
st.write(ohlc.head())

# --------------------------------------------------------------------------
# Plot Candlestick Chart using mplfinance
# --------------------------------------------------------------------------
try:
    st.subheader("📊 Candlestick Chart")
    fig, axlist = mpf.plot(
        ohlc,  # Use the cleaned DataFrame
        type="candle",
        style="yahoo",
        title=f"📊 L’Oréal (OR.PA) from {start_date} to {end_date}",
        volume=True,
        mav=(20, 50),  # Moving Averages (20-day, 50-day)
        figsize=(10, 6),
        returnfig=True
    )
    st.pyplot(fig)
except Exception as e:
    st.error(f"❌ mplfinance plotting error: {e}")
