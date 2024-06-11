import pytest
from unittest.mock import MagicMock, patch
from dspygen.google_sheets import (
    show_all_sheet_data,
    get_row_data,
    get_column_data,
    add_new_row_data,
    update_cell
)


@pytest.fixture
def mock_sheet(mocker):
    mock_sheet = mocker.MagicMock()
    mock_sheet.get_all_values.return_value = [["Name", "Age", "City"], ["Alice", "30", "New York"]]
    mock_sheet.row_values.return_value = ["Alice", "30", "New York"]
    mock_sheet.col_values.return_value = ["Name", "Alice"]
    return mock_sheet


def test_show_all_sheet_data(mock_sheet, mocker):
    mocker.patch('dspygen.google_sheets.client.open_by_key').return_value.sheet1 = mock_sheet
    sheet = mock_sheet
    show_all_sheet_data(sheet)
    mock_sheet.get_all_values.assert_called_once()


def test_get_row_data(mock_sheet, mocker):
    mocker.patch('dspygen.google_sheets.client.open_by_key').return_value.sheet1 = mock_sheet
    sheet = mock_sheet
    row_data = get_row_data(sheet, 2)
    assert row_data == ["Alice", "30", "New York"]
    mock_sheet.row_values.assert_called_once_with(2)


def test_get_column_data(mock_sheet, mocker):
    mocker.patch('dspygen.google_sheets.client.open_by_key').return_value.sheet1 = mock_sheet
    sheet = mock_sheet
    column_data = get_column_data(sheet, 1)
    assert column_data == ["Name", "Alice"]
    mock_sheet.col_values.assert_called_once_with(1)


def test_add_new_row_data(mock_sheet, mocker):
    mocker.patch('dspygen.google_sheets.client.open_by_key').return_value.sheet1 = mock_sheet
    sheet = mock_sheet
    new_data = ["Bob", "25", "Los Angeles"]
    add_new_row_data(sheet, new_data)
    mock_sheet.append_row.assert_called_once_with(new_data)


def test_update_cell(mock_sheet, mocker):
    mocker.patch('dspygen.google_sheets.client.open_by_key').return_value.sheet1 = mock_sheet
    sheet = mock_sheet
    update_cell(sheet, 2, 2, "Updated Value")
    mock_sheet.update_cell.assert_called_once_with(2, 2, "Updated Value")
