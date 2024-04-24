import streamlit as st
import pandas as pd
import seaborn as sns

# Streamlit app
st.title('Material Cycle Time Analysis')

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    data['END TIME'] = pd.to_datetime(data['END TIME'])  # ensure END TIME is datetime format

    # Material selection
    material_list = data['MATERIAL'].unique()
    selected_material = st.selectbox('Select a material:', material_list)

    # Grouping selection
    group_by_options = ['Week', 'Month']
    group_by = st.selectbox('Group by:', group_by_options)

    # Filter data based on selected material
    filtered_data = data[data['MATERIAL'] == selected_material]

    # Process data for boxplot
    if group_by == 'Week':
        filtered_data['TIME GROUP'] = filtered_data['END TIME'].dt.isocalendar().week
        time_label = 'Week of the Year'
    elif group_by == 'Month':
        filtered_data['TIME GROUP'] = filtered_data['END TIME'].dt.month
        time_label = 'Month of the Year'

    # Plotting
    fig, ax = plt.subplots()
    sns.boxplot(x='TIME GROUP', y='CYCLE TIME', data=filtered_data, ax=ax)
    ax.set_title(f'Cycle Time Distribution by {group_by} for {selected_material}')
    ax.set_xlabel(time_label)
    ax.set_ylabel('Cycle Time (Days)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("Please upload an Excel file to proceed.")
