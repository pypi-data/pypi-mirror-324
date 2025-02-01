import pytest
import pandas as pd
import json
from AutoGenix_ETL.JSONLoader import JSONLoader
from AutoGenix_ETL.determine_orient import determine_orient


def test_jsonloader_records_format():
    data = [
        {"name": "John Doe", "age": 30, "city": "New York"},
        {"name": "Jane Smith", "age": 25, "city": "Chicago"},
    ]
    file_path = "test_records.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    df = JSONLoader(file_path)
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["name", "age", "city"]


def test_jsonloader_split_format():
    data = {
        "index": [0, 1],
        "columns": ["name", "age", "city"],
        "data": [["John Doe", 30, "New York"], ["Jane Smith", 25, "Chicago"]],
    }
    file_path = "test_split.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    df = JSONLoader(file_path)
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["name", "age", "city"]


def test_jsonloader_columns_format():
    data = {
        "name": ["John Doe", "Jane Smith"],
        "age": [30, 25],
        "city": ["New York", "Chicago"],
    }
    file_path = "test_columns.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    df = JSONLoader(file_path)
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["name", "age", "city"]


def test_jsonloader_empty_file():
    file_path = "empty.json"
    with open(file_path, "w") as file:
        file.write("")

    with pytest.raises(json.JSONDecodeError):
        JSONLoader(file_path)


def test_jsonloader_invalid_json():
    file_path = "invalid.json"
    with open(file_path, "w") as file:
        file.write("{invalid: json data}")

    with pytest.raises(json.JSONDecodeError):
        JSONLoader(file_path)


def test_jsonloader_orient_detection():
    data = [
        {"name": "John Doe", "age": 30, "city": "New York"},
        {"name": "Jane Smith", "age": 25, "city": "Chicago"},
    ]
    file_path = "test_orient.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    df = JSONLoader(file_path)
    orient = determine_orient(data)
    assert not df.empty
    assert orient == "records"
    assert len(df) == 2
    assert list(df.columns) == ["name", "age", "city"]
