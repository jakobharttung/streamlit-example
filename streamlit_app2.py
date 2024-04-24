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
    
    # Base chart for sharing the X-axis and Y-axis scales
    base = alt.Chart().encode(
        x=alt.X(f'{interval_col}:O', axis=alt.Axis(title='Time Interval'))
    )

    # Creating the line chart for overall average cycle time
    line = base.mark_line(color='red').encode(
        y=alt.Y('Overall Average Cycle Time:Q', axis=alt.Axis(title='Cycle Time (days)'))
    ).transform_filter(
        (alt.datum['Overall Average Cycle Time'] != 0)
    ).properties(
        width=700,
        height=400
    ).data(overall_avg_data)

    # Creating the circles for the material averages
    circles = base.mark_circle().encode(
        y=alt.Y('average_cycle_time:Q'),
        size=alt.Size('number_of_batches:Q', title='Number of Batches', legend=alt.Legend(title="Batch Count")),
        color='MATERIAL:N',
        tooltip=['MATERIAL', 'average_cycle_time', 'number_of_batches']
    ).properties(
        width=700,
        height=400
    ).data(material_avg_data)
    
    # Combining the line and circle charts
    combined_chart = alt.layer(line, circles).resolve_scale(
        y='shared'
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
