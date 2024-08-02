import dspy

from dspygen.utils.dspy_tools import init_ol

#init_ol() - breaks auto poe tests  >> TBD move into main


class NLtoSQL(dspy.Signature):
    """
    Convert natural language to SQL
    """
    natural_language = dspy.InputField(desc="Natural language query")
    database_schema = dspy.InputField(desc="The schema of the target database in JSON format.")
    sql_query = dspy.OutputField(desc="SQL query")


schema = """
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name TEXT,
    department TEXT
    organization TEXT
    permission_level INT
);
"""


natural_language = """
Show me the names of all the employees who work in the IT department and have permission level 3.
The must be in the organization 'ABC'.
"""


prog = dspy.ChainOfThought(NLtoSQL)

pred = prog.forward(natural_language=natural_language, database_schema=schema)
print(pred)
