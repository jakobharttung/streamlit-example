import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
import openbb as obb

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit for Finance",
    layout="wide"
)
obb.account.login(pat="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoX3Rva2VuIjoibTdvT2ZYY3VzWkV1N2sxNG56QXQ0eWJQQlZDTDZFSHExRk5CaUx3dSIsImV4cCI6MTc0ODA3Mjk5N30.MdAYRToDt-37uJScSgnNP8yPsvjhxCereq8caBsTz2M")
# Import your data
output = obb.equity.price.historical("AAPL")
df = output.to_dataframe()
pyg_app = StreamlitRenderer(df)
pyg_app.explorer()

