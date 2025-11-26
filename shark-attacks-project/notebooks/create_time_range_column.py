def create_time_range_column(SAdf):
    """
    Creates a 'Time_Range' column based on the hour extracted from the 'Time' column.
    NaN values resulting from missing 'Time' data are renamed to 'Unknown'.

    Args:
        SAdf (pd.DataFrame): The DataFrame containing the 'Time' column (expected 
                             to contain datetime.time objects or pandas.NaT).

    Returns:
        pd.DataFrame: The modified DataFrame with the new 'Time_Range' column.
    """
    import numpy as np
    import pandas as pd
    from datetime import time

    def categorize_time(time_obj):
        """
        Categorizes a datetime.time object into a descriptive time range.
        """
        # If the time is NaT (missing or invalid), return NaN
        if pd.isna(time_obj):
            return np.nan
        
        # Extract the hour component (0-23)
        hour = time_obj.hour

        if 6 <= hour < 12:
            return 'Morning'        # 06:00:00 to 11:59:59
        elif 12 <= hour < 17:
            return 'Afternoon'      # 12:00:00 to 16:59:59 (Noon to 5 PM)
        elif 17 <= hour < 22:
            return 'Evening'        # 17:00:00 to 21:59:59 (5 PM to 10 PM)
        else: # 22 <= hour <= 23 OR 0 <= hour < 6
            return 'Night'          # 22:00:00 to 05:59:59 (10 PM to 6 AM)

    # Apply the categorization function to the cleaned 'Time' column
    SAdf['Time_Range'] = SAdf['Time'].apply(categorize_time)

    # Replace NaN values with 'Unknown'
    SAdf['Time_Range'] = SAdf['Time_Range'].fillna('Unknown')
    
    return SAdf

# Example of how you would call this function (assuming SAdf is defined):
# SAdf = create_time_range_column(SAdf)