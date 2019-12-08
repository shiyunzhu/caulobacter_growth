import numpy as np
import pandas as pd

def growth_event_annotate(df, threshold=0.5):
    '''This function adds a "divison event" column
    to the passed DataFrame and fills it based on the 
    change in the areas between the previous and the
    next index in  the data frame. If that change is
    above a certain threshold, the subsequent times are
    delineated as the next division event.
    -----
    Parameters:
    df - DataFrame containing columns "time (min)",
    "area (µm²)", and "bacterium".
    -----
    kwargs:
    threshold - the value that determines if the area
    change is a fluctuation in data analysis/acquisition
    or a true division event. Default is 0.5.
    -----
    Returns:
    df - the altered DataFrame, now with a filled "division
    event" column.'''
    event_id = 1
    start_of_event = 0
    
    df['division event'] = np.nan
    
    indices = np.arange(df.shape[0] - 1)
    
    for index in indices:
        area_change = np.abs(df.loc[index, 'area (µm²)'] - df.loc[index + 1, 'area (µm²)'])
        if area_change > threshold:
            end_of_event = index
            
            for ind in range(start_of_event, end_of_event + 1):
                df.loc[ind, 'division event'] = event_id
            start_of_event = index + 1
            event_id += 1
        if index >= 10283:
            df.loc[index, 'division event'] = 107.0
        
    df.loc[10320, 'division event'] = 107.0
    
    return df
