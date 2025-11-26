def clean_shark_attack_type(SAdf):
    """
    Cleans and standardizes the 'Type' column in the DataFrame SAdf.
    
    Args:
        SAdf (pd.DataFrame): The DataFrame containing the 'Type' column.

    Returns:
        pd.DataFrame: The modified DataFrame.
    """
   
    # Standardize the 'Type' column: convert to string, strip whitespace, and Title Case
    SAdf['Type'] = SAdf['Type'].astype(str).str.strip().str.title()

    # Define the list of allowed (canonical) values
    canonical_types = ['Unprovoked', 'Provoked']

    # Replace any value not in the canonical list with 'Unknown'
    SAdf['Type'] = SAdf['Type'].mask(~SAdf['Type'].isin(canonical_types), 'Unknown')
    
    return SAdf

# Example of how you would call this function (assuming SAdf is defined):
# SAdf = clean_shark_attack_type(SAdf)