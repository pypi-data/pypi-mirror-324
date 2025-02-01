import unittest
from AutoGenix_ETL.determine_orient import determine_orient


class TestDetermineOrient(unittest.TestCase):
    def test_records_orient(self):
        json_data = [
            {"name": "John Doe", "age": 30, "city": "New York"},
            {"name": "Jane Smith", "age": 25, "city": "Chicago"},
        ]
        self.assertEqual(determine_orient(json_data), "records")

    def test_split_orient(self):
        json_data = {
            "index": [0, 1],
            "columns": ["name", "age", "city"],
            "data": [["John Doe", 30, "New York"], ["Jane Smith", 25, "Chicago"]],
        }
        self.assertEqual(determine_orient(json_data), "split")

    def test_index_orient(self):
        json_data = {
            "0": {"name": "John Doe", "age": 30, "city": "New York"},
            "1": {"name": "Jane Smith", "age": 25, "city": "Chicago"},
        }
        self.assertEqual(determine_orient(json_data), "index")

    def test_columns_orient(self):
        json_data = {
            "name": ["John Doe", "Jane Smith"],
            "age": [30, 25],
            "city": ["New York", "Chicago"],
        }
        self.assertEqual(determine_orient(json_data), "columns")

    def test_values_orient(self):
        json_data = [[1, "John Doe", 30], [2, "Jane Smith", 25]]
        self.assertEqual(determine_orient(json_data), "values")

    def test_empty_data(self):
        json_data = {}
        self.assertEqual(determine_orient(json_data), "columns")

    def test_nested_data(self):
        json_data = {"name": ["John Doe", {"nested": "value"}]}  # Complex nested case
        self.assertEqual(determine_orient(json_data), "columns")

    def test_mixed_list_dict(self):
        json_data = [{"name": "John Doe"}, [1, 2, 3]]  # Mixed types
        self.assertEqual(determine_orient(json_data), "columns")


if __name__ == "__main__":
    unittest.main()
