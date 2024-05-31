import streamlit as st
import plotly.express as px
import pandas as pd

def load_data(uploaded_file):
    data = pd.read_excel(uploaded_file)
    return data

st.title("Sunburst budget analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type='xlsx')
if uploaded_file is not None:
    data = load_data(uploaded_file)
    fig = px.sunburst(data, path=['BUSINESS UNIT (Snow)', 'Business  Capability', 'Business Sub Capability', 'Analytical Cost Nature', 'product',
                              'Competitive advantage', 'Business critical', 'AIMS OUTSOURCING LEVEL', 'Vendor'],
                  values=' Horizon 2025',
                  color='freq',
                  color_continuous_scale='rdbu_r',
                  width=960, height=600
                 )
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.show()
    
