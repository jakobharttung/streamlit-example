from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
# Import your data
df = pd.read_excel("timeseries.xlsx")
df_minute = df.resample('min').sum()
pyg_app = StreamlitRenderer(df_minute)
 
pyg_app.explorer()
