import streamlit as st
import pandas as pd
import altair as alt

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Convert 'END TIME' to datetime and set it as index
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    df.set_index('END TIME', inplace=True)

    # Toggle for time interval selection
    interval = st.radio("Select the time interval:", ('Monthly', 'Weekly'))

    # Resample dataframe based on selected interval
    if interval == 'Monthly':
        df_resampled = df.resample('M').mean()
    else:
        df_resampled = df.resample('W').mean()

    # Calculate overall average cycle time
    overall_avg_cycle_time = df['CYCLE TIME'].mean()

    # Calculate average cycle time for each material
    material_avg = df.groupby('MATERIAL')['CYCLE TIME'].mean().reset_index()

    # Visualization
    base = alt.Chart(df.reset_index()).encode(
        alt.X('END TIME:T', axis=alt.Axis(title=interval + ' Interval'))
    )
    line = base.mark_line(color='red').encode(
        alt.Y(alt.Y('mean(CYCLE TIME):Q', title='Overall Average Cycle Time (days)'),
              scale=alt.Scale(domain=[df['CYCLE TIME'].min(), df['CYCLE TIME'].max()]))
    )
    points = base.mark_circle().encode(
        alt.Y('mean(CYCLE TIME):Q', title='Material Average Cycle Time (days)'),
        alt.Size('count(MATERIAL):Q'),
        alt.Color('MATERIAL:N', legend=alt.Legend(title="Material"))
    )
    chart = alt.layer(line, points).resolve_scale(y='shared')
    st.altair_chart(chart, use_container_width=True)

    # Material selector for boxplot
    material = st.selectbox("Select a material:", df['MATERIAL'].unique())
    material_df = df[df['MATERIAL'] == material]
    boxplot = alt.Chart(material_df.reset_index()).mark_boxplot().encode(
        alt.X('END TIME:T', axis=alt.Axis(title=interval + ' Interval')),
        alt.Y('CYCLE TIME:Q', axis=alt.Axis(title='Cycle Time (days)'))
    )
    st.altair_chart(boxplot, use_container_width=True)
