import pandas as pd

def extracting_ymd(df, column):
    """
    Returns a copy of the input DataFrame with three new columns: year, month, and day,
    extracted from the specified datetime column.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the datetime column.
        
    column : str
        The name of the datetime column to extract from.

    Raises
    -------
    KeyError :
        If the input column is not a column in df.
        
    TypeError :
        If the input column is not of datetime type.

    Returns
    -------
    pandas.DataFrame :
        A copy of the input DataFrame with added columns:
        '<column>_year', '<column>_month', '<column>_day'.

    Example
    -------
    >>> df = pd.DataFrame({'timestamp': ['2024-01-07 12:30:45', '2023-12-25 08:15:30']})
    >>> df['timestamp'] = pd.to_datetime(df['timestamp'])
    >>> extracting_ymd(df, 'timestamp')
            timestamp  timestamp_year  timestamp_month  timestamp_day
    0 2024-01-07 12:30:45             2024                1             7
    1 2023-12-25 08:15:30             2023               12            25
    """
    # Check if the column exists
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")

    # Check if the column is of datetime type
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        raise TypeError(f"Column '{column}' must be of datetime type.")

    # Create a copy of the DataFrame to avoid modifying the original
    result = df.copy()

    # Ensure empty datetime columns are correctly handled
    if result.empty:     
        result[f"{column}_year"] = pd.Series(dtype="Int64")
        result[f"{column}_month"] = pd.Series(dtype="Int64")
        result[f"{column}_day"] = pd.Series(dtype="Int64")
        return result

    # Extract hour, minute, and second into new columns
    result[f"{column}_year"] = result[column].dt.year.astype("Int64")
    result[f"{column}_month"] = result[column].dt.month.astype("Int64")
    result[f"{column}_day"] = result[column].dt.day.astype("Int64")

    return result


def extracting_hms(df, column):
    """
    Returns a copy of the input DataFrame with three new columns: hour, minute, and second,
    extracted from the specified datetime column.

    Parameters
    -----------
    df : pd.DataFrame
        The DataFrame containing the datetime column.
        
    column : str
        The name of the datetime column to extract from.
        
    Raises
    -------
    KeyError :
        If the input column is not a column in df.
        
    TypeError :
        If the input column is not of datetime type.

    Returns
    -------
    pd.DataFrame :
        A copy of the input DataFrame with added columns:
        '<column>_hour', '<column>_minute', '<column>_second'.

    Example
    -------
    >>> df = pd.DataFrame({'timestamp': ['2024-01-07 12:30:45', '2023-12-25 08:15:30']})
    >>> df['timestamp'] = pd.to_datetime(df['timestamp'])
    >>> extracting_hms(df, 'timestamp')
            timestamp  timestamp_hour  timestamp_minute  timestamp_second
    0 2024-01-07 12:30:45             12                30               45
    1 2023-12-25 08:15:30              8                15               30
    """

    # Check if the column exists
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")

    # Check if the column is of datetime type
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        raise TypeError(f"Column '{column}' must be of datetime type.")

    # Create a copy of the DataFrame to avoid modifying the original
    result = df.copy()

    # Ensure empty datetime columns are correctly handled
    if result.empty:     
        result[f"{column}_hour"] = pd.Series(dtype="Int64")
        result[f"{column}_minute"] = pd.Series(dtype="Int64")
        result[f"{column}_second"] = pd.Series(dtype="Int64")
        return result

    # Extract hour, minute, and second into new columns
    result[f"{column}_hour"] = result[column].dt.hour.astype("Int64")
    result[f"{column}_minute"] = result[column].dt.minute.astype("Int64")
    result[f"{column}_second"] = result[column].dt.second.astype("Int64")

    return result

