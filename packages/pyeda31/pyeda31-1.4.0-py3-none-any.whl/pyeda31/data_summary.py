import pandas as pd

def get_summary_statistics(df, col = None):
    """
    Generate summary statistics for specified columns or all columns if none are provided.

    This function will return the important statistics (including mean, min, max, median, mode, and range) for numeric columns, as well as
    key metrics (including number of unique values, the most frequent value, and its corresponding frequency) for non-numeric columns.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the data for analysis.
    col : list or None
        A list of column names for which to get statistics. 
        Default value is None, the function will apply for all columns.

    Returns
    ----------
    pd.DataFrame
        A DataFrame with summary statistics for the specified columns, including mean, min, max, median, mode, and range for numeric columns, as well as number of unique values, the most frequent value, and its corresponding frequency) for non-numeric columns.
    
    Examples
    --------
    >>> from pyeda31.data_summary import get_summary_statistics
    >>> get_summary_statistics(df)
    """
    if col is None:
        col = df.columns.tolist()

    summary_stats = {}

    for column in col:
        if column not in df.columns:
            raise KeyError(f"Column '{column}' does not exist in the dataframe.")

        if pd.api.types.is_numeric_dtype(df[column]):
            summary_stats[column] = {
                "mean": df[column].mean(),
                "min": df[column].min(),
                "max": df[column].max(),
                "median": df[column].median(),
                "mode": df[column].mode().iloc[0] if not df[column].mode().empty else None,
                "range": df[column].max() - df[column].min(),
            }
        
        else:
            summary_stats[column] = {
                "num_unique_values": df[column].nunique(),
                "most_frequent_value": df[column].value_counts().idxmax() if not df[column].value_counts().empty else None,
                "frequency_of_most_frequent_value": df[column].value_counts().max() if not df[column].value_counts().empty else None,
            }

    summary_df = pd.DataFrame(summary_stats)

    return summary_df