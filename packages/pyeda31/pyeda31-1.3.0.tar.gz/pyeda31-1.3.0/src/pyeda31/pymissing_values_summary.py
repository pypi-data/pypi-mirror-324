import pandas as pd


def missing_values_summary(df):
    """
    This function is to provide a summary of missing values in the dataset as a Series.

    Parameters
    ----------
    df (pd.DataFrame): The DataFrame containing the data.

    Returns
    -------
    pd.Series: A Series showing the count and percentage of missing values.

    Examples
    --------
    >>> from pyeda31.pymissing_value import missing_values_summary
    >>> missing_values_summary(df)
    """
    # Calculate the count of missing values for each column
    missing_count = df.isnull().sum()
    
    # Calculate the percentage of missing values for each column
    missing_percentage = (missing_count / len(df)) * 100

    # Combine count and percentage into a Series, filtering out columns with no missing values
    missing_summary = missing_count[missing_count > 0].astype(str) + " (" + \
                      missing_percentage[missing_count > 0].round(2).astype(str) + "%)"

    missing_summary.name = "Missing Count (Percentage)"
    return missing_summary.sort_values(ascending=False) 

