import streamlit as st
import pandas as pd
import altair as alt

# Function to calculate overall average cycle time
def calculate_overall_avg(df, interval):
    df['DATE'] = pd.to_datetime(df['DATE'])
    if interval == 'W':
        df['INTERVAL'] = df['DATE'].dt.strftime('%U')
    else:
        df['INTERVAL'] = df['DATE'].dt.strftime('%Y-%m')
    return df.groupby('INTERVAL')['CYCLE TIME'].mean().reset_index(name='AVG_CYCLE_TIME')

# Function to calculate material level average cycle time and batch count
def calculate_material_avg(df, interval):
    df['DATE'] = pd.to_datetime(df['DATE'])
    if interval == 'W':
        df['INTERVAL'] = df['DATE'].dt.strftime('%U')
    else:
        df['INTERVAL'] = df['DATE'].dt.strftime('%Y-%m')
    return df.groupby(['INTERVAL', 'MATERIAL'])['CYCLE TIME'].agg(['mean', 'count']).reset_index()

# Streamlit app
st.title('Manufacturing Batch Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Convert 'CYCLE TIME' to numeric
    df['CYCLE TIME'] = pd.to_numeric(df['CYCLE TIME'], errors='coerce')
    
    # Toggle for time intervals
    interval = st.radio("Select the time interval", ('Monthly', 'Weekly'))
    interval_code = 'M' if interval == 'Monthly' else 'W'
    
    # Calculate overall and material level cycle times
    overall_avg = calculate_overall_avg(df, interval_code)
    material_avg = calculate_material_avg(df, interval_code)
    
    # Create the plot with two layers
    base = alt.Chart(overall_avg).encode(
        alt.X('INTERVAL:N', title='Interval')
    )
    
    line = base.mark_line(color='blue').encode(
        alt.Y('AVG_CYCLE_TIME:Q', title='Average Cycle Time')
    )
    
    points = alt.Chart(material_avg).mark_circle().encode(
        alt.X('INTERVAL:N', title='Interval'),
        alt.Y('mean:Q', title='Average Cycle Time'),
        alt.Size('count:Q', title='Number of Batches'),
        alt.Color('MATERIAL:N', legend=alt.Legend(title='Material'))
    )
    
    st.altair_chart(line + points, use_container_width=True)
    
    # Material selector and boxplot
    material_list = df['MATERIAL'].unique()
    selected_material = st.selectbox("Select a material", material_list)
    
    material_df = df[df['MATERIAL'] == selected_material]
    material_df['INTERVAL'] = material_df['DATE'].dt.strftime('%U' if interval_code == 'W' else '%Y-%m')
    
    boxplot = alt.Chart(material_df).mark_boxplot().encode(
        alt.X('INTERVAL:N', title='Interval'),
        alt.Y('CYCLE TIME:Q', title='Cycle Time', scale=alt.Scale(zero=False)),
        alt.Color('MATERIAL:N', legend=alt.Legend(title='Material'))
    )
    
    st.altair_chart(boxplot, use_container_width=True)
