import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# Function to calculate average cycle time
def calculate_average_cycle_time(df, interval):
    df['Date'] = pd.to_datetime(df['END TIME'])
    df.set_index('Date', inplace=True)
    if interval == 'Monthly':
        resampled = df.resample('M').mean()
    else:
        resampled = df.resample('W').mean()
    return resampled

# Function to prepare data for the plot
def prepare_data_for_plot(df, interval):
    df['Date'] = pd.to_datetime(df['END TIME'])
    df.set_index('Date', inplace=True)
    if interval == 'Monthly':
        df['Interval'] = df.index.to_period('M')
    else:
        df['Interval'] = df.index.to_period('W')
    overall_avg = df['CYCLE TIME'].mean()
    material_avg = df.groupby(['MATERIAL', 'Interval'])['CYCLE TIME'].mean().reset_index()
    material_count = df.groupby(['MATERIAL', 'Interval']).size().reset_index(name='Counts')
    return overall_avg, material_avg, material_count

# Streamlit app
st.title('Manufacturing Batch Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type='xlsx')
if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Toggle for time intervals
    interval = st.radio("Select Time Interval", ('Monthly', 'Weekly'))

    # Calculate overall and material level cycle time
    overall_avg, material_avg, material_count = prepare_data_for_plot(df, interval)

    # Plot with two layers
    base = alt.Chart(material_avg).encode(
        alt.X('Interval:N', title='Time Interval'),
        alt.Y('CYCLE TIME:Q', title='Average Cycle Time (days)')
    )

    line = base.mark_line().encode(
        alt.Y('average(CYCLE TIME):Q', title='Overall Average Cycle Time')
    )

    points = base.mark_circle().encode(
        alt.Size('Counts:Q'),
        alt.Color('MATERIAL:N', legend=alt.Legend(title="Material"))
    )

    st.altair_chart(line + points, use_container_width=True)

    # Selector for materials
    selected_material = st.selectbox('Select a Material', df['MATERIAL'].unique())

    # Boxplot for selected material
    material_data = df[df['MATERIAL'] == selected_material]
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        alt.X('Interval:N', title='Time Interval'),
        alt.Y('CYCLE TIME:Q', title='Cycle Time (days)')
    )

    st.altair_chart(boxplot, use_container_width=True)
