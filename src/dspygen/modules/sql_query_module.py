"""

"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class SQLQueryModule(dspy.Module):
    """SQLQueryModule"""

    def forward(self, old_query):
        pred = dspy.Predict("old_query -> improved_query")
        result = pred(old_query=old_query).improved_query
        return result


def sql_query_call(old_query):
    sql_query = SQLQueryModule()
    return sql_query.forward(old_query=old_query)


@app.command()
def call(old_query):
    """SQLQueryModule"""
    init_dspy()
    
    print(sql_query_call(old_query=old_query))


from fastapi import APIRouter
router = APIRouter()

@router.post("/sql_query/")
async def sql_query_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return sql_query_call(**data)


def main():
    init_dspy()
    old_query = ""
    print(sql_query_call(old_query=old_query))
    

if __name__ == "__main__":
    main()
