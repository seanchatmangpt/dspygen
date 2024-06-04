"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class NaturalLanguageToSQLModule(dspy.Module):
    """NaturalLanguageToSQLModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, natural_language, database_schema):
        pred = dspy.Predict("natural_language, database_schema -> sql_query")
        self.output = pred(natural_language=natural_language, database_schema=database_schema).sql_query
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(natural_language, database_schema):
    """NaturalLanguageToSQLModule"""
    init_dspy()

    print(natural_language_to_sql_call(natural_language=natural_language, database_schema=database_schema))



def natural_language_to_sql_call(natural_language, database_schema):
    natural_language_to_sql = NaturalLanguageToSQLModule()
    return natural_language_to_sql.forward(natural_language=natural_language, database_schema=database_schema)

schema = """
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name TEXT,
    department TEXT
    organization TEXT
    permission_level INT
);
"""

nl = """
Show me the names of all the employees who work in the IT department and have permission level 3.
The must be in the organization 'ABC'.
"""


def main():
    init_dspy()
    natural_language = nl
    database_schema = schema
    result = natural_language_to_sql_call(natural_language=natural_language, database_schema=database_schema)
    print(result)


from fastapi import APIRouter
router = APIRouter()

@router.post("/natural_language_to_sql/")
async def natural_language_to_sql_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return natural_language_to_sql_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("NaturalLanguageToSQLModule Generator")
natural_language = st.text_input("Enter natural_language")
database_schema = st.text_input("Enter database_schema")

if st.button("Submit NaturalLanguageToSQLModule"):
    init_dspy()

    result = natural_language_to_sql_call(natural_language=natural_language, database_schema=database_schema)
    st.write(result)
"""

if __name__ == "__main__":
    main()
