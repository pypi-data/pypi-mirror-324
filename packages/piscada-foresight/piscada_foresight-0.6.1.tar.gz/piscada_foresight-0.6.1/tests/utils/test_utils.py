import json
from pathlib import Path
from typing import cast

import pandas as pd


def load_file_content(filename: str):
    """
    Load content from a text, JSON, or GraphQL file located in the test_config directory.

    Args:
        filename (str): The name of the file to load, including its extension.

    Returns:
        dict | str: Parsed JSON data if the file is a JSON file, or raw string content for other files.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is unsupported.
    """
    # Resolve the file path in the test_config directory
    config_path = Path(__file__).parent / "../test_config" / filename

    # Check if the file exists
    if not config_path.exists():
        raise FileNotFoundError(f"File not found: {config_path.resolve()}")

    # Determine file type by extension and load content accordingly
    file_extension = config_path.suffix.lower()

    with config_path.open("r", encoding="utf-8") as file:
        if file_extension == ".json":
            # Load and return JSON data
            return json.load(file)
        elif file_extension in {".txt", ".graphql"}:
            # Load and return plain text content
            return file.read()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """
    Save a DataFrame to a CSV file with microsecond precision.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        path (str): The file path where the DataFrame will be saved.
    """
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    df.to_csv(save_path, index=True, date_format="%Y-%m-%dT%H:%M:%S.%f%z")


def load_dataframe(path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file and ensure the index is timezone-aware (UTC).

    Parameters:
        path (str): The file path from which the DataFrame will be loaded.

    Returns:
        pd.DataFrame: The loaded DataFrame with a timezone-aware index.
    """
    save_path = Path(path)
    if not save_path.exists():
        raise FileNotFoundError(f"File not found: {save_path}")

    df = pd.read_csv(save_path, index_col=0, parse_dates=True)
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("Index is not a DatetimeIndex")
    df.index = cast(pd.DatetimeIndex, df.index)
    # Ensure the index is tz-aware (UTC)
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")

    return df


def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    """
    Compare two DataFrames by flooring their indexes to the nearest second to avoid fractional second mismatches.

    Parameters:
        df1 (pd.DataFrame): The first DataFrame to compare.
        df2 (pd.DataFrame): The second DataFrame to compare.

    Raises:
        AssertionError: If the DataFrames are not equal.
    """

    if not isinstance(df1.index, pd.DatetimeIndex):
        raise TypeError("df1.index is not a DatetimeIndex")
    df1.index = cast(pd.DatetimeIndex, df1.index)

    if not isinstance(df2.index, pd.DatetimeIndex):
        raise TypeError("df2.index is not a DatetimeIndex")
    df2.index = cast(pd.DatetimeIndex, df2.index)

    df1.index = df1.index.floor("S")
    df2.index = df2.index.floor("S")

    pd.testing.assert_frame_equal(df1, df2, check_dtype=False, check_exact=False)
