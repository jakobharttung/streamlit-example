import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import numpy as np

# Function to preprocess the data
def preprocess_data(df, interval):
    # Ensure CYCLE TIME is numeric
    df['CYCLE TIME'] = pd.to_numeric(df['CYCLE TIME'], errors='coerce')
    
    # Convert END TIME to datetime
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    
    # Group by the selected interval
    if interval == 'Weekly':
        df['TIME INTERVAL'] = df['END TIME'].dt.strftime('%Y-%U')
    else:
        df['TIME INTERVAL'] = df['END TIME'].dt.strftime('%Y-%m')
    
    return df

# Function to calculate average cycle times
def calculate_cycle_times(df):
    # Calculate overall average cycle time
    overall_avg = df['CYCLE TIME'].mean()
    
    # Calculate material-level average cycle time
    material_avg = df.groupby('MATERIAL')['CYCLE TIME'].mean().reset_index()
    
    # Calculate the number of batches for each material
    material_counts = df['MATERIAL'].value_counts().reset_index()
    material_counts.columns = ['MATERIAL', 'BATCH COUNT']
    
    # Merge the averages and counts
    material_cycle_times = pd.merge(material_avg, material_counts, on='MATERIAL')
    
    return overall_avg, material_cycle_times

# Streamlit app
st.title('Manufacturing Batch Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Time Interval Toggle
    interval = st.radio("Select Time Interval", ('Monthly', 'Weekly'))
    
    # Preprocess data
    df = preprocess_data(df, interval)
    
    # Calculate cycle times
    overall_avg, material_cycle_times = calculate_cycle_times(df)
    
    # Combined Plot
    base = alt.Chart(df).encode(
        alt.X('TIME INTERVAL:O', axis=alt.Axis(title=interval + ' Interval'))
    )
    
    # Line chart for overall average cycle time
    line = base.mark_line(color='red').encode(
        alt.Y('mean(CYCLE TIME):Q', axis=alt.Axis(title='Average Cycle Time (days)'))
    )
    
    # Circle chart for material-level average cycle time
    circles = base.mark_circle().encode(
        alt.Y('CYCLE TIME:Q'),
        alt.Size('BATCH COUNT:Q'),
        alt.Color('MATERIAL:N', legend=alt.Legend(title='Material'))
    ).transform_filter(
        alt.datum['CYCLE TIME'] == material_cycle_times['CYCLE TIME']
    )
    
    # Combine the charts
    combined_chart = alt.layer(line, circles).resolve_scale(y='shared')
    
    st.altair_chart(combined_chart, use_container_width=True)
    
    # Material Selector and Boxplot
    selected_material = st.selectbox('Select a Material', df['MATERIAL'].unique())
    
    # Filter data for the selected material
    material_data = df[df['MATERIAL'] == selected_material]
    
    # Boxplot for cycle time distribution
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        alt.X('TIME INTERVAL:O', axis=alt.Axis(title=interval + ' Interval')),
        alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Cycle Time (days)'))
    )
    
    st.altair_chart(boxplot, use_container_width=True)
