import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np

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
# Fix Column Order and Ensure Data is Numeric
# --------------------------------------------------------------------------
required_columns = ["Open", "High", "Low", "Close", "Volume"]

# Ensure required columns exist
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"⚠️ Missing required columns: {missing_columns}")
    st.stop()

# Convert only existing columns to numeric
for col in required_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")  # Convert and coerce errors to NaN

# --------------------------------------------------------------------------
# Debugging Step 2: Show Data Types Before Cleaning
# --------------------------------------------------------------------------
st.subheader("📊 Data Types Before Cleaning")
st.write(data.dtypes)

# --------------------------------------------------------------------------
# Remove NaN, Inf, or Any Invalid Values
# --------------------------------------------------------------------------
# Replace Inf values with NaN
data.replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop rows where any required column is NaN
data.dropna(subset=required_columns, inplace=True)

# --------------------------------------------------------------------------
# Debugging Step 3: Show Cleaned Data Before Plotting
# --------------------------------------------------------------------------
st.subheader("🔍 Cleaned Data Preview (After Fixing NaNs & Infs)")
st.write(data.head())

# Final Check: Stop if DataFrame is Empty After Cleaning
if data.empty:
    st.error("⚠️ After cleaning, no valid data remains to plot.")
    st.stop()

# --------------------------------------------------------------------------
# Plot Candlestick Chart using mplfinance
# --------------------------------------------------------------------------
try:
    st.subheader("📊 Candlestick Chart")
    fig, axlist = mpf.plot(
        data,
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
