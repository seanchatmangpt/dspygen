import sqlite3

from dspygen.modules.gen_keyword_arguments_module import invoke
from dspygen.utils.dspy_tools import init_dspy

# Assuming Chinook.db is located in the same directory for simplicity
conn = sqlite3.connect("Chinook.db")


def execute_query(query: str) -> str:
    """
    Executes a SQL query against the database and returns the results as a string.

    Parameters:
    - query (str): SQL query to be executed.

    Returns:
    str: The results of the SQL query formatted as a string.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if not results:
            return "No results found."
        else:
            result_str = "\n".join([str(row) for row in results])
            return result_str
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        cursor.close()


def question_to_chinook_query(question: str, query: str) -> str:
    """Convert the question to a Chinook.db SQL Query"""
    return execute_query(query)


def main():
    init_dspy()

    result = invoke(question_to_chinook_query, "Hi, who are the top 5 artists by number of tracks?")

    print(result)


if __name__ == '__main__':
    main()
