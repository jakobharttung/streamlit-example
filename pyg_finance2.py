import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
from openbb import obb

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit for Finance",
    layout="wide"
)
df = pdf.DataFrame()
st.write("starting")
pyg_app = StreamlitRenderer(df)
pyg_app.explorer()

