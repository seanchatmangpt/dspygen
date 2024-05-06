import os

from dspygen.utils.pydantic_tools import InstanceMixin


class DataWriter:
    def __init__(self, data, file_path="", write_options=None):
        if write_options is None:
            write_options = {}
        self.file_path = file_path
        self.df = pd.DataFrame(data)
        self.write_options = write_options

    def get_file_path(self):
        context_generator = DataFrameContextGenerator()
        context_string = context_generator.generate_context(self.df)

        inst = FileNameModel.to_inst("Create a filename that fits \n" + context_string)
        return inst.file_name

    def forward(self, **kwargs):
        if not self.file_path:
            self.file_path = self.get_file_path()

        _, file_extension = os.path.splitext(self.file_path)
        file_extension = file_extension.lower()

        write_functions = {
            '.csv': self.df.to_csv,
            # Add more mappings for different file types
        }

        if file_extension in write_functions:
            write_function = write_functions[file_extension]
            try:
                write_function(self.file_path, **self.write_options)
            except Exception as e:
                raise ValueError(f"Failed to write to {self.file_path} due to: {e}")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


from pydantic import BaseModel, Field
import pandas as pd
from typing import List, Dict, Any
from io import StringIO


class DataFrameContextGenerator(BaseModel):
    descriptive_stats: bool = True
    dtypes_info: bool = True
    context: str = ""

    class Config:
        arbitrary_types_allowed = True

    def generate_context(self, df) -> str:
        # Convert the input data to a pandas DataFrame

        # Initialize a buffer for DataFrame info
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()

        context_parts = []

        # Optionally include descriptive statistics
        if self.descriptive_stats:
            desc_stats = df.describe().to_string()
            context_parts.append(desc_stats)

        # Optionally include data types information
        if self.dtypes_info:
            dtypes_str = df.dtypes.to_string()
            context_parts.append(dtypes_str)

        # Concatenate all parts to form the complete context
        context = "\n".join(context_parts)
        self.context = context
        return self.context


class FileNameModel(BaseModel, InstanceMixin):
    file_name: str = Field(..., description="Unique CSV filename based on the data provided.")
    extension: str = Field("csv", description="File extension for the output file.")


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()
    # Example Usage
    # data = [
    #     {'Date': '2023-01-01', 'Temperature': 22, 'Humidity': 80},
    #     {'Date': '2023-01-02', 'Temperature': 25, 'Humidity': 75},
    #     {'Date': '2023-01-03', 'Temperature': 21, 'Humidity': 85},
    # ]

    data = {
        'Book Title': ['The Great Gatsby', '1984', 'Brave New World', 'The Catcher in the Rye'],
        'Author': ['F. Scott Fitzgerald', 'George Orwell', 'Aldous Huxley', 'J.D. Salinger'],
        'Price': [10.99, 9.99, 8.99, 12.99],
        'Sold Copies': [500, 800, 650, 450]
    }

    # DataWriter(data).forward()
    from dspygen.rm.data_retriever import DataRetriever
    print(DataRetriever("/Users/sac/dev/dspygen/src/dspygen/writer/Book_Title_Author_Price_Sold_Copies.csv").forward())


# Usage example
if __name__ == "__main__":
    main()
#     file_path = 'output_data.csv'
#     data = pd.DataFrame({'id': [1, 2], 'value': ['A', 'B']})
#     writer = DataWriter(file_path, data)
#     writer.write()
#

