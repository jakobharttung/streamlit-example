import streamlit as st
import altair as alt
import pandas as pd

def load_data(uploaded_file):
    data = pd.read_excel(uploaded_file)
    data['END TIME'] = pd.to_datetime(data['END TIME'])
    # Creating period columns for aggregation
    data['MONTH_YEAR'] = data['END TIME'].dt.to_period('M').astype(str)  # Convert to string for display
    data['WEEK_YEAR'] = data['END TIME'].dt.strftime('%Y - W%V')  # Already string
    return data

st.title("Manufacturing Batch Cycle Times Analysis")

uploaded_file = st.file_uploader("Choose an Excel file", type='xlsx')
if uploaded_file is not None:
    data = load_data(uploaded_file)
    interval = st.radio("Select Time Interval:", ('Weekly', 'Monthly'))
    interval_col = 'MONTH_YEAR' if interval == 'Monthly' else 'WEEK_YEAR'
    
    # Compute overall average cycle time
    overall_avg_data = data.groupby(interval_col)['CYCLE TIME'].mean().reset_index()
    overall_avg_data = overall_avg_data.rename(columns={'CYCLE TIME': 'Overall Average Cycle Time'})
    
    # Compute average cycle time per material
    material_avg_data = data.groupby(['MATERIAL', interval_col]).agg(
        average_cycle_time=('CYCLE TIME', 'mean'),
        number_of_batches=('MATERIAL', 'count')
    ).reset_index()
    
    # Line chart for overall average cycle time across all materials
    line_chart = alt.Chart(overall_avg_data).mark_line(color='blue').encode(
        x=alt.X('MONTH:O', title='Month of the Year'),
        y=alt.Y('overall_average_cycle_time:Q', title='Overall Average Cycle Time (Days)'),
        tooltip=['MONTH', 'overall_average_cycle_time']
    ).properties(
        title='Overall Monthly Average Cycle Time'
    )

    # Bubble chart for the number of batches per material at the average cycle time
    bubbles = alt.Chart(material_avg_data).mark_circle().encode(
        x='MONTH:O',
        y='average_cycle_time:Q',
        size='number_of_batches:Q',
        color='MATERIAL:N',
        tooltip=['MATERIAL', 'average_cycle_time', 'num_batches']
    ).properties(
        title='Number of Batches by Material Each Month'
    )

    # Combine the line and bubble charts
    combined_chart = alt.layer(line_chart, bubbles).resolve_scale(
        y='shared'
    ).properties(
        width=600,
        height=400
    )

    
    # Material selector and boxplot for cycle time distribution
    selected_material = st.selectbox('Select Material:', data['MATERIAL'].unique())
    material_data = data[data['MATERIAL'] == selected_material]
    
    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        x=alt.X(f'{interval_col}:O', title='Time Interval'),
        y=alt.Y('CYCLE TIME:Q', title='Cycle Time (days)')
    ).properties(
        title=f'Cycle Time Distribution for {selected_material}',
        width=700,
        height=400
    )
    
    st.altair_chart(boxplot, use_container_width=True)
