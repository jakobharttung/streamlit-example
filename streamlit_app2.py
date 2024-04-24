import streamlit as st
import altair as alt
import pandas as pd

def load_data(uploaded_file):
    # Load the Excel file
    data = pd.read_excel(uploaded_file)
    # Ensure columns are correctly named as per your Excel file, assuming all uppercase
    data['END TIME'] = pd.to_datetime(data['END TIME'])
    # Create period columns for aggregation
    data['MONTH_YEAR'] = data['END TIME'].dt.to_period('M')
    data['WEEK_YEAR'] = data['END TIME'].dt.strftime('%Y - W%V')
    return data

st.title("Batch Cycle Times Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type='xlsx')
if uploaded_file is not None:
    data = load_data(uploaded_file)
    
    # Interval selection
    interval = st.radio("Choose the analysis interval:", ('Weekly', 'Monthly'))
    interval_col = 'MONTH_YEAR' if interval == 'Monthly' else 'WEEK_YEAR'
    
    # Aggregate data for overall and per material
    overall_avg_data = data.groupby(interval_col)['CYCLE TIME'].mean().reset_index().rename(columns={'CYCLE TIME': 'Overall Average'})
    material_avg_data = data.groupby(['MATERIAL', interval_col]).agg(
        Average_Cycle_Time=('CYCLE TIME', 'mean'),
        Number_of_Batches=('MATERIAL', 'size')
    ).reset_index()

    # Line chart for overall average cycle time
    line = alt.Chart(overall_avg_data).mark_line(color='red').encode(
        x=alt.X(interval_col, title='Time Interval'),
        y=alt.Y('Overall Average', title='Average Cycle Time (days)')
    )

    # Circle chart for material-specific averages
    circles = alt.Chart(material_avg_data).mark_circle().encode(
        x=alt.X(interval_col, title='Time Interval'),
        y=alt.Y('Average_Cycle_Time', title='Average Cycle Time (days)'),
        size='Number_of_Batches',
        color='MATERIAL',
        tooltip=['MATERIAL', 'Average_Cycle_Time', 'Number_of_Batches']
    )

    # Combine charts with shared y-axis
    combined_chart = alt.layer(line, circles).resolve_scale(
        y='shared'
    ).properties(
        width=700,
        height=400
    )
    
    st.altair_chart(combined_chart, use_container_width=True)

    # Selector for materials and boxplot for cycle time distribution
    selected_material = st.selectbox('Select a material:', data['MATERIAL'].unique())
    material_data = data[data['MATERIAL'] == selected_material]
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        x=alt.X(interval_col, title='Time Interval'),
        y=alt.Y('CYCLE TIME', title='Cycle Time (days)')
    ).properties(
        title=f'Cycle Time Distribution for {selected_material}',
        width=700,
        height=400
    )
    
    st.altair_chart(boxplot, use_container_width=True)
