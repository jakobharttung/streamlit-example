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
# Debug: Show raw data to verify structure
# --------------------------------------------------------------------------
st.subheader("🔍 Data Preview")
st.write(data.head())  # Show first rows of raw data

# --------------------------------------------------------------------------
# Validate Data
# --------------------------------------------------------------------------
if data.empty:
    st.error("❌ No stock data found for L’Oréal (OR.PA). Please try again later.")
else:
    st.success(f"✅ Data successfully fetched from {start_date} to {end_date}.")

    # ----------------------------------------------------------------------
    # Convert Data to Numeric (Handle Edge Cases)
    # ----------------------------------------------------------------------
    required_columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    
    # Ensure only existing columns are processed
    existing_columns = [col for col in required_columns if col in data.columns]

    if not existing_columns:
        st.error("⚠️ Critical columns missing! Data might be incomplete.")
    else:
        # Convert existing columns to numeric
        for col in existing_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        # Debug: Show data types after conversion
        st.subheader("📊 Data Types After Conversion")
        st.write(data.dtypes)

        # ------------------------------------------------------------------
        # Drop rows with NaN in required columns
        # ------------------------------------------------------------------
        data.dropna(subset=["Open", "High", "Low", "Close", "Volume"], inplace=True)

        if data.empty:
            st.error("⚠️ After cleaning, no valid data remains to plot.")
        else:
            # --------------------------------------------------------------
            # Plot candlestick chart using mplfinance
            # --------------------------------------------------------------
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

            # --------------------------------------------------------------
            # Render the chart in Streamlit
            # --------------------------------------------------------------
            st.pyplot(fig)
