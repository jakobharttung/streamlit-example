import streamlit as st
import pandas as pd
import altair as alt

# Streamlit app
st.title('Material Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    data['END TIME'] = pd.to_datetime(data['END TIME'])  # ensure END TIME is datetime format
    data['WEEK'] = data['END TIME'].dt.isocalendar().week  # add week column for grouping
    data['MONTH'] = data['END TIME'].dt.month  # add month column for grouping

    # Material selection
    material_list = data['MATERIAL'].unique()
    selected_material = st.selectbox('Select a material:', material_list)

    # Grouping selection for the first chart
    time_group_options = ['Week', 'Month']
    selected_group = st.selectbox('Group the first chart by:', time_group_options)

    # Filter data based on selected material
    filtered_data = data[data['MATERIAL'] == selected_material]

    # Determine grouping for the first chart
    if selected_group == 'Week':
        group_field = 'WEEK'
        time_label = 'Week of the Year'
    else:
        group_field = 'MONTH'
        time_label = 'Month of the Year'

    # Boxplot visualization for the first chart
    boxplot = alt.Chart(filtered_data).mark_boxplot().encode(
        x=alt.X(f'{group_field}:O', title=time_label),
        y=alt.Y('CYCLE TIME:Q', title='Cycle Time (Days)'),
        tooltip=['CYCLE TIME', f'{group_field}']
    ).properties(
        width=600,
        height=400,
        title=f'Cycle Time Distribution by {time_label}'
    ).interactive()

    st.altair_chart(boxplot, use_container_width=True)

    # Group by month for the second chart (line and bubble)
    monthly_data = data.groupby(['MONTH', 'MATERIAL']).agg(
        average_cycle_time=('CYCLE TIME', 'mean'),
        num_batches=('CYCLE TIME', 'count')
    ).reset_index()

    # Line chart for average cycle time across all materials
    line_chart = alt.Chart(monthly_data).mark_line(color='blue').encode(
        x=alt.X('MONTH:O', title='Month of the Year'),
        y=alt.Y('average_cycle_time:Q', title='Average Cycle Time (Days)'),
        tooltip=['MONTH', 'average_cycle_time']
    ).properties(
        title='Monthly Average Cycle Time Across Materials'
    )

    # Bubble chart for the number of batches per material at the average cycle time
    bubbles = alt.Chart(monthly_data).mark_point().encode(
        x='MONTH:O',
        y='average_cycle_time:Q',
        size='num_batches:Q',
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

    st.altair_chart(combined_chart, use_container_width=True)
else:
    st.write("Please upload an Excel file to proceed.")
