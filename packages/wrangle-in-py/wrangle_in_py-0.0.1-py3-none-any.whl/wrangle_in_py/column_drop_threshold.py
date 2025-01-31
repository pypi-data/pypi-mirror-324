import pandas as pd
from scipy.stats import variation

def column_drop_threshold(df, threshold, variance=None):
    """
    Returns a copy of the dataframe inputted with columns removed if they did not meet the threshold specified, 
    and with columns removed if they had a coefficient of variance lower than specified.
    
    Parameters
    ----------
    df : pd.DataFrame
        The input pandas dataframe whose missingness threshold and coefficient of variance needs to be checked
    
    threshold : float
        Must be 0 <= threshold <= 1
        The threshold for the proportion of missing values to allow in each column of the dataframe, 
        Columns with a larger proportion of missing observations than the threshold will be removed from the dataframe

    variance : float
        Default is None
        The lowest coefficient of variance to allow in any one column of the dataframe
        Columns with a lower variance than specified will be removed from the dataframe
        A column must have at least 2 numbers for coefficient of variance to be calculated
          because the coefficient of variance cannot be calculated with 1 or 0 numbers. 

    Raises
    -------
    TypeError :
    	If the input for df is not a pandas DataFrame.
     
    ValueError :
    	If the input for threshold is not a float and in the inclusive range 0 and 1.
     	Or if the input for variance is not a float >=0.
    
    Returns
    ----------
    pd.DataFrame
        A new dataframe where each column meets or exceeds the specified allowable missingness threshold, and the variance threshold. 
        Any columns previously not meeting the thresholds have been removed.
    
    Examples
    ----------
    >>> data = {'apple': [1, 2, NaN], 'banana': [3, 4, 5], 'kiwi': [NaN, 30, NaN], 'peach': [2, 2, 2]}
    >>> df = pd.DataFrame(data)
    >>> column_drop_threshold(df, 0.35, 0.1)
        apple banana
    0   1     3
    1   2     4
    2   NaN   5
    """
    # Check that the df is a pandas dataframe
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The first argument must be a pandas DataFrame.")
        
    # Check that the missingness threshold is a number between 0 and 1
    if not (isinstance(threshold, (int, float)) and 0 <= threshold <= 1):
        raise ValueError("The missingness threshold must be a number between 0 and 1.")
    
    # Check that the coefficient of variance is a positive float
    if variance is not None and not (isinstance(variance, (int, float)) and variance >= 0):
        raise ValueError("The coefficient of variance must be a positive float.")

    columns_to_drop = []	

    for col in df.columns:
        missing_count = df[col].isnull().sum() # Calculate the total number of missing values in the column
        total_count = len(df[col])  #Calculate the total number of values in the column 
        missingness = (missing_count / total_count) # Calculate the proportion of missing values 
        if missingness > threshold: 
            columns_to_drop.append(col) # If the missingness proportion is too high add the column to the drop list
	
    if variance is not None:
        for col in df.select_dtypes(include=['number']).columns: 
            cv = variation(df[col]) # Calculate the coefficient of variance for the column
            if cv < variance: 
                columns_to_drop.append(col) # If the cv is too low add the column to the drop list
                
    dropped_df = df.drop(columns=columns_to_drop, errors='ignore') # Drop the specified columns
	
    return dropped_df


