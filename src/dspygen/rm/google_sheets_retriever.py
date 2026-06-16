from typing import Any, Optional

import dspy
import gspread
import pandas as pd
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
from pandasql import sqldf


def apply_sql_to_dataframe(df: pd.DataFrame, query: str) -> pd.DataFrame:
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
    def __init__(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        client: gspread.Client | None = None,
        query: str = "",
        return_columns: list[str] | None = None,
        pipeline: Any = None,
        step: Any = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the GoogleSheetRetriever with explicit dependency injection.

        Args:
            spreadsheet_id: The Google Sheets spreadsheet key/ID.
            sheet_name: Name of the worksheet tab to read.
            client: An authenticated ``gspread.Client`` instance. When *None*,
                ``gspread.oauth()`` is used as a default (service-account
                credentials are also supported via ``gspread.service_account()``).
            query: Optional initial SQL filter applied at construction time.
            return_columns: Subset of columns to include in results.
            pipeline: Optional pipeline object for context propagation.
            step: Optional pipeline step reference.
        """
        super().__init__()
        if return_columns is None:
            return_columns = []

        self.pipeline = pipeline
        self.step = step
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.return_columns = return_columns

        # Explicit injection: use the provided client or fall back to oauth.
        if client is None:
            client = gspread.oauth()
        self.client: gspread.Client = client

        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
        except SpreadsheetNotFound as exc:
            raise SpreadsheetNotFound(
                f"Spreadsheet not found: {spreadsheet_id!r}. "
                "Check the ID and that the service account has access."
            ) from exc
        except APIError as exc:
            raise APIError(
                f"Google Sheets API error while opening {spreadsheet_id!r}: {exc}"
            ) from exc

        try:
            self.sheet = spreadsheet.worksheet(sheet_name)
        except WorksheetNotFound as exc:
            raise WorksheetNotFound(
                f"Worksheet {sheet_name!r} not found in spreadsheet {spreadsheet_id!r}."
            ) from exc

        # Read all records with FORMATTED_VALUE to get human-readable cell values.
        try:
            records = self.sheet.get_all_records(value_render_option="FORMATTED_VALUE")
        except APIError as exc:
            raise APIError(
                f"Failed to read records from {sheet_name!r}: {exc}"
            ) from exc

        self.df = pd.DataFrame(records)

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
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    sheet_id = "10aU_0JoXzHyfq4_YCMDMqdiJGuLAdwiAq9PSegI53YI"
    sheet_name = 'Sheet1'

    gsr = GoogleSheetRetriever(sheet_id, sheet_name)
    print(gsr.forward())


if __name__ == '__main__':
    main()
