def preprocess_data(df, interval):
    # Convert END TIME to datetime
    df['END TIME'] = pd.to_datetime(df['END TIME'])
    
    # Ensure CYCLE TIME is numeric
    df['CYCLE TIME'] = pd.to_numeric(df['CYCLE TIME'], errors='coerce')
    
    # Set the interval for analysis
    if interval == 'Monthly':
        df['TIME INTERVAL'] = df['END TIME'].dt.to_period('M')
    else:
        df['TIME INTERVAL'] = df['END TIME'].dt.to_period('W')
    
    # Group by the interval and MATERIAL, then calculate the average CYCLE TIME
    material_cycle_time = df.groupby(['MATERIAL', 'TIME INTERVAL']).agg({'CYCLE TIME': 'mean', 'MATERIAL': 'size'}).rename(columns={'MATERIAL': 'BATCH COUNT'})
    
    # Calculate the overall average CYCLE TIME
    overall_cycle_time = df.groupby('TIME INTERVAL').agg({'CYCLE TIME': 'mean'}).rename(columns={'CYCLE TIME': 'OVERALL CYCLE TIME'})
    
    return material_cycle_time.reset_index(), overall_cycle_time.reset_index()
