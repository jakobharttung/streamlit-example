import streamlit as st
import pandas as pd
import altair as alt

# Function to preprocess the data
def preprocess_data(uploaded_file):
    # Read the Excel file
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    # Convert 'END TIME' to datetime and extract the month and week
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    df['Month'] = df['END TIME'].dt.to_period('M')
    df['Week'] = df['END TIME'].dt.to_period('W')
    return df

# Function to generate the plot
def generate_plot(df, interval):
    # Group by the selected interval and calculate the average cycle time
    if interval == 'Monthly':
        group = df.groupby(['MATERIAL', 'Month'])
        interval_col = 'Month'
    else:
        group = df.groupby(['MATERIAL', 'Week'])
        interval_col = 'Week'
    
    material_avg = group['CYCLE TIME'].mean().reset_index()
    overall_avg = df['CYCLE TIME'].mean()
    
    # Line chart for overall average cycle time
    line = alt.Chart(pd.DataFrame({interval_col: material_avg[interval_col].unique(), 'CYCLE TIME': [overall_avg]*len(material_avg[interval_col].unique())})).mark_line(color='red').encode(
        x=alt.X(f'{interval_col}:O', axis=alt.Axis(title=interval)),
        y=alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Overall Average Cycle Time (days)'))
    )
    
    # Circle chart for each material
    points = alt.Chart(material_avg).mark_circle().encode(
        x=alt.X(f'{interval_col}:O', axis=alt.Axis(title=interval)),
        y=alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Material Average Cycle Time (days)')),
        size=alt.Size('count()', title='Number of Batches'),
        color=alt.Color('MATERIAL:N', legend=alt.Legend(title="Material"))
    )
    
    return (line + points).resolve_scale(y='independent')

# Streamlit app
st.title('Manufacturing Batch Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type='xlsx')
if uploaded_file:
    df = preprocess_data(uploaded_file)
    
    # Toggle for time intervals
    interval = st.radio("Select Time Interval", ('Monthly', 'Weekly'))
    
    # Generate and display the plot
    plot = generate_plot(df, interval)
    st.altair_chart(plot, use_container_width=True)
    
    # Selector for materials
    material = st.selectbox('Select a Material', df['MATERIAL'].unique())
    
    # Filter data for the selected material
    material_df = df[df['MATERIAL'] == material]
    
    # Boxplot for the selected material
    boxplot = alt.Chart(material_df).mark_boxplot().encode(
        x=alt.X(f'{interval}:O', axis=alt.Axis(title=interval)),
        y=alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Cycle Time (days)'))
    )
    st.altair_chart(boxplot, use_container_width=True)
