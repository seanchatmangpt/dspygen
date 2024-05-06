"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        

class GenerateSearchQueriesForLearningObjective(dspy.Signature):
    """
    Generate 1 to 3 search queries based on the specified learning objective with the intent
    of finding relevant information via SERP API.
    """
    learning_objectives = dspy.InputField(desc="Specific learning objective to generate search queries for.")

    search_queries = dspy.OutputField(desc="List of 1 to 3 search queries tailored to retrieve information relevant to the learning objective. Separate each query with a comma.", prefix="```search_queries")




class QueryGeneratorModule(dspy.Module):
    """QueryGeneratorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, learning_objectives):
        pred = dspy.Predict(GenerateSearchQueriesForLearningObjective)
        self.output = pred(learning_objectives=learning_objectives).search_queries
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(learning_objectives):
    """QueryGeneratorModule"""
    init_dspy()

    print(query_generator_call(learning_objectives=learning_objectives))



def query_generator_call(learning_objectives):
    query_generator = QueryGeneratorModule()
    return query_generator.forward(learning_objectives=learning_objectives)



def main():
    init_dspy()
    learning_objectives = ""
    result = query_generator_call(learning_objectives=learning_objectives)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/query_generator/")
async def query_generator_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return query_generator_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("QueryGeneratorModule Generator")
learning_objectives = st.text_input("Enter learning_objectives")

if st.button("Submit QueryGeneratorModule"):
    init_dspy()

    result = query_generator_call(learning_objectives=learning_objectives)
    st.write(result)
"""

if __name__ == "__main__":
    main()
