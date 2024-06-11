import pytest
from unittest import mock
import inject
import gspread
import pandas as pd

from dspygen.rm.google_sheets_retriever import GoogleSheetRetriever, apply_sql_to_dataframe


# Define the mock client fixture
@pytest.fixture
def mock_client():
    client = mock.MagicMock(spec=gspread.Client)
    sheet = mock.MagicMock()
    client.open_by_key.return_value.worksheet.return_value = sheet

    # Mock data to be returned by get_all_records
    mock_data = [
        {"Author": "George Orwell", "Title": "1984", "Year": 1949},
        {"Author": "George Orwell", "Title": "Animal Farm", "Year": 1945},
        {"Author": "Aldous Huxley", "Title": "Brave New World", "Year": 1932}
    ]

    sheet.get_all_records.return_value = mock_data
    return client


# Configure the injection
def configure_test(binder, mock_client):
    binder.bind(gspread.Client, mock_client)


# Fixture to configure the inject module
@pytest.fixture(autouse=True)
def configure_inject(mock_client):
    inject.clear_and_configure(lambda binder: binder.bind(gspread.Client, mock_client))
    yield
    inject.clear()


def test_retrieve_data(mock_client):
    sheet_id = "fake_spreadsheet_id"
    sheet_name = 'Sheet1'
    query = "SELECT * FROM df WHERE Author = 'George Orwell'"

    retriever = GoogleSheetRetriever(sheet_id, sheet_name)
    results = retriever.forward(query=query)

    expected_results = [
        {"Author": "George Orwell", "Title": "1984", "Year": 1949},
        {"Author": "George Orwell", "Title": "Animal Farm", "Year": 1945}
    ]

    sheet = mock_client.open_by_key.return_value.worksheet.return_value

    # Verify that data was retrieved and processed correctly
    sheet.get_all_records.assert_called_once()
    assert results == expected_results


# Example usage of apply_sql_to_dataframe
def test_apply_sql_to_dataframe():
    mock_data = [
        {"Author": "George Orwell", "Title": "1984", "Year": 1949},
        {"Author": "George Orwell", "Title": "Animal Farm", "Year": 1945},
        {"Author": "Aldous Huxley", "Title": "Brave New World", "Year": 1932}
    ]
    df = pd.DataFrame(mock_data)
    query = "SELECT * FROM df WHERE Author = 'George Orwell'"

    result_df = apply_sql_to_dataframe(df, query)
    expected_df = pd.DataFrame([
        {"Author": "George Orwell", "Title": "1984", "Year": 1949},
        {"Author": "George Orwell", "Title": "Animal Farm", "Year": 1945}
    ])

    pd.testing.assert_frame_equal(result_df, expected_df)
