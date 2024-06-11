import dspy
import inject
import gspread
import pandas as pd
from pandasql import sqldf


def apply_sql_to_dataframe(df, query):
    """
    This function applies an SQL query to the given DataFrame.

    Parameters:
    - df: pandas DataFrame.
    - query: SQL query as a string.

    Returns:
    - DataFrame containing the result of the SQL query.
    """
    local_env = locals()
    local_env["df"] = df
    return sqldf(query, local_env)


class GoogleSheetRetriever(dspy.Retrieve):
    @inject.autoparams()
    def __init__(self, spreadsheet_id, sheet_name, client: gspread.Client, query="", return_columns=None, pipeline=None, step=None, **kwargs):
        super().__init__()
        if return_columns is None:
            return_columns = []

        self.pipeline = pipeline
        self.step = step

        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.return_columns = return_columns

        self.client = client
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        # Read the data from the Google Sheet
        self.df = pd.DataFrame(self.sheet.get_all_records())

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
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    sheet_id = "10aU_0JoXzHyfq4_YCMDMqdiJGuLAdwiAq9PSegI53YI"
    sheet_name = 'Sheet1'

    gsr = GoogleSheetRetriever(sheet_id, sheet_name)
    print(gsr.forward())


if __name__ == '__main__':
    main()
