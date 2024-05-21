from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
# Import your data
df = pd.read_excel("Plant cycle time Data.xlsx")
df['graphmonth' = df['END TIME'].dt.strftime('%Y-%m') 
pyg_app = StreamlitRenderer(df)
 
pyg_app.explorer()
