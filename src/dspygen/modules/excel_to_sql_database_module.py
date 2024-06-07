"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ExcelToSQLDatabaseModule(dspy.Module):
    """ExcelToSQLDatabaseModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, excel_data):
        pred = dspy.Predict("excel_data -> sql_entries")
        self.output = pred(excel_data=excel_data).sql_entries
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(excel_data):
    """ExcelToSQLDatabaseModule"""
    init_dspy()

    print(excel_to_sql_database_call(excel_data=excel_data))



def excel_to_sql_database_call(excel_data):
    excel_to_sql_database = ExcelToSQLDatabaseModule()
    return excel_to_sql_database.forward(excel_data=excel_data)



def main():
    init_dspy(model="gpt-4o")
    excel_data = "Create this table: name,age\nJohn,25\nDoe,30\n"
    result = excel_to_sql_database_call(excel_data=excel_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/excel_to_sql_database/")
async def excel_to_sql_database_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return excel_to_sql_database_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("ExcelToSQLDatabaseModule Generator")
excel_data = st.text_input("Enter excel_data")

if st.button("Submit ExcelToSQLDatabaseModule"):
    init_dspy()

    result = excel_to_sql_database_call(excel_data=excel_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
