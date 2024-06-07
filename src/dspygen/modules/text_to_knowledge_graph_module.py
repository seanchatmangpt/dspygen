"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class TextToKnowledgeGraphModule(dspy.Module):
    """TextToKnowledgeGraphModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, unstructured_text):
        pred = dspy.Predict("unstructured_text -> knowledge_graph")
        self.output = pred(unstructured_text=unstructured_text).knowledge_graph
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(unstructured_text):
    """TextToKnowledgeGraphModule"""
    init_dspy()

    print(text_to_knowledge_graph_call(unstructured_text=unstructured_text))



def text_to_knowledge_graph_call(unstructured_text):
    text_to_knowledge_graph = TextToKnowledgeGraphModule()
    return text_to_knowledge_graph.forward(unstructured_text=unstructured_text)



def main():
    init_dspy()
    unstructured_text = ""
    result = text_to_knowledge_graph_call(unstructured_text=unstructured_text)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/text_to_knowledge_graph/")
async def text_to_knowledge_graph_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return text_to_knowledge_graph_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("TextToKnowledgeGraphModule Generator")
unstructured_text = st.text_input("Enter unstructured_text")

if st.button("Submit TextToKnowledgeGraphModule"):
    init_dspy()

    result = text_to_knowledge_graph_call(unstructured_text=unstructured_text)
    st.write(result)
"""

if __name__ == "__main__":
    main()
