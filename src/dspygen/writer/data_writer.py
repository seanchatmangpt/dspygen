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
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                self.df = pd.DataFrame(data)
            elif isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
                self.df = pd.DataFrame(data)
            else:
                raise ValueError("For CSV files, data must be a list of dictionaries or a dictionary of lists.")
            
            # Check for any variation of 'ID' column
            id_column = next((col for col in self.df.columns if col.lower() == 'id'), None)
            
            # If no ID column exists, add it
            if id_column is None:
                self.df.insert(0, 'ID', range(len(self.df)))
            else:
                # If ID column exists but is not the first column, move it to the front
                if self.df.columns.get_loc(id_column) != 0:
                    cols = self.df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index(id_column)))
                    self.df = self.df[cols]
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
            print("write " + self.file_path)
            try:
                # Set index=False to prevent writing the index as a separate column
                self.df.to_csv(self.file_path, index=False, **self.write_options)
            except Exception as e:
                raise ValueError(f"Failed to write to {self.file_path} due to: {e}")

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
    # Test case 1: No ID column (should add 'ID' column)
    data_csv1 = [
        {'Book Title': 'The Great Gatsby', 'Author': 'F. Scott Fitzgerald', 'Price': 10.99, 'Sold Copies': 500},
        {'Book Title': '1984', 'Author': 'George Orwell', 'Price': 9.99, 'Sold Copies': 800},
        {'Book Title': 'Brave New World', 'Author': 'Aldous Huxley', 'Price': 8.99, 'Sold Copies': 650},
        {'Book Title': 'The Catcher in the Rye', 'Author': 'J.D. Salinger', 'Price': 12.99, 'Sold Copies': 450}
    ]
    writer_csv1 = DataWriter(file_path="test1_no_id.csv", data=data_csv1)
    writer_csv1.forward()

    # Test case 2: 'id' column exists (should keep existing 'id' and move to front)
    data_csv2 = [
        {'id': 'A1', 'Book Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Price': 11.99, 'Sold Copies': 750},
        {'id': 'B2', 'Book Title': 'Pride and Prejudice', 'Author': 'Jane Austen', 'Price': 7.99, 'Sold Copies': 950},
    ]
    writer_csv2 = DataWriter(file_path="test2_existing_id.csv", data=data_csv2)
    writer_csv2.forward()

    # Test case 3: 'ID' column exists but not at the front (should move to front)
    data_csv3 = [
        {'Book Title': 'The Hobbit', 'ID': 'C3', 'Author': 'J.R.R. Tolkien', 'Price': 14.99, 'Sold Copies': 1000},
        {'Book Title': 'Dune', 'ID': 'D4', 'Author': 'Frank Herbert', 'Price': 13.99, 'Sold Copies': 850},
    ]
    writer_csv3 = DataWriter(file_path="test3_id_not_front.csv", data=data_csv3)
    writer_csv3.forward()

    # Test case 4: 'Id' column exists (should keep existing 'Id' and move to front)
    data_csv4 = [
        {'Book Title': 'The Alchemist', 'Author': 'Paulo Coelho', 'Id': 'E5', 'Price': 9.99, 'Sold Copies': 1200},
        {'Book Title': 'The Da Vinci Code', 'Author': 'Dan Brown', 'Id': 'F6', 'Price': 12.99, 'Sold Copies': 1100},
    ]
    writer_csv4 = DataWriter(file_path="test4_Id_exists.csv", data=data_csv4)
    writer_csv4.forward()

    # Example Usage for Markdown (unchanged)
    data_md = "# Book List\n\n- The Great Gatsby\n- 1984\n- Brave New World\n- The Catcher in the Rye"
    writer_md = DataWriter(file_path="Tetris_Blog_Phi3Med.md", data=data_md)
    writer_md.forward()

if __name__ == "__main__":
    main()
