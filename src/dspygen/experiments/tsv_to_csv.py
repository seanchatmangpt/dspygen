import os
import csv
from pathlib import Path


def get_latest_file(directory, extension):
    """Gets the latest file with the given extensions from the specified directory."""
    files = list(Path(directory).glob(f"*{extension}"))
    if not files:
        raise FileNotFoundError(f"No files with extensions {extension} found in {directory}")
    latest_file = max(files, key=os.path.getctime)
    return latest_file


def tsv_to_csv(tsv_filepath):
    """Converts a TSV file to a CSV file."""
    csv_filepath = tsv_filepath.with_suffix('.csv')

    with open(tsv_filepath, 'r') as tsvfile, open(csv_filepath, 'w', newline='') as csvfile:
        tsv_reader = csv.reader(tsvfile, delimiter='\t')
        csv_writer = csv.writer(csvfile)

        for row in tsv_reader:
            csv_writer.writerow(row)

    print(f"CSV file saved as {csv_filepath}")


if __name__ == "__main__":
    # Define the directory to search for the latest TSV file (Desktop in this case)
    desktop_directory = Path("~/Desktop").expanduser()

    try:
        # Find the latest TSV file on the Desktop
        latest_tsv = get_latest_file(desktop_directory, ".tsv")
        print(f"Latest TSV file found: {latest_tsv}")

        # Convert the latest TSV file to CSV
        tsv_to_csv(latest_tsv)

    except FileNotFoundError as e:
        print(e)
