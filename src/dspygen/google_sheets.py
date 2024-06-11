import gspread
from google.oauth2.service_account import Credentials

from dspygen.utils.file_tools import project_dir

def show_all_sheet_data(sheet):
    """
    Prints all data from the given sheet.
    """
    all_data = sheet.get_all_values()
    for row in all_data:
        print(row)


def get_row_data(sheet, row_number):
    """
    Retrieves data from a specific row in the sheet.
    """
    row_data = sheet.row_values(row_number)
    print(f"Data in row {row_number}: {row_data}")
    return row_data


def get_column_data(sheet, column_number):
    """
    Retrieves data from a specific column in the sheet.
    """
    column_data = sheet.col_values(column_number)
    print(f"Data in column {column_number}: {column_data}")
    return column_data


def add_new_row_data(sheet, data):
    """
    Adds a new row of data to the sheet.
    """
    sheet.append_row(data)


def update_cell(sheet, row, column, value):
    """
    Updates a specific cell in the sheet.
    """
    sheet.update_cell(row, column, value)


def create_log_sheet(workbook):
    """
    Creates a new log sheet in the workbook if it does not already exist.
    """
    try:
        sheet_list = workbook.worksheets()
        sheet_names = [sheet.title for sheet in sheet_list]
        if "logsheet" not in sheet_names:
            workbook.add_worksheet(title="logsheet", rows="100", cols="20")
            print("Logsheet created successfully.")
        else:
            print("Logsheet exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
