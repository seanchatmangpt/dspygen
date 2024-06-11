import pytest
from unittest import mock
import inject
import gspread

from dspygen.writer.google_sheets_writer import GoogleSheetWriter


@pytest.fixture
def mock_client():
    client = mock.MagicMock(spec=gspread.Client)
    sheet = mock.MagicMock()
    client.open_by_key.return_value.worksheet.return_value = sheet
    return client


def configure_test(binder):
    binder.bind(gspread.Client, mock_client)


@pytest.fixture(autouse=True)
def configure_inject(mock_client):
    inject.clear_and_configure(lambda binder: binder.bind(gspread.Client, mock_client))
    yield
    inject.clear()


def test_write(mock_client):
    data = {
        'Book Title': ['The Great Gatsby'],
        'Author': ['F. Scott Fitzgerald'],
        'Price': [10.99],
        'Sold Copies': [500]
    }
    writer = GoogleSheetWriter(data, 'fake_spreadsheet_id', 'Sheet1')
    writer.write()
    sheet = mock_client.open_by_key.return_value.worksheet.return_value

    # Verify that the sheet was cleared and updated with the data
    sheet.clear.assert_called_once()
    sheet.update.assert_called_once_with([
        ['Book Title', 'Author', 'Price', 'Sold Copies'],
        ['The Great Gatsby', 'F. Scott Fitzgerald', 10.99, 500]
    ])


def test_append_row(mock_client):
    data = {
        'Book Title': ['The Great Gatsby'],
        'Author': ['F. Scott Fitzgerald'],
        'Price': [10.99],
        'Sold Copies': [500]
    }
    writer = GoogleSheetWriter(data, 'fake_spreadsheet_id', 'Sheet1')
    new_row = ['1984', 'George Orwell', 9.99, 800]
    writer.append_row(new_row)
    sheet = mock_client.open_by_key.return_value.worksheet.return_value

    # Verify that the new row was appended
    sheet.append_row.assert_called_once_with(new_row)


def test_update_cell(mock_client):
    data = {
        'Book Title': ['The Great Gatsby'],
        'Author': ['F. Scott Fitzgerald'],
        'Price': [10.99],
        'Sold Copies': [500]
    }
    writer = GoogleSheetWriter(data, 'fake_spreadsheet_id', 'Sheet1')
    writer.update_cell(2, 3, 20.99)
    sheet = mock_client.open_by_key.return_value.worksheet.return_value

    # Verify that the cell was updated
    sheet.update_cell.assert_called_once_with(2, 3, 20.99)


def test_delete_row(mock_client):
    data = {
        'Book Title': ['The Great Gatsby'],
        'Author': ['F. Scott Fitzgerald'],
        'Price': [10.99],
        'Sold Copies': [500]
    }
    writer = GoogleSheetWriter(data, 'fake_spreadsheet_id', 'Sheet1')
    writer.delete_row(2)
    sheet = mock_client.open_by_key.return_value.worksheet.return_value

    # Verify that the row was deleted
    sheet.delete_rows.assert_called_once_with(2)
