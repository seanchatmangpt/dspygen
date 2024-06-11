import gspread
from google.oauth2.service_account import Credentials
import inject
import pandas as pd

from dspygen.rm.google_sheets_retriever import GoogleSheetRetriever
from dspygen.utils.file_tools import project_dir


class GoogleSheetWriter:
    @inject.autoparams()
    def __init__(self, data, spreadsheet_id, sheet_name, client: gspread.Client):
        self.client = client
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(sheet_name)

        # Convert the input data to a pandas DataFrame
        self.df = pd.DataFrame(data)

    def write(self):
        self.sheet.clear()  # Clear the sheet before writing new data
        self.sheet.update([self.df.columns.values.tolist()] + self.df.values.tolist())  # Update the sheet with new data

    def append_row(self, data):
        self.sheet.append_row(data)

    def update_cell(self, row, column, value):
        self.sheet.update_cell(row, column, value)

    def delete_row(self, row):
        self.sheet.delete_rows(row)



def main():
    sheet_id = "10aU_0JoXzHyfq4_YCMDMqdiJGuLAdwiAq9PSegI53YI"
    sheet_name = "Sheet1"
    credentials_json = str(project_dir() / "credentials.json")

    # Set up Google Sheets API credentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(credentials_json, scopes=scopes)

    # Sample data
    data = {
        'Book Title': ['The Great Gatsby', '1984', 'Brave New World', 'The Catcher in the Rye'],
        'Author': ['F. Scott Fitzgerald', 'George Orwell', 'Aldous Huxley', 'J.D. Salinger'],
        'Price': [10.99, 9.99, 8.99, 12.99],
        'Sold Copies': [500, 800, 650, 450]
    }

    # Initialize GoogleSheetWriter and write data to the Google Sheet
    writer = GoogleSheetWriter(data, sheet_id, sheet_name, credentials=creds)
    writer.write()

    # Initialize GoogleSheetRetriever and read data from the Google Sheet
    gs_retriever = GoogleSheetRetriever(sheet_id, sheet_name, credentials=creds)
    print("Data in Google Sheet:")
    print(gs_retriever.forward())

    # Append a new row to the Google Sheet
    new_row = ['To Kill a Mockingbird', 'Harper Lee', 11.99, 600]
    writer.append_row(new_row)

    # Update a cell in the Google Sheet
    writer.update_cell(2, 3, 20.99)  # Update Price of the first book

    # Read data after updates
    print("Data after updates:")
    print(gs_retriever.forward())

    # Delete a row from the Google Sheet
    writer.delete_row(2)  # Delete the second row

    # Read data after deletion
    print("Data after deletion:")
    print(gs_retriever.forward())


if __name__ == "__main__":
    main()
