import streamlit as st
import pandas as pd
import altair as alt

# Function to preprocess the data
def preprocess_data(uploaded_file, interval):
    # Read the Excel file
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    # Convert 'END TIME' to datetime
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    # Create a column for the interval based on the 'END TIME'
    if interval == 'Monthly':
        df['Interval'] = df['END TIME'].dt.strftime('%Y-%m')
    else:
        df['Interval'] = df['END TIME'].dt.strftime('%Y-%U')
    return df

# Function to generate the plot
def generate_plot(df, interval):
    # Group by the selected interval and calculate the average cycle time for each material
    material_avg = df.groupby(['MATERIAL', 'Interval'])['CYCLE TIME'].mean().reset_index()
    # Calculate the count of batches for each material in the given interval
    material_count = df.groupby(['MATERIAL', 'Interval']).size().reset_index(name='Batch Count')
    # Merge the count data with the average cycle time data
    material_avg = pd.merge(material_avg, material_count, on=['MATERIAL', 'Interval'])
    
    # Calculate the overall average cycle time per interval
    overall_avg = df.groupby('Interval')['CYCLE TIME'].mean().reset_index()
    
    # Create the base chart for material averages
    points = alt.Chart(material_avg).mark_circle().encode(
        x=alt.X('Interval:O', axis=alt.Axis(title='Interval')),
        y=alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Average Cycle Time (days)')),
        size=alt.Size('Batch Count:Q', title='Number of Batches'),
        color=alt.Color('MATERIAL:N', legend=alt.Legend(title="Material"))
    )
    
    # Create the line chart for overall averages
    line = alt.Chart(overall_avg).mark_line(color='red').encode(
        x=alt.X('Interval:O', axis=alt.Axis(title='Interval')),
        y=alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Overall Average Cycle Time (days)'))
    )
    
    return (points + line).resolve_scale(y='independent')

# Streamlit app
st.title('Manufacturing Batch Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type='xlsx')
if uploaded_file:
    # Toggle for time intervals
    interval = st.radio("Select Time Interval", ('Monthly', 'Weekly'))
    
    df = preprocess_data(uploaded_file, interval)
    
    # Generate and display the plot
    plot = generate_plot(df, interval)
    st.altair_chart(plot, use_container_width=True).resolve_scale(y='independent')
    
    # Selector for materials
    material = st.selectbox('Select a Material', df['MATERIAL'].unique())
    
    # Filter data for the selected material
    material_df = df[df['MATERIAL'] == material]
    
    # Boxplot for the selected material
    boxplot = alt.Chart(material_df).mark_boxplot().encode(
        x=alt.X('Interval:O', axis=alt.Axis(title='Interval')),
        y=alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Cycle Time (days)'))
    )
    st.altair_chart(boxplot, use_container_width=True)
