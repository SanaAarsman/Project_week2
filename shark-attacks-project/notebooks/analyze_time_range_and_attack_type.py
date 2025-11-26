def analyze_time_range_and_attack_type(SAdf):
    """
    Groups shark attack incidents by 'Time_Range' and 'Type', counts the incidents
    in each group, and calculates the percentage of the total known time incidents.

    NOTE: The current code relies on the previous step where NaN in 'Time_Range' 
    was replaced with 'Unknown'. Therefore, filtering 'Time_Range'.notna() will 
    exclude all incidents categorized as 'Unknown'.

    Args:
        SAdf (pd.DataFrame): The DataFrame containing the 'Time_Range' and 'Type' columns.

    Returns:
        pd.DataFrame: A DataFrame showing the 'Time_Range', 'Type', 'Incident Count', 
                      and 'Percentage' for all categorized time incidents.
    """
    import pandas as pd
    
    # 1. Filter the DataFrame to include only incidents with a known time range
    # Assuming 'Unknown' is the category to exclude (as it's the old NaN).
    known_time_incidents = SAdf[SAdf['Time_Range'] != 'Unknown'].copy()

    # 2. Calculate the total number of known incidents (denominator for percentage)
    total_known_incidents = len(known_time_incidents)

    # 3. Group by Time_Range and Type, then count the size of each group
    grouped_incidents = known_time_incidents.groupby(['Time_Range', 'Type']).size().reset_index(name='Incident Count')

    # 4. Calculate the percentage of the total known incidents
    grouped_incidents['Percentage'] = (grouped_incidents['Incident Count'] / total_known_incidents) * 100

    # 5. Format the percentage column for clean display
    grouped_incidents['Percentage'] = grouped_incidents['Percentage'].round(2).astype(str) + '%'
    
    return grouped_incidents

# Example of how you would call this function (assuming SAdf is defined):
# attack_breakdown = analyze_time_range_and_attack_type(SAdf)