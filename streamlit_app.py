import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# --------------------------------------------------------------------------
# Streamlit Title
# --------------------------------------------------------------------------
st.title("📈 L’Oréal (OR.PA) - Daily Candlestick Chart")

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

# --------------------------------------------------------------------------
# Debugging: Show raw data preview
# --------------------------------------------------------------------------
st.subheader("🔍 Raw Data Preview")
st.write(data.head())

# --------------------------------------------------------------------------
# Ensure Data is Valid
# --------------------------------------------------------------------------
if data.empty:
    st.error("❌ No stock data found for L’Oréal (OR.PA). Please try again later.")
else:
    st.success(f"✅ Data successfully fetched from {start_date} to {end_date}.")
    
    # ----------------------------------------------------------------------
    # Ensure Data Has a DateTime Index
    # ----------------------------------------------------------------------
    if not isinstance(data.index, pd.DatetimeIndex):
        st.warning("⚠️ Converting index to DateTime format.")
        data.index = pd.to_datetime(data.index)

    # ----------------------------------------------------------------------
    # Convert Required Columns to Numeric
    # ----------------------------------------------------------------------
    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    
    # Ensure only existing columns are processed
    existing_columns = [col for col in required_columns if col in data.columns]

    if len(existing_columns) < len(required_columns):
        missing_cols = list(set(required_columns) - set(existing_columns))
        st.error(f"⚠️ Missing columns: {missing_cols}. Data might be incomplete.")

    # Convert only existing columns to numeric
    for col in existing_columns:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # Debug: Show data types after conversion
    st.subheader("📊 Data Types After Conversion")
    st.write(data.dtypes)

    # ------------------------------------------------------------------
    # Drop Rows with Missing Data
    # ------------------------------------------------------------------
    data.dropna(subset=required_columns, inplace=True)

    if data.empty:
        st.error("⚠️ After cleaning, no valid data remains to plot.")
    else:
        # --------------------------------------------------------------
        # Plot Candlestick Chart using mplfinance
        # --------------------------------------------------------------
        try:
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
