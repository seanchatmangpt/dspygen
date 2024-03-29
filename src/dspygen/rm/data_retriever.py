import sqlite3
from pathlib import Path

import dspy
import pandas as pd
import os

from pandasql import sqldf


# Function to apply an SQL query to a DataFrame
def apply_sql_to_dataframe(df, query):
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


def read_any(filepath, query, read_options=None):
    if read_options is None:
        read_options = {}
    _, file_extension = os.path.splitext(filepath)
    file_extension = file_extension.lower()
    read_functions = {
        '.csv': pd.read_csv,
        '.xls': pd.read_excel,
        '.xlsx': pd.read_excel,
        '.pickle': pd.read_pickle,
        '.pkl': pd.read_pickle,
        '.h5': pd.read_hdf,
        '.hdf': pd.read_hdf,
        '.sql': pd.read_sql,  # Connection argument needed here.
        '.db': pd.read_sql,  # Connection argument needed here.
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

    if file_extension == '.sql' or file_extension == '.db':
        connection = sqlite3.connect(filepath)
        # Updated to pass 'params' from read_options to pd.read_sql_query
        df = pd.read_sql_query(query, connection, params=read_options.get('params', None))
        connection.close()
        return df

    if file_extension in read_functions:
        read_func = read_functions[file_extension]
        try:
            return read_func(filepath, **read_options)
        except Exception as e:
            raise ValueError(f"Failed to read {filepath} due to: {e}")
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


class DataRetriever(dspy.Retrieve):
    def __init__(self, file_path: str | Path, query: str = "", return_columns=None,
                 read_options=None, pipeline=None, step=None, **kwargs):
        super().__init__()
        if return_columns is None:
            return_columns = []
        if read_options is None:
            read_options = {}

        self.pipeline = pipeline
        self.step = step

        self.file_path = str(file_path)
        self.return_columns = return_columns
        self.read_options = read_options

        # Read the data using the read_any function
        self.df = read_any(file_path, query, read_options)  # No SQL query here

    def forward(self, query: str = None, k: int = None, **kwargs) -> list[dict]:
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


def main():
    file_path = 'sample_data.csv'
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
