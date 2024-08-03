import os
import pandas as pd
from pydantic import BaseModel, Field
from io import StringIO

class DataWriter:
    def __init__(self, data, file_path="", write_options=None):
        print("init " + file_path)

        if write_options is None:
            write_options = {}
        self.file_path = file_path
        
        # Determine file extension
        _, file_extension = os.path.splitext(self.file_path)
        file_extension = file_extension.lower()

        # Handle different data formats
        if file_extension == '.csv':
            if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
                self.df = pd.DataFrame(data)
            else:
                raise ValueError("For CSV files, data must be a dictionary of lists.")
        elif file_extension == '.md':
            if isinstance(data, str):
                self.md_content = data
            else:
                raise ValueError("For Markdown files, data must be a string.")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        self.write_options = write_options

    def get_file_path(self):
        context_generator = DataFrameContextGenerator()
        context_string = context_generator.generate_context(self.df) if hasattr(self, 'df') else ""

        inst = FileNameModel.to_inst("Create a filename that fits \n" + context_string)
        return inst.file_name

    def forward(self, **kwargs):
        if not self.file_path:
            self.file_path = self.get_file_path()

        _, file_extension = os.path.splitext(self.file_path)
        file_extension = file_extension.lower()

        if file_extension == '.csv':
            write_functions = {
                '.csv': self.df.to_csv,
                # Add more mappings for different file types
            }
            print("write " + self.file_path)
            if file_extension in write_functions:
                write_function = write_functions[file_extension]
                try:
                    write_function(self.file_path, **self.write_options)
                except Exception as e:
                    raise ValueError(f"Failed to write to {self.file_path} due to: {e}")
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")

        elif file_extension == '.md':
            print("write " + self.file_path)
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.md_content)
            except Exception as e:
                raise ValueError(f"Failed to write to {self.file_path} due to: {e}")

        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

class DataFrameContextGenerator(BaseModel):
    descriptive_stats: bool = True
    dtypes_info: bool = True
    context: str = ""

    class Config:
        arbitrary_types_allowed = True

    def generate_context(self, df) -> str:
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()

        context_parts = []

        if self.descriptive_stats:
            desc_stats = df.describe().to_string()
            context_parts.append(desc_stats)

        if self.dtypes_info:
            dtypes_str = df.dtypes.to_string()
            context_parts.append(dtypes_str)

        context = "\n".join(context_parts)
        self.context = context
        return self.context

class FileNameModel(BaseModel):
    file_name: str = Field(..., description="Unique CSV filename based on the data provided.")
    extension: str = Field("csv", description="File extension for the output file.")

def main():
    # Example Usage for CSV
    data_csv = {
        'Book Title': ['The Great Gatsby', '1984', 'Brave New World', 'The Catcher in the Rye'],
        'Author': ['F. Scott Fitzgerald', 'George Orwell', 'Aldous Huxley', 'J.D. Salinger'],
        'Price': [10.99, 9.99, 8.99, 12.99],
        'Sold Copies': [500, 800, 650, 450]
    }
    writer_csv = DataWriter(file_path="./data/Book_Title_Author_Price_Sold_Copies.csv", data=data_csv)
    writer_csv.forward()

    # Example Usage for Markdown
    data_md = "# Book List\n\n- The Great Gatsby\n- 1984\n- Brave New World\n- The Catcher in the Rye"
    writer_md = DataWriter(file_path="./data/Tetris_Blog_Phi3Med.md", data=data_md)
    writer_md.forward()

if __name__ == "__main__":
    main()
