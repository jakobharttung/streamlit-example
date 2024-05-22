import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Function to load data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        # Ensure CYCLE TIME is numeric
        df['CYCLE TIME'] = pd.to_numeric(df['CYCLE TIME'], errors='coerce')
        return df
    else:
        return pd.DataFrame()

# Function to generate interval-based analysis
def interval_analysis(df, interval):
    # Convert END TIME to datetime
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    
    # Set the index to END TIME for resampling
    df.set_index('END TIME', inplace=True)
    
    # Resample and calculate means
    if interval == 'Monthly':
        resampled = df.resample('M')
    else: # Weekly
        resampled = df.resample('W')
    
    overall_avg = resampled['CYCLE TIME'].mean()
    material_avg = resampled.groupby('MATERIAL')['CYCLE TIME'].mean()
    batch_count = resampled['MATERIAL'].value_counts()
    
    return overall_avg, material_avg, batch_count

# Streamlit app
st.title('Manufacturing Batch Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader('Upload your Excel file', type=['xlsx'])

# Load data
df = load_data(uploaded_file)

# Toggle for time interval
interval = st.radio('Select Time Interval', ('Monthly', 'Weekly'))

# Generate analysis based on selected interval
if not df.empty:
    overall_avg, material_avg, batch_count = interval_analysis(df, interval)
    
    # Altair chart
    base = alt.Chart(df.reset_index()).encode(
        alt.X('END TIME', title='Batch Date')
    )
    
    # Overall average cycle time line
    line = base.mark_line().encode(
        alt.Y('average(CYCLE TIME)', title='Average Cycle Time (days)')
    )
    
    # Material average cycle time circles
    points = base.mark_circle().encode(
        alt.Y('average(CYCLE TIME)', title='Average Cycle Time (days)'),
        alt.Size('count(MATERIAL)'),
        alt.Color('MATERIAL', legend=alt.Legend(title='Material'))
    )
    
    # Combine charts
    chart = alt.layer(line, points).resolve_scale(y='shared')
    
    st.altair_chart(chart, use_container_width=True)
    
    # Material selector for boxplot
    selected_material = st.selectbox('Select a Material', df['MATERIAL'].unique())
    
    # Filter data for selected material
    material_data = df[df['MATERIAL'] == selected_material]
    
    # Boxplot for cycle time distribution of selected material
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        alt.X('END TIME', title=f'{interval} Interval'),
        alt.Y('CYCLE TIME', title='Cycle Time (days)')
    )
    
    st.altair_chart(boxplot, use_container_width=True)
