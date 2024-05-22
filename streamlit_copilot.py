import streamlit as st
import pandas as pd
import altair as alt

# Function to load data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    else:
        return pd.DataFrame()

# Function to generate the plot
def generate_plot(df, interval):
    # Ensure CYCLE TIME is numeric
    df['CYCLE TIME'] = pd.to_numeric(df['CYCLE TIME'], errors='coerce')
    
    # Calculate overall average cycle time
    overall_avg_cycle_time = df['CYCLE TIME'].mean()
    
    # Calculate average cycle time for each material
    material_avg = df.groupby('MATERIAL')['CYCLE TIME'].mean().reset_index()
    
    # Calculate number of batches for each material
    material_counts = df['MATERIAL'].value_counts().reset_index()
    material_counts.columns = ['MATERIAL', 'BATCH_COUNT']
    
    # Merge the two dataframes
    material_avg = material_avg.merge(material_counts, on='MATERIAL')
    
    # Create the base line chart for overall average
    line = alt.Chart(df).mark_line().encode(
        x=alt.X('END TIME:T', timeUnit=interval),
        y=alt.Y('mean(CYCLE TIME):Q', title='Average Cycle Time')
    )
    
    # Create the circle chart for each material
    points = alt.Chart(material_avg).mark_circle().encode(
        x=alt.X('END TIME:T', timeUnit=interval),
        y=alt.Y('CYCLE TIME:Q', title=''),
        size='BATCH_COUNT:Q'
    )
    
    # Combine the two charts
    chart = alt.layer(line, points).resolve_scale(y='shared')
    
    return chart

# Streamlit app
def main():
    st.title('Manufacturing Batch Cycle Time Analysis')
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type='xlsx')
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        # Toggle for time intervals
        interval = st.radio("Select Time Interval", ('monthly', 'weekly'))
        
        # Generate and display plot
        st.altair_chart(generate_plot(df, interval), use_container_width=True)
        
        # Selector for materials
        material = st.selectbox('Select a Material', df['MATERIAL'].unique())
        
        # Filter data for selected material
        material_df = df[df['MATERIAL'] == material]
        
        # Generate and display boxplot for selected material
        boxplot = alt.Chart(material_df).mark_boxplot().encode(
            x=alt.X('END TIME:T', timeUnit=interval),
            y='CYCLE TIME:Q'
        )
        st.altair_chart(boxplot, use_container_width=True)

if __name__ == "__main__":
    main()
