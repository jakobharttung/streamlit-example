from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import numpy as np
import streamlit as st
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
#make this example reproducible
np.random.seed(0)

#create DataFrame with hourly index
# df = pd.DataFrame(index=pd.date_range('2020-01-06', '2020-12-27', freq='h'))

#add column to show sales by hour
# df['sales'] = np.random.randint(low=0, high=20, size=len(df.index))
# weekly_df = pd.DataFrame()
# weekly_df['sales'] = df['sales'].resample('D').sum()
# weekly_df['TS'] = weekly_df.index
# Import your data
df = pd.read_excel("timeseries.xlsx")
df.set_index('TS', inplace=True)
df_minute = pd.DataFrame()
df_minute['RAW_VALUE'] = df['RAW_VALUE'].resample('D').sum()
pyg_app = StreamlitRenderer(weekly_df)
 
pyg_app.explorer()
