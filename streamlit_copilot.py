import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import numpy as np

# Function to preprocess the data
def preprocess_data(df, interval):
    # Convert END TIME to datetime
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    
    # Set the interval for analysis
    if interval == 'Monthly':
        df['TIME INTERVAL'] = df['END TIME'].dt.to_period('M')
    else:
        df['TIME INTERVAL'] = df['END TIME'].dt.to_period('W')
    
    # Group by the interval and MATERIAL, then calculate the average CYCLE TIME
    material_cycle_time = df.groupby(['MATERIAL', 'TIME INTERVAL']).agg({'CYCLE TIME': 'mean', 'MATERIAL': 'size'}).rename(columns={'MATERIAL': 'BATCH COUNT'})
    
    # Calculate the overall average CYCLE TIME
    overall_cycle_time = df.groupby('TIME INTERVAL').agg({'CYCLE TIME': 'mean'}).rename(columns={'CYCLE TIME': 'OVERALL CYCLE TIME'})
    
    return material_cycle_time.reset_index(), overall_cycle_time.reset_index()

# Function to create the combined plot
def create_combined_plot(material_cycle_time, overall_cycle_time, interval):
    # Base chart for overall average cycle time
    line_chart = alt.Chart(overall_cycle_time).mark_line(color='red').encode(
        alt.X('TIME INTERVAL:N', title='Time Interval'),
        alt.Y('OVERALL CYCLE TIME:Q', title='Average Cycle Time (days)')
    )
    
    # Chart for each material's average cycle time
    circle_chart = alt.Chart(material_cycle_time).mark_circle().encode(
        alt.X('TIME INTERVAL:N', title='Time Interval'),
        alt.Y('CYCLE TIME:Q', title='Average Cycle Time (days)'),
        alt.Size('BATCH COUNT:Q', title='Number of Batches'),
        alt.Color('MATERIAL:N', legend=alt.Legend(title='Material'))
    )
    
    # Combine the charts
    combined_chart = alt.layer(line_chart, circle_chart).resolve_scale(y='shared')
    
    return combined_chart

# Function to create the boxplot for a selected material
def create_boxplot(df, material, interval):
    # Filter the data for the selected material
    material_df = df[df['MATERIAL'] == material]
    
    # Create the boxplot
    boxplot = alt.Chart(material_df).mark_boxplot().encode(
        alt.X('TIME INTERVAL:N', title='Time Interval'),
        alt.Y('CYCLE TIME:Q', title='Cycle Time (days)')
    )
    
    return boxplot

# Streamlit app
st.title('Manufacturing Batch Cycle Times Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Ensure all-caps column names
    df.columns = map(str.upper, df.columns)
    
    # Toggle for time intervals
    interval = st.radio("Select the time interval for analysis:", ('Monthly', 'Weekly'))
    
    # Preprocess the data
    material_cycle_time, overall_cycle_time = preprocess_data(df, interval)
    
    # Create and display the combined plot
    st.altair_chart(create_combined_plot(material_cycle_time, overall_cycle_time, interval), use_container_width=True)
    
    # Material selector
    material = st.selectbox("Select a material for detailed analysis:", df['MATERIAL'].unique())
    
    # Create and display the boxplot for the selected material
    st.altair_chart(create_boxplot(df, material, interval), use_container_width=True)
