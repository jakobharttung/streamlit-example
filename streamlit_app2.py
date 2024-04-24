import streamlit as st
import altair as alt
import pandas as pd

def load_data(uploaded_file):
    data = pd.read_excel(uploaded_file)
    data['END TIME'] = pd.to_datetime(data['END TIME'])
    # Adding period columns for aggregation
    data['MONTH_YEAR'] = data['END TIME'].dt.to_period('M')
    data['WEEK_YEAR'] = data['END TIME'].dt.strftime('%Y - W%V')
    return data

st.title("Manufacturing Batch Cycle Times Analysis")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type='xlsx')
if uploaded_file is not None:
    data = load_data(uploaded_file)

    # Interval selection
    interval = st.radio("Select Time Interval:", ('Weekly', 'Monthly'))
    interval_col = 'MONTH_YEAR' if interval == 'Monthly' else 'WEEK_YEAR'

    # Aggregate data based on selected interval
    summary = data.groupby([interval_col, 'MATERIAL']).agg(
        average_cycle_time=('CYCLE TIME', 'mean'),
        number_of_batches=('START BATCH CODE', 'count')
    ).reset_index()

    overall_avg = data.groupby(interval_col).agg(
        overall_avg_cycle_time=('CYCLE TIME', 'mean')
    ).reset_index()

    # Combined Chart: Line for Overall Average, Points for Each Material
    line = alt.Chart(overall_avg).mark_line(color='red').encode(
        x=alt.X(f'{interval_col}:O', title='Time Interval'),
        y=alt.Y('overall_avg_cycle_time:Q', title='Overall Average Cycle Time (days)')
    )

    points = alt.Chart(summary).mark_circle().encode(
        x=alt.X(f'{interval_col}:O', title='Time Interval'),
        y=alt.Y('average_cycle_time:Q'),
        size=alt.Size('number_of_batches:Q', title='Number of Batches'),
        color='MATERIAL:N',
        tooltip=['MATERIAL', 'average_cycle_time', 'number_of_batches']
    )

    combined_chart = alt.layer(line, points).properties(
        width=700,
        height=400
    ).resolve_scale(
        y='independent'
    )

    st.altair_chart(combined_chart, use_container_width=True)

    # Material Selector and Boxplot
    selected_material = st.selectbox('Select Material:', summary['MATERIAL'].unique())
    material_data = data[data['MATERIAL'] == selected_material]

    boxplot = alt.Chart(material_data).mark_boxplot().encode(
        x=alt.X(f'{interval_col}:O', title='Time Interval'),
        y=alt.Y('CYCLE TIME:Q', title='Cycle Time (days)'),
    ).properties(
        title=f'Cycle Time Distribution for {selected_material}',
        width=700,
        height=400
    )
    st.altair_chart(boxplot, use_container_width=True)
