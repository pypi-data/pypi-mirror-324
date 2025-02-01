import pandas as pd

def remove_duplicates(df, subset_columns=None, keep='first'):
    """
    Remove duplicate rows from a DataFrame based on specified columns.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to process.
        
    subset_columns : list or None
        List of column names to consider for identifying duplicates.
        If None (default), consider all columns.
        
    keep : str
        Determines which duplicates to keep:
        - 'first': Keep the first occurrence (default).
        - 'last': Keep the last occurrence.
        - False: Drop all duplicates.

    Raises
    ------
    ValueError :
        If the input for dataframe is not a pandas DataFrame.
        If any column in subset_columns is not a column in the input dataframe.
        If the input for keep is not 'first', 'last', or False.

    Returns
    -------
    pd.DataFrame: A DataFrame with duplicates removed.

    Example
    -------
    >>> data = {'A': [1, 2, 2, 4], 'B': [5, 6, 6, 8]}
    >>> df = pd.DataFrame(data)
    >>> remove_duplicates(df, subset_columns=['A'])
       A  B
    0  1  5
    1  2  6
    3  4  8
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if subset_columns is not None:
        if not all(col in df.columns for col in subset_columns):
            raise ValueError("Some columns in subset_columns are not present in the DataFrame")
    
    if keep not in ['first', 'last', False]: 
         raise ValueError("Invalid value for 'keep'. Must be 'first', 'last', or False.")

    # Drop duplicates using pandas
    original_row_count = len(df)
    result = df.drop_duplicates(subset=subset_columns, keep=keep)
    dropped_rows = original_row_count - len(result)

    print(f"{dropped_rows} rows have been dropped.")

    return result


