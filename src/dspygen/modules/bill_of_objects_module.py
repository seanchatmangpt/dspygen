import dspy
from dspygen.utils.dspy_tools import init_dspy        


class BillOfObjectsModule(dspy.Module):
    """BillOfObjectsModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, source_text):
        pred = dspy.Predict("source_text -> bill_of_objects_csv")
        self.output = pred(source_text=source_text).bill_of_objects_csv
        return self.output
        

def bill_of_objects_call(source_text):
    bill_of_objects = BillOfObjectsModule()
    return bill_of_objects.forward(source_text=source_text)


def main():
    init_dspy()
    source_text = ""
    print(bill_of_objects_call(source_text=source_text))


if __name__ == "__main__":
    main()
