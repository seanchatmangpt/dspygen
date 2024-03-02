"""assert"""
import typer

from dspygen.typetemp.functional import render

app = typer.Typer(help="Generate assertions for dspy.")


assert_template = '''import dspy
from dspygen.utils.dspy_tools import init_dspy

MIN_SUMMARY_LENGTH = 20


class TempModule(dspy.Module):
    def __init__(self, min_summary_len=MIN_SUMMARY_LENGTH):
        super().__init__()
        
        self.min_summary_len = min_summary_len
        
    def validate_output(self, summary) -> bool:
        """Summary should be over a certain amount of characters"""
        
        dspy.Assert(len(summary) > self.min_summary_len, f"{summary} is not valid")
        
        return True
        
    def forward(self, prompt):
        pred = dspy.Predict("prompt -> summary")
        summary = pred(prompt=prompt).summary
        
        try:
            if self.validate_output(summary):
                return summary
        except AssertionError as e:
            pred = dspy.ChainOfThought("prompt, error -> summary")
            summary = pred(prompt=prompt, error=str(e)).summary
            
            if self.validate_output(summary):
                return summary


def main():
    init_dspy()    
    
    story = "The quick brown fox jumps over the lazy dog."
    
    temp_module = TempModule(min_summary_len=100)
    summary = temp_module.forward(story)
    
    print(summary)
    

if __name__ == "__main__":
    main()
    
'''

@app.command(name="new")
def new_assert(file_name: str):
    """assert"""
    _assert = render(assert_template)
    print(_assert)

    with open(file_name, "w") as f:
        f.write(_assert)

    print(f"Assert written to {file_name}")



def main():
    _assert = render(assert_template)
    print(_assert)

    with open("temp_assert.py", "w") as f:
        f.write(_assert)

    print("assert written to temp_assert.py")


if __name__ == '__main__':
    main()
