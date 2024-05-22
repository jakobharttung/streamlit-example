import streamlit as st
import pandas as pd
import altair as alt

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Convert 'END TIME' to datetime
    df['END TIME'] = pd.to_datetime(df['END TIME'])

    # Toggle for time interval selection
    interval = st.radio("Select the time interval:", ('Monthly', 'Weekly'))

    # Format 'END TIME' based on selected interval
    if interval == 'Monthly':
        df['Time Interval'] = df['END TIME'].dt.strftime('%Y-%m')
    else:
        df['Time Interval'] = df['END TIME'].dt.strftime('%Y-%U')

    # Calculate overall average cycle time
    overall_avg_cycle_time = df.groupby('Time Interval')['CYCLE TIME'].mean().reset_index(name='Overall Average Cycle Time')

    # Calculate average cycle time for each material
    material_avg = df.groupby(['MATERIAL', 'Time Interval'])['CYCLE TIME'].mean().reset_index(name='Material Average Cycle Time')

    # Merge the overall average with material averages
    merged_df = pd.merge(material_avg, overall_avg_cycle_time, on='Time Interval')

    # Visualization
    base = alt.Chart(merged_df).encode(
        alt.X('Time Interval:N', axis=alt.Axis(title=interval + ' Interval'))
    )
    line = base.mark_line(color='red').encode(
        alt.Y('Overall Average Cycle Time:Q', title='Cycle Time (days)')
    )
    points = base.mark_circle().encode(
        alt.Y('Material Average Cycle Time:Q', title='Cycle Time (days)'),
        alt.Size('count(MATERIAL):Q'),
        alt.Color('MATERIAL:N', legend=alt.Legend(title="Material"))
    )
    chart = alt.layer(line, points).resolve_scale(y='shared')
    st.altair_chart(chart, use_container_width=True)

    # Material selector for boxplot
    material = st.selectbox("Select a material:", df['MATERIAL'].unique())
    material_df = df[df['MATERIAL'] == material]
    boxplot = alt.Chart(material_df).mark_boxplot().encode(
        alt.X('Time Interval:N', axis=alt.Axis(title=interval + ' Interval')),
        alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Cycle Time (days)'))
    )
    st.altair_chart(boxplot, use_container_width=True)
