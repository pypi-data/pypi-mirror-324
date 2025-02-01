import pandas as pd
from collections import defaultdict
import re

def string_standardizer(messy_string):
    """
    Converts the inputted messy_string to lowercase and
    non-alphanumerics (including spaces and punctuation) will be replaced with underscores.

    Parameters
    ----------
    messy_string : str
        The input string to be standardized.
    
    Raises
    ------
    TypeError :
        If the input messy_string is not a string.

    Returns
    -------
    str
        A standardized version of the input string in lowercase 
        and non-alphanumeric characters replaced by underscores.

    Examples
    --------
    >>> string_standardizer('Jack Fruit 88')
    'jack_fruit_88'
    
    >>> string_standardizer('PINEAPPLES')
    'pineapples'

    >>> string_standardizer('Dragon (Fruit)')
    'dragon__fruit_'
    """
    if not isinstance(messy_string, str):
        raise TypeError("messy_string input should be of type string.")
    new_string = re.sub(r'[^\w]', '_', messy_string)
    new_string = new_string.lower()
    return new_string

def resulting_duplicates(original_strings, standardized_strings):
    """
    Identifies which strings became duplicates after standardization.

    Parameters
    ----------
    original_strings : list of str
        List of strings before standardization.
        
    standardized_strings : list of str
        List of strings after standardization.

    Raises
    ------
    ValueError :
        If the inputs original_strings and standardized_strings are not the same length.
        
    TypeError :
        If either of the inputs, original_strings or standardized_strings,
        are not a list of strings.

    Returns
    -------
    dict :
        A dictionary where the keys are the standardized strings with duplicate(s),
        and the values are lists of the original strings that map to them.
    
    Examples
    --------
    >>> strings_before = ['Jack Fruit 88.', "Jack!Fruit!88!", "PINEAPPLES"]
    >>> strings_after = ["jack_fruit_88_", "jack_fruit_88_", "pineapples"]
    >>> identify_duplicates(strings_before, strings_after)
    {'jack_fruit_88_': ['Jack Fruit 88.', 'Jack!Fruit!88!']}
    """
    # check if original_strings is a list of strings
    if not isinstance(original_strings, list) or not all(isinstance(element, str) for element in original_strings):
        raise TypeError("original_strings must be a list of strings.")
    
    # check if standardized_strings is a list of strings
    if not isinstance(standardized_strings, list) or not all(isinstance(element, str) for element in standardized_strings):
        raise TypeError("standardized_strings must be a list of strings.")
    
    # check if original_strings and standardized_strings are the same length
    if len(original_strings) != len(standardized_strings):
        raise ValueError("Both inputs must be of the same length.")
    
    # Map standardized names to original names
    duplicates = defaultdict(list)

    for orig, std in zip(original_strings, standardized_strings):
        duplicates[std].append(orig)

    # Filter to keep only those with multiple original columns mapping to the same standardized name
    duplicates = {key: value for key, value in duplicates.items() if len(value) > 1}

    return duplicates

def column_name_standardizer(df):
    """
    Returns a copy of the inputted dataframe with standardized column names.
    Column names will be converted to lowercase and
    non-alphanumerics (including spaces and punctuation) will be replaced with underscores.

    If the standardization results in duplicate column names, a warning will be raised.

    Parameters
    ----------
    df : pandas DataFrame
        The input pandas DataFrame whose column names need standardization.
    
    Warnings
    --------
    UserWarning :
        If any of the standardized column names are the same.
    
    Raises
    ------
    TypeError:
        If the input dataframe is not a pandas DataFrame.

    Returns
    -------
    pandas.DataFrame :
        A new DataFrame with standardized column names.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'Jack Fruit 88': [1, 2], 'PINEAPPLES': [3, 4], 'Dragon (Fruit)': [25, 30]}
    >>> df = pd.DataFrame(data)
    >>> column_name_standardizer(df)
       jack_fruit_88  pineapples  dragon__fruit_
    0           1          3         25
    1           2          4         30
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The input must be a pandas DataFrame.")

    original_columns = df.columns.tolist()
    standardized_columns = [string_standardizer(col) for col in original_columns]

    duplicates = resulting_duplicates(original_columns, standardized_columns)

    if bool(duplicates):
        import warnings
        warnings.warn(f"Duplicate column names found after standardization: {duplicates}")

    standardized_df = df.copy()
    standardized_df.columns = standardized_columns
    return standardized_df
