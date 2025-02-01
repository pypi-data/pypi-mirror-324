def determine_orient(json_data):
    """
    Automatically determines the appropriate orient for pandas.read_json based on the structure of the JSON data.

    Parameters:
    -----------
    json_data : dict or list
        The JSON data to analyze. It can be a dictionary or a list.

    Returns:
    --------
    str
        The appropriate orient value for pandas.read_json. Possible values are:
        - 'records'
        - 'split'
        - 'values'
        - 'index'
        - 'columns'

    Orient Formats and Examples:
    ----------------------------
    1. 'records':
       The JSON data is a list of dictionaries, where each dictionary represents a row.
       Example:
       [
           { "name": "John Doe", "age": 30, "city": "New York" },
           { "name": "Jane Smith", "age": 25, "city": "Chicago" },
           { "name": "Sam Brown", "age": 35, "city": "Los Angeles" }
       ]

    2. 'split':
       The JSON data is a dictionary with keys 'index', 'columns', and 'data'.
       Example:
       {
           "index": [0, 1, 2],
           "columns": ["name", "age", "city"],
           "data": [
               ["John Doe", 30, "New York"],
               ["Jane Smith", 25, "Chicago"],
               ["Sam Brown", 35, "Los Angeles"]
           ]
       }

    3. 'values':
       The JSON data is a list of lists, where each inner list represents a row.
       Example:
       [
           [1, "John Doe", 30, true],
           [2, "Jane Smith", 25, false],
           [3, "Sam Brown", 35, true]
       ]

    4. 'index':
       The JSON data is a dictionary of dictionaries, where the outer keys are row indices and the inner dictionaries represent rows.
       Example:
       {
           "0": { "name": "John Doe", "age": 30, "city": "New York" },
           "1": { "name": "Jane Smith", "age": 25, "city": "Chicago" },
           "2": { "name": "Sam Brown", "age": 35, "city": "Los Angeles" }
       }

    5. 'columns':
       The JSON data is a dictionary of lists, where each key represents a column and the values are the column data.
       Example:
       {
           "name": ["John Doe", "Jane Smith", "Sam Brown"],
           "age": [30, 25, 35],
           "city": ["New York", "Chicago", "Los Angeles"]
       }

    Notes:
    ------
    - If the JSON data does not match any of the above formats, the function defaults to 'columns'.
    - For deeply nested JSON structures, consider flattening the data before using this function.
    """
    if isinstance(json_data, list):
        # Check if it's a list of dictionaries (records format)
        if all(isinstance(item, dict) for item in json_data):
            return "records"
    elif isinstance(json_data, dict):
        # Check for 'split' format
        if all(key in json_data for key in ["index", "columns", "data"]):
            return "split"
        # Check for 'index' format
        elif all(isinstance(value, dict) for value in json_data.values()):
            return "index"
        # Check for 'columns' format
        elif all(isinstance(value, list) for value in json_data.values()):
            return "columns"
        # Check for 'values' format (list of lists)
        elif isinstance(next(iter(json_data.values())), list) and not isinstance(
            next(iter(json_data.values()))[0], dict
        ):
            return "values"
    # Default to 'columns' if no specific format is detected
    return "columns"
