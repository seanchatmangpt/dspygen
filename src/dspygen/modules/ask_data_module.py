import dspy
from dspygen.utils.dspy_tools import init_dspy, init_ol
from dspygen.rm.data_retriever import read_any
from dspygen.rm.doc_retriever import read_any as doc_read_any
import pandas as pd
import io

class AskDataSignature(dspy.Signature):
    """
    Answers a natural language question about data from a file.
    """
    question = dspy.InputField(desc="Natural language question about the data.")
    data = dspy.InputField(desc="The data content from the file.")
    answer = dspy.OutputField(desc="Plain text answer to the question.")

class AskDataModule(dspy.Module):
    """AskDataModule for answering questions about data from various file types"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args

    def forward(self, question, file_path):
        try:
            # First, try to read as structured data
            data = read_any(file_path, query="")
            if isinstance(data, pd.DataFrame):
                csv_buffer = io.StringIO()
                data.to_csv(csv_buffer, index=False)
                data = csv_buffer.getvalue()
            else:
                data = str(data)
        except Exception:
            try:
                # If that fails, try to read as a document
                data = doc_read_any(file_path)
                if isinstance(data, dict):
                    data = "\n".join(data.values())
                data = str(data)
            except Exception:
                # If both fail, read as plain text
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = file.read()

        pred = dspy.Predict(AskDataSignature)
        return pred(question=question, data=data).answer

def ask_data_call(question, file_path):
    ask_data_module = AskDataModule()
    return ask_data_module.forward(question=question, file_path=file_path)

def main():
    # init_ol(model="mistral-nemo")
    init_ol(model="qwen2:latest")
    # init_ol(model="mistral-nemo")
    # Example usage
    from dspygen.experiments.cal_apps.reminder_app import RemindersApp
    app = RemindersApp()
    app.export_reminders("reminders.csv")
    question = "Can you answer me a new appointment for a haircut at 1pm on 9/1"
    
    result = ask_data_call(question=question, file_path="reminders.csv")
    print(result)

if __name__ == "__main__":
    main()
