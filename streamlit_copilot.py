import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Function to preprocess the data
def preprocess_data(df, interval):
    # Convert 'END TIME' to datetime and extract the desired time interval
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    if interval == 'Weekly':
        df['TIME INTERVAL'] = df['END TIME'].dt.to_period('W').apply(lambda r: r.start_time)
    else:
        df['TIME INTERVAL'] = df['END TIME'].dt.to_period('M').apply(lambda r: r.start_time)
    
    # Ensure 'CYCLE TIME' is numeric
    df['CYCLE TIME'] = pd.to_numeric(df['CYCLE TIME'], errors='coerce')
    return df

# Function to calculate average cycle times
def calculate_cycle_times(df, interval):
    # Group by 'TIME INTERVAL' and 'MATERIAL' and calculate the mean 'CYCLE TIME'
    material_cycle_time = df.groupby(['TIME INTERVAL', 'MATERIAL'])['CYCLE TIME'].mean().reset_index()
    
    # Calculate the overall average 'CYCLE TIME' for each 'TIME INTERVAL'
    overall_cycle_time = df.groupby('TIME INTERVAL')['CYCLE TIME'].mean().reset_index()
    
    # Count the number of batches for each 'MATERIAL' and 'TIME INTERVAL'
    batch_counts = df.groupby(['TIME INTERVAL', 'MATERIAL']).size().reset_index(name='BATCH COUNT')
    
    # Merge the dataframes
    material_cycle_time = pd.merge(material_cycle_time, batch_counts, on=['TIME INTERVAL', 'MATERIAL'])
    return overall_cycle_time, material_cycle_time

# Streamlit app
st.title('Batch Cycle Time Analysis App')

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Time Interval Toggle
    interval = st.radio("Select Time Interval", ('Monthly', 'Weekly'))
    
    # Preprocess the data
    df = preprocess_data(df, interval)
    
    # Calculate cycle times
    overall_cycle_time, material_cycle_time = calculate_cycle_times(df, interval)
    
    # Create the overall average cycle time line chart
    line_chart = alt.Chart(overall_cycle_time).mark_line().encode(
        x=alt.X('TIME INTERVAL:T', title='Time Interval'),
        y=alt.Y('CYCLE TIME:Q', title='Overall Average Cycle Time (days)')
    )
    
    # Create the material average cycle time circle chart
    circle_chart = alt.Chart(material_cycle_time).mark_circle().encode(
        x=alt.X('TIME INTERVAL:T', title='Time Interval'),
        y=alt.Y('CYCLE TIME:Q', title='Material Average Cycle Time (days)'),
        size=alt.Size('BATCH COUNT:Q', title='Number of Batches'),
        color=alt.Color('MATERIAL:N', legend=alt.Legend(title='Material'))
    )
    
    # Combine the charts
    combined_chart = alt.layer(line_chart, circle_chart).resolve_scale(y='shared')
    st.altair_chart(combined_chart, use_container_width=True)
    
    # Material selector for boxplot
    material_selector = st.selectbox('Select a Material for Boxplot', df['MATERIAL'].unique())
    
    # Filter data for the selected material
    material_data = df[df['MATERIAL'] == material_selector]
    
    # Create the boxplot
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        x=alt.X('TIME INTERVAL:T', title='Time Interval'),
        y=alt.Y('CYCLE TIME:Q', title='Cycle Time (days)')
    )
    st.altair_chart(boxplot, use_container_width=True)
