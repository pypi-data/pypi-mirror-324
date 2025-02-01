import pandas as pd


def CsvLoader(csv_file_name, n=5, **kwargs):
    """
    Reads a CSV file into a Pandas DataFrame and returns the first `n` rows.

    Parameters:
    -----------
    csv_file_name : str
        The name or path of the CSV file to read.

    n : int, optional, default: 5
        The number of rows to return from the top of the DataFrame.

    *args : tuple
        Additional positional arguments to pass to `pandas.read_csv`.

    **kwargs : dict
        Additional keyword arguments to pass to `pandas.read_csv`.
        Common arguments include:
        - sep : str, default ','
            Delimiter to use (e.g., ',' for CSV).
        - header : int, list of int, default 0
            Row number(s) to use as column names.
        - index_col : int, str, or list, default None
            Column(s) to use as the row index.
        - usecols : list, default None
            Columns to read from the file.
        - dtype : dict, default None
            Data types for specific columns.
        - na_values : scalar, str, or list, default None
            Additional strings to recognize as NaN.

    Returns:
    --------
    pandas.DataFrame
        The first `n` rows of the DataFrame created from the CSV file.

    Example:
    --------
    # Read a CSV file and return the first 5 rows
    df = read_csv('data.csv')

    # Read specific columns from a CSV file
    df = read_csv('data.csv', usecols=['name', 'age'])

    # Read a CSV file with a specific column as the index
    df = read_csv('data.csv', index_col='id')
    """

    # Read the CSV file with any additional arguments
    df = pd.read_csv(csv_file_name, **kwargs)
    df_head = df.head(n)
    # Return the first `n` 5 rows
    return df_head
