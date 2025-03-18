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
    st.stop()  # Stop execution here

# --------------------------------------------------------------------------
# Debugging Step 2: Check Data Types Before Processing
# --------------------------------------------------------------------------
st.subheader("📊 Data Types Before Conversion")
st.write(data.dtypes)

# Ensure Data Has a DateTime Index
if not isinstance(data.index, pd.DatetimeIndex):
    st.warning("⚠️ Converting index to DateTime format.")
    data.index = pd.to_datetime(data.index)

# --------------------------------------------------------------------------
# Convert Required Columns to Numeric
# --------------------------------------------------------------------------
required_columns = ["Open", "High", "Low", "Close", "Volume"]

# Ensure required columns exist
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"⚠️ Missing columns: {missing_columns}. Data might be incomplete.")
    st.stop()

# Convert only valid columns
for col in required_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# --------------------------------------------------------------------------
# Debugging Step 3: Show Data Types After Conversion
# --------------------------------------------------------------------------
st.subheader("📊 Data Types After Conversion")
st.write(data.dtypes)

# Drop rows with missing values
data.dropna(subset=required_columns, inplace=True)

if data.empty:
    st.error("⚠️ After cleaning, no valid data remains to plot.")
    st.stop()

# --------------------------------------------------------------------------
# Debugging Step 4: Show Cleaned Data Before Plotting
# --------------------------------------------------------------------------
st.subheader("🔍 Cleaned Data Preview")
st.write(data.head())

# --------------------------------------------------------------------------
# Plot Candlestick Chart using mplfinance
# ----------------------------------------------------------
