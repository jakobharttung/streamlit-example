import streamlit as st
import altair as alt
import pandas as pd

def load_data(uploaded_file):
    # Load the Excel file
    data = pd.read_excel(uploaded_file)
    data['End Time'] = pd.to_datetime(data['End Time'])
    # Create period columns for aggregation
    data['Month_Year'] = data['End Time'].dt.to_period('M')
    data['Week_Year'] = data['End Time'].dt.strftime('%Y - W%V')
    return data

st.title("Batch Cycle Times Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type='xlsx')
if uploaded_file is not None:
    data = load_data(uploaded_file)
    
    # Interval selection
    interval = st.radio("Choose the analysis interval:", ('Weekly', 'Monthly'))
    interval_col = 'Month_Year' if interval == 'Monthly' else 'Week_Year'
    
    # Aggregate data for overall and per material
    overall_avg_data = data.groupby(interval_col)['Cycle Time'].mean().reset_index().rename(columns={'Cycle Time': 'Overall Average'})
    material_avg_data = data.groupby(['Material', interval_col]).agg(
        Average_Cycle_Time=('Cycle Time', 'mean'),
        Number_of_Batches=('Material', 'size')
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
        color='Material',
        tooltip=['Material', 'Average_Cycle_Time', 'Number_of_Batches']
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
    selected_material = st.selectbox('Select a material:', data['Material'].unique())
    material_data = data[data['Material'] == selected_material]
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        x=alt.X(interval_col, title='Time Interval'),
        y=alt.Y('Cycle Time', title='Cycle Time (days)')
    ).properties(
        title=f'Cycle Time Distribution for {selected_material}',
        width=700,
        height=400
    )
    
    st.altair_chart(boxplot, use_container_width=True)
