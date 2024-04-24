import streamlit as st
import pandas as pd

# Streamlit app
st.title('Material Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file, engine='openpyxl'))
    st.write(data)
else:
    st.write("Please upload an Excel file to proceed.")
