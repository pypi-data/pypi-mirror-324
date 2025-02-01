import unittest
import pandas as pd
from io import StringIO


class TestCsvLoader(unittest.TestCase):
    def setUp(self):
        # Sample CSV content for testing
        self.csv_data = """name,age,city
John,30,New York
Jane,28,Chicago
Sam,35,Los Angeles
Alice,25,Boston
Bob,40,San Francisco
Eve,22,Miami
"""

        # Expected DataFrame for comparison
        self.sample_df = pd.DataFrame(
            {
                "name": ["John", "Jane", "Sam", "Alice", "Bob", "Eve"],
                "age": [30, 28, 35, 25, 40, 22],
                "city": [
                    "New York",
                    "Chicago",
                    "Los Angeles",
                    "Boston",
                    "San Francisco",
                    "Miami",
                ],
            }
        )

    def test_load_csv_default_rows(self):
        """Test loading CSV with default number of rows (5)."""
        csv_file = StringIO(self.csv_data)
        df = CsvLoader(csv_file)
        pd.testing.assert_frame_equal(df, self.sample_df.head(5))  # Check top 5 rows

    def test_load_csv_with_custom_row_count(self):
        """Test loading CSV with a custom row count (3)."""
        csv_file = StringIO(self.csv_data)
        df = CsvLoader(csv_file, n=3)
        pd.testing.assert_frame_equal(df, self.sample_df.head(3))  # Check top 3 rows

    def test_load_csv_with_usecols(self):
        """Test loading CSV with selected columns only."""
        csv_file = StringIO(self.csv_data)
        df = CsvLoader(csv_file, usecols=["name", "city"])
        expected_df = self.sample_df[["name", "city"]]
        pd.testing.assert_frame_equal(
            df, expected_df.head()
        )  # Check for selected columns

    def test_load_csv_with_index_col(self):
        """Test loading CSV with a custom index column."""
        csv_file = StringIO(self.csv_data)
        df = CsvLoader(csv_file, index_col="name")
        expected_df = self.sample_df.set_index("name")
        pd.testing.assert_frame_equal(df, expected_df.head())  # Check for index column

    def test_load_csv_with_custom_separator(self):
        """Test loading CSV with a custom separator ('|')."""
        csv_data = """name|age|city
John|30|New York
Jane|28|Chicago
Sam|35|Los Angeles
"""
        csv_file = StringIO(csv_data)
        df = CsvLoader(csv_file, sep="|")
        expected_df = pd.DataFrame(
            {
                "name": ["John", "Jane", "Sam"],
                "age": [30, 28, 35],
                "city": ["New York", "Chicago", "Los Angeles"],
            }
        )
        pd.testing.assert_frame_equal(df, expected_df)  # Check with custom separator

    def test_load_csv_with_na_values(self):
        """Test loading CSV with custom NA values (empty string treated as NaN)."""
        csv_data = """name,age,city
John,30,New York
Jane,,Chicago
Sam,35,Los Angeles
"""
        csv_file = StringIO(csv_data)
        df = CsvLoader(csv_file, na_values=[""])
        self.assertTrue(
            pd.isna(df.loc[1, "age"])
        )  # Check if 'NaN' is assigned correctly

    def test_load_csv_with_dtype(self):
        """Test loading CSV with specific column data types."""
        csv_data = """name,age,city
John,30,New York
Jane,28,Chicago
Sam,35,Los Angeles
"""
        csv_file = StringIO(csv_data)
        df = CsvLoader(csv_file, dtype={"age": float})
        self.assertEqual(
            df["age"].dtype, float
        )  # Check if the age column is of float type


if __name__ == "__main__":
    unittest.main()
