import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional, Union

import dspy
import pandas as pd
from pandasql import sqldf


# Function to apply an SQL query to a DataFrame
def apply_sql_to_dataframe(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    This function applies an SQL query to the given DataFrame.

    Parameters:
    - df: pandas DataFrame.
    - query: SQL query as a string.

    Returns:
    - DataFrame containing the result of the SQL query.
    """
    # Dynamically add the DataFrame to the local scope with the name 'df'
    local_env = locals()
    local_env["df"] = df
    return sqldf(query, local_env)


@contextmanager
def _sqlite_connection(filepath: str | Path) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for a SQLite connection that ensures cleanup on exit."""
    conn = sqlite3.connect(str(filepath))
    try:
        yield conn
    finally:
        conn.close()


def read_any(filepath: str | Path, query: str, read_options: dict[str, Any] | None = None) -> pd.DataFrame:
    """Read a data file of any supported type and return a DataFrame.

    For .sql / .db files, ``query`` is executed via ``pd.read_sql_query``.
    For all other types the file is loaded with the appropriate pandas reader
    and ``read_options`` are forwarded as keyword arguments.

    Args:
        filepath: Path to the data file.
        query: SQL query string (used only for .sql / .db files).
        read_options: Extra keyword arguments forwarded to the pandas reader.
            For .sql / .db files, a ``params`` key is passed to
            ``pd.read_sql_query`` if present.

    Returns:
        DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If *filepath* does not exist.
        ValueError: If the file type is unsupported or reading fails.
        sqlite3.Error: If the SQLite query execution fails.
    """
    if read_options is None:
        read_options = {}

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    file_extension = path.suffix.lower()

    read_functions: dict[str, Any] = {
        '.csv': pd.read_csv,
        '.xls': pd.read_excel,
        '.xlsx': pd.read_excel,
        '.pickle': pd.read_pickle,
        '.pkl': pd.read_pickle,
        '.h5': pd.read_hdf,
        '.hdf': pd.read_hdf,
        '.sql': pd.read_sql,  # Connection argument needed here.
        '.db': pd.read_sql,   # Connection argument needed here.
        '.json': pd.read_json,
        '.parquet': pd.read_parquet,
        '.orc': pd.read_orc,
        '.feather': pd.read_feather,
        '.gbq': pd.read_gbq,  # Requires additional args like project_id.
        '.html': pd.read_html,  # Returns a list of DataFrames.
        '.xml': pd.read_xml,
        '.stata': pd.read_stata,
        '.sas': pd.read_sas,  # Might require additional arguments.
        '.sav': pd.read_spss,
        '.dta': pd.read_stata,
        '.fwf': pd.read_fwf,  # Might require formatting arguments.
    }

    if file_extension in ('.sql', '.db'):
        try:
            with _sqlite_connection(path) as conn:
                return pd.read_sql_query(query, conn, params=read_options.get('params'))
        except sqlite3.Error as exc:
            raise sqlite3.Error(f"SQLite query failed for {path}: {exc}") from exc

    # Use pyarrow engine for parquet when not explicitly overridden
    if file_extension == '.parquet' and 'engine' not in read_options:
        read_options = {**read_options, 'engine': 'pyarrow'}

    if file_extension in read_functions:
        read_func = read_functions[file_extension]
        try:
            return read_func(str(path), **read_options)
        except (OSError, ValueError) as exc:
            raise ValueError(f"Failed to read {path}: {exc}") from exc
    else:
        raise ValueError(f"Unsupported file type: {file_extension!r}")


class DataRetriever(dspy.Retrieve):
    supported_extensions = [
        '.csv', '.xls', '.xlsx', '.pickle', '.pkl', '.h5', '.hdf',
        '.sql', '.db', '.json', '.parquet', '.orc', '.feather',
        '.gbq', '.html', '.xml', '.stata', '.sas', '.sav', '.dta', '.fwf',
    ]

    def __init__(
        self,
        file_path: str | Path,
        query: str = "",
        return_columns: list[str] | None = None,
        read_options: dict[str, Any] | None = None,
        pipeline: Any = None,
        step: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        if return_columns is None:
            return_columns = []
        if read_options is None:
            read_options = {}

        self.pipeline = pipeline
        self.step = step

        self.file_path = Path(file_path)
        self.return_columns = return_columns
        self.read_options = read_options

        # Read the data using the read_any function
        self.df = read_any(self.file_path, query, read_options)

    @classmethod
    def supports_file_type(cls, file_extension: str) -> bool:
        return file_extension.lower() in cls.supported_extensions

    def forward(self, query: str | None = None, k: int | None = None, **kwargs: Any) -> list[dict]:
        # Check if a SQL query is provided
        if query:
            # Apply the SQL query to the DataFrame
            matches = apply_sql_to_dataframe(self.df, query)
        else:
            matches = self.df

        if k is not None:
            matches = matches.head(k)

        if self.return_columns:
            # Ensure only specified return columns are included in the results
            matches = matches[self.return_columns]

        result = matches.to_dict(orient='records')

        if self.pipeline:
            self.pipeline.context.data = result

        return result


def main() -> None:
    file_path = Path('sample_data.csv')
    query = "SELECT name FROM df WHERE age < 30"  # SQL query to filter data
    return_columns = ['name']

    # Initialize the DataRetriever with the path to your CSV file
    # Note: The query passed here is an SQL query that will be applied to the DataFrame.
    # If your initial reading does not require filtering, you might pass an empty string or adjust accordingly.
    data_retriever = DataRetriever(file_path=file_path, return_columns=return_columns)

    # For demonstration, applying the SQL query using the forward method
    # Normally, you'd integrate your SQL query logic where it fits best in your application flow
    filtered_results = data_retriever.forward(query=query)

    # Print the filtered results
    print("Filtered Results:")
    print(filtered_results)


if __name__ == "__main__":
    main()
