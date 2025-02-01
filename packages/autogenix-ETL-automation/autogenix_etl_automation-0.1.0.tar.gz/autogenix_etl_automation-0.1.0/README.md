# Autogenix ETL Automation

## Overview

**Autogenix ETL Automation** is a Python package designed to simplify and automate Extract, Transform, and Load (ETL) processes. With built-in modules for loading and processing CSV and JSON data, this package provides essential tools for efficient data handling and transformation.

## Features

- **CSV Loader:** Easily load CSV files into Pandas DataFrames with customizable options.
- **JSON Loader:** Automatically detect the appropriate orientation for JSON data and load it into DataFrames.
- **Dynamic Orient Detection:** Analyze the structure of JSON data to determine the optimal loading strategy.

## Installation

```bash
pip install autogenix-etl-automation
```

## Requirements

- Python >= 3.6
- pandas

## Usage

### CSV Loader
The `CsvLoader` function reads a CSV file and returns the first `n` rows.

#### Example

```python
from autogenix_etl.CsvLoader import CsvLoader

# Load a CSV file and return the first 5 rows
df = CsvLoader("data.csv")
print(df)

# Load a CSV file with custom delimiter and specific columns
df = CsvLoader("data.csv", sep=';', usecols=['name', 'age'])
print(df)
```

#### Parameters
- **csv_file_name:** The name or path of the CSV file.
- **n:** Number of rows to return (default is 5).
- **kwargs:** Additional arguments passed to `pandas.read_csv()`.

### JSON Loader
The `JSONLoader` function reads JSON data and returns a DataFrame.

#### Example

```python
from autogenix_etl.JSONLoader import JSONLoader

# Load JSON data and return the first 5 rows
df = JSONLoader("data.json")
print(df)
```

#### Parameters
- **file_path:** Path to the JSON file.
- **kwargs:** Additional arguments passed to `pandas.read_json()`.

### JSON Orient Detection
The package intelligently detects the correct orientation for JSON data (`records`, `split`, `index`, `columns`, or `values`) using the `determine_orient` function.

#### Example

```python
from autogenix_etl.determine_orient import determine_orient

# Example JSON data
json_data = [
    {"name": "John Doe", "age": 30, "city": "New York"},
    {"name": "Jane Smith", "age": 25, "city": "Chicago"}
]

orient = determine_orient(json_data)
print(f"Detected orient: {orient}")
```


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author
Rishikeswaran S  
[Email](mailto:rishikeswaran17@gmail.com)  

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

## Acknowledgments
Special thanks to the open-source community for inspiration and support.

