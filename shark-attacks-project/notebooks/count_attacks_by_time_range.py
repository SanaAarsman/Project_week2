def count_attacks_by_time_range(SAdf):
    """
    Counts the occurrences of each category in the 'Time_Range' column, 
    including 'Unknown' values (previously NaN).

    Args:
        SAdf (pd.DataFrame): The DataFrame containing the 'Time_Range' column.

    Returns:
        pd.DataFrame: A DataFrame with two columns: 'Time Range' and 
                      'Incident Count', showing the value counts.
    """
    import pandas as pd
    
    # Calculate the count of shark attacks per time range category.
    # dropna=False ensures the 'Unknown' category (if present) is included.
    attacks_by_time_range = SAdf['Time_Range'].value_counts(dropna=False)

    # Convert the Series to a DataFrame and rename the count column
    attacks_df = attacks_by_time_range.reset_index()
    attacks_df.columns = ['Time Range', 'Incident Count']
    
    return attacks_df

# Example of how you would call this function (assuming SAdf is defined):
# attack_counts = count_attacks_by_time_range(SAdf)