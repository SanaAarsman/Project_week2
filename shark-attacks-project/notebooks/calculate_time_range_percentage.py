def calculate_time_range_percentage(SAdf):
    """
    Counts shark attacks by 'Time_Range' and calculates the percentage for 
    each known time category, excluding 'Unknown' incidents from the total 
    used for the percentage calculation.

    Args:
        SAdf (pd.DataFrame): The DataFrame containing the 'Time_Range' column.

    Returns:
        pd.DataFrame: A DataFrame with 'Time Range', 'Incident Count', and 
                      'Percentage' columns.
    """
    
    # 1. Calculate the count of shark attacks per time range category (including 'Unknown').
    attacks_by_time_range = SAdf['Time_Range'].value_counts(dropna=False)

    # 2. Convert the Series to a DataFrame and rename the count column
    attacks_df = attacks_by_time_range.reset_index()
    attacks_df.columns = ['Time Range', 'Incident Count']

    # 3. Calculate total incidents FOR KNOWN TIMES ONLY
    total_incidents_known = SAdf[SAdf['Time_Range'] != 'Unknown']['Time_Range'].count()

    # 4. Create the new column for the percentage.
    attacks_df['Percentage'] = attacks_df.apply(
        lambda row: (row['Incident Count'] / total_incidents_known) * 100
        if row['Time Range'] != 'Unknown'
        else 0,
        axis=1
    )

    # 5. Format the percentage to two decimal places for readability
    attacks_df['Percentage'] = attacks_df['Percentage'].round(2).astype(str) + '%'
    
    return attacks_df

# Example of how you would call this function (assuming SAdf is defined):
# time_breakdown_df = calculate_time_range_percentage(SAdf)