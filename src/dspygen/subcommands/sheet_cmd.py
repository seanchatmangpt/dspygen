"""sheet"""
import typer

from dspygen.rm.google_sheets_retriever import GoogleSheetRetriever
from dspygen.writer.google_sheets_writer import GoogleSheetWriter

app = typer.Typer()


@app.command(name="read")
def retrieve_data(sheet_id: str = "10aU_0JoXzHyfq4_YCMDMqdiJGuLAdwiAq9PSegI53YI",
                  sheet_name: str = "Sheet1",
                  query: str = "SELECT * FROM df",
                  k: int = 3):
    """Retrieve data from Google Sheet and print as JSON."""
    # from dspygen.utils.dspy_tools import init_ol
    # init_ol()
    #
    from dspygen.rm.google_sheets_retriever import GoogleSheetRetriever
    gsr = GoogleSheetRetriever(spreadsheet_id=sheet_id, sheet_name=sheet_name)
    result = gsr.forward(query=query, k=k)
    import json
    print(json.dumps(result))


@app.command(name="create")
def create(sheet_id: str = "1ybh9g143P_cQk5Mz73ogsXrK0dWrquJut5XX7QVY3oI",
           sheet_name: str = "Sheet1"):
    # Sample data
    data = {
        'Book Title': ['The Great Gatsby', '1984', 'Brave New World', 'The Catcher in the Rye'],
        'Author': ['F. Scott Fitzgerald', 'George Orwell', 'Aldous Huxley', 'J.D. Salinger'],
        'Price': [10.99, 9.99, 8.99, 12.99],
        'Sold Copies': [500, 800, 650, 450]
    }

    # Initialize GoogleSheetWriter and write data to the Google Sheet
    writer = GoogleSheetWriter(data, sheet_id, sheet_name)
    writer.write()

    # Initialize GoogleSheetRetriever and read data from the Google Sheet
    gs_retriever = GoogleSheetRetriever(sheet_id, sheet_name)
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

