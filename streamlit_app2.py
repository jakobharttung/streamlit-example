import streamlit as st
import altair as alt
import pandas as pd

def load_data(uploaded_file):
    data = pd.read_excel(uploaded_file)
    data['END TIME'] = pd.to_datetime(data['END TIME'])
    # Create month and week period columns for aggregation
    data['MONTH_YEAR'] = data['END TIME'].dt.to_period('M').astype(str)  # Convert to string for display
    data['WEEK_YEAR'] = data['END TIME'].dt.strftime('%Y - W%V')  # Already string
    return data

st.title("Manufacturing Batch Cycle Times Analysis")

uploaded_file = st.file_uploader("Choose an Excel file", type='xlsx')
if uploaded_file is not None:
    data = load_data(uploaded_file)
    interval = st.radio("Select Time Interval:", ('Weekly', 'Monthly'))
    interval_col = 'MONTH_YEAR' if interval == 'Monthly' else 'WEEK_YEAR'
    
    # Compute overall and per material average cycle times
    overall_avg_data = data.groupby(interval_col)['CYCLE TIME'].mean().reset_index()
    overall_avg_data = overall_avg_data.rename(columns={'CYCLE TIME': 'Overall Average Cycle Time'})
    
    material_avg_data = data.groupby(['MATERIAL', interval_col]).agg(
        average_cycle_time=('CYCLE TIME', 'mean'),
        number_of_batches=('MATERIAL', 'count')
    ).reset_index()
    
    # Define the base encoding for shared axis settings
    base = alt.Chart().encode(
        x=alt.X(f'{interval_col}:O', title='Time Interval')
    )

    # Line chart for overall average cycle time
    line = alt.Chart(overall_avg_data).mark_line(color='red').encode(
        y=alt.Y('Overall Average Cycle Time:Q', title='Cycle Time (days)', scale=alt.Scale(zero=False))
    )

    # Circle chart for material-specific average cycle times
    circles = alt.Chart(material_avg_data).mark_circle().encode(
        y=alt.Y('average_cycle_time:Q', title='Cycle Time (days)', scale=alt.Scale(zero=False)),
        size=alt.Size('number_of_batches:Q', title='Number of Batches'),
        color='MATERIAL:N',
        tooltip=['MATERIAL', 'average_cycle_time', 'number_of_batches']
    )

    # Combine charts with shared y-axis
    combined_chart = (line + circles).resolve_scale(
        y='shared'
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(combined_chart, use_container_width=True)
    
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
