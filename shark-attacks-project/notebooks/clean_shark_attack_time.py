def clean_shark_attack_time(SAdf):
    """
    Performs multi-step cleaning and standardization on the 'Time' column of the DataFrame.
    
    The process involves:
    1. Creating a temporary column ('Time_Cleaned').
    2. Using regex to standardize various formats (xxhxx, xxxxhrs, decimal) into 'HH:MM'.
    3. Filtering out descriptive/range values and setting them to NaN.
    4. Coercing the standardized strings into datetime.time objects in the original 'Time' column.

    Args:
        SAdf (pd.DataFrame): The DataFrame containing the 'Time' column.

    Returns:
        pd.DataFrame: The modified DataFrame with the cleaned 'Time' column and 
                      without the temporary 'Time_Cleaned' column.
    """
    import pandas as pd
    import numpy as np
    
    # 1. Removing white spaces and ensuring string type
    # Create the temporary column 'Time_Cleaned' directly from the string version of 'Time'.
    SAdf['Time_Cleaned'] = SAdf['Time'].fillna('').astype(str).apply(str.strip)
    
    #  2. Step 1: Standardize Common Patterns using Regex 

    # Pattern 1: xxhxx (e.g., '12h30', '9h0')
    SAdf['Time_Cleaned'] = SAdf['Time_Cleaned'].str.replace(
        r'^(\d{1,2})h(\d{0,2})$',
        lambda m: f"{int(m.group(1)):02d}:{m.group(2).zfill(2)}", # Format to 09:00, 13:15
        regex=True
    )

    # Pattern 2 & 3: Consolidated xxxxhrs/hr OR numeric-only time (e.g., '0100hrs', '1524', '100hrs')
    def military_time_formatter(match):
        # m.group(1) is the digits (e.g., '100' or '1524')
        digits = match.group(1)
        
        # 1. Pad to 4 digits (e.g., '100' -> '0100')
        padded_digits = digits.zfill(4)
        
        # 2. Extract HH and MM and join with a colon (e.g., '0100' -> '01:00')
        return f"{padded_digits[:2]}:{padded_digits[-2:]}"

    # Combine matching for xxxxhrs (Pattern 2)
    SAdf['Time_Cleaned'] = SAdf['Time_Cleaned'].str.replace(
        r'^(\d{3,4})\s*hrs?$', 
        military_time_formatter,
        regex=True
    )

    # Combine matching for xxxx (Pattern 3)
    SAdf['Time_Cleaned'] = SAdf['Time_Cleaned'].str.replace(
        r'^(?!\d{1,2}h)(\d{3,4})$', # Numeric only, not already matched by xxhxx
        military_time_formatter,
        regex=True
    )

    # Pattern 4: decimal time (e.g., '15.5')
    def convert_decimal(match):
        hour = int(match.group(1))
        # m.group(2) is the decimal part (e.g., '5')
        # We need to calculate minutes from the decimal part (e.g., 0.5 * 60 = 30)
        minute = int(round(float(f"0.{match.group(2)}")) * 60)
        # Ensure hour padding here as well
        return f"{hour:02d}:{minute:02d}"

    SAdf['Time_Cleaned'] = SAdf['Time_Cleaned'].str.replace(
        r'^(\d{1,2})\.(\d{1,2})$', 
        convert_decimal, 
        regex=True
    )
    
    #  3. Step 2: Handle Ranges, Descriptions, and Unknowns 

    # Values that are ranges, descriptive, or malformed should be set to NaN (missing)
    descriptive_or_range_values = [
        'Not stated', 'AM', '?', 'after 1200hr', '14h00-15h00', '14h00  -15h00',
        'Late afternoon', '14h30 / 15h30', 'Morning ', '09h30 / 10h00',
        '10h45-11