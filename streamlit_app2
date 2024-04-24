import streamlit as st
import altair as alt
import pandas as pd

# Load the data
@st.cache
def load_data():
    data = pd.read_excel('/mnt/data/Plant cycle time Data.xlsx')
    data['END TIME'] = pd.to_datetime(data['END TIME'])
    # Create a month-year and week-year column for grouping
    data['MONTH_YEAR'] = data['END TIME'].dt.to_period('M')
    data['WEEK_YEAR'] = data['END TIME'].dt.strftime('%Y - W%V')
    return data

data = load_data()

# Sidebar for controls
interval = st.sidebar.radio("Select Time Interval", ('Weekly', 'Monthly'))

# Create a summary DataFrame based on selected interval
if interval == 'Monthly':
    summary = data.groupby(['MATERIAL', 'MONTH_YEAR']).agg(
        average_cycle_time=('CYCLE TIME', 'mean'),
        number_of_batches=('START BATCH CODE', 'count')
    ).reset_index()
else:
    summary = data.groupby(['MATERIAL', 'WEEK_YEAR']).agg(
        average_cycle_time=('CYCLE TIME', 'mean'),
        number_of_batches=('START BATCH CODE', 'count')
    ).reset_index()

# Visualization: Bubble Chart
bubble_chart = alt.Chart(summary).mark_point().encode(
    x='average_cycle_time:Q',
    y='MATERIAL:N',
    size='number_of_batches:Q',
    color='MATERIAL:N',
    tooltip=['MATERIAL', 'average_cycle_time', 'number_of_batches']
).interactive()

st.altair_chart(bubble_chart, use_container_width=True)

# Material Selector and Boxplot
selected_material = st.selectbox('Select Material', summary['MATERIAL'].unique())
filtered_data = data[data['MATERIAL'] == selected_material]

# Adjust the x-axis based on the interval
x_axis = 'MONTH_YEAR:O' if interval == 'Monthly' else 'WEEK_YEAR:O'

boxplot = alt.Chart(filtered_data).mark_boxplot().encode(
    x=x_axis,
    y='CYCLE TIME:Q'
).properties(
    title=f'Distribution of Cycle Times for {selected_material}'
)

st.altair_chart(boxplot, use_container_width=True)
