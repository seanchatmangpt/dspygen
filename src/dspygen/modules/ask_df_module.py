import dspy
from dspygen.utils.dspy_tools import init_dspy
import pandas as pd
import io

class AskDFSignature(dspy.Signature):
    """
    Answers a natural language question about a DataFrame.
    """
    question = dspy.InputField(desc="Natural language question about the DataFrame.")
    df_csv = dspy.InputField(desc="The DataFrame in CSV string format.")
    answer = dspy.OutputField(desc="Plain text answer to the question.")

class AskDFModule(dspy.Module):
    """AskDFModule for answering questions about DataFrames using natural language"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args

    def forward(self, question, df):
        # Convert DataFrame to CSV string
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        df_csv = csv_buffer.getvalue()

        pred = dspy.Predict(AskDFSignature)
        return pred(question=question, df_csv=df_csv).answer

def ask_df_call(question, df):
    ask_df_module = AskDFModule()
    return ask_df_module.forward(question=question, df=df)

def main():
    init_dspy()
    # Example usage
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'San Francisco', 'London']
    })
    question = "Who is older than 30?"
    
    result = ask_df_call(question=question, df=df)
    print(result)

if __name__ == "__main__":
    main()