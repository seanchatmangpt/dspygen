import dspy
from dspygen.utils.dspy_tools import init_dspy

class TextToDFSQLSignature(dspy.Signature):
    """
    Converts natural language text and a DataFrame schema into an SQL query
    compatible with pandasql.sqldf, where the DataFrame is referenced as 'df'.

    ```python
    import pandas as pd
    from pandasql import sqldf

    # Example DataFrame
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })

    # Generated SQL query from the signature
    query = "SELECT * FROM df WHERE age > 30"

    # Execute query with sqldf
    result = sqldf(query, locals())
    ```
    """
    text = dspy.InputField(desc="Natural language text describing the query.")
    df_schema = dspy.InputField(desc="Schema of the DataFrame, containing columns and their data types.")
    df_data = dspy.InputField(desc="Data of the DataFrame, containing rows and columns.")
    sql_query = dspy.OutputField(
        desc=(
            "Generated SQL query based on the input text, designed to be compatible with "
            "pandasql.sqldf. The query will reference the DataFrame as 'df' and use SQLite-compatible "
            "SQL syntax. Ensure the SQL operations and functions used are supported by SQLite"
            "ALWAYS SELECT *."
        ),
        prefix="```sql\nSELECT * FROM df "
    )

class DFSQLModule(dspy.Module):
    """DFSQLModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, text, df_schema, df_data):
        # Use the custom Signature class for prediction
        pred = dspy.Predict(TextToDFSQLSignature)
        self.output = "SELECT * FROM df " + pred(text=text, df_schema=df_schema, df_data=df_data).sql_query
        self.output = self.output.replace("```", "").strip()
        return self.output


def dfsql_call(text, df_schema, df_data):
    text_to_data_frame_sql_generator = DFSQLModule()
    return text_to_data_frame_sql_generator.forward(text=text, df_schema=df_schema, df_data=df_data)


def main():
    init_dspy()
    # app = RemindersApp()
    # app.export_reminders("reminders.csv")
    # dr = DataRetriever(file_path="reminders.csv")
    # df_schema = dr.df.columns.tolist()
    # df_data = dr.df.values.tolist()
    #
    # text = "Find what am I supposed to cut?"
    # result = dfsql_call(text=text, df_schema=df_schema, df_data=df_data)
    #
    # results = app.query(result)
    #
    # print(results[0])


if __name__ == "__main__":
    main()
