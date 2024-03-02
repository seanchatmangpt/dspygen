import dspy
from dspygen.utils.dspy_tools import init_dspy

MIN_SUMMARY_LENGTH = 20


class TempModule(dspy.Module):
    def __init__(self, min_summary_len=MIN_SUMMARY_LENGTH):
        super().__init__()
        
        self.min_summary_len = min_summary_len
        
    def validate_output(self, summary) -> bool:
        """Summary should be over a certain amount of characters"""
        
        dspy.Assert(len(summary) > self.min_summary_len,
                    f"len({summary}) > min_summary_len={self.min_summary_len} is the incorrect length")
        
        return True
        
    def forward(self, prompt):
        pred = dspy.Predict("prompt, min_summary_len -> summary")
        summary = pred(prompt=prompt, min_summary_len=str(self.min_summary_len)).summary
        
        try:
            if self.validate_output(summary):
                return summary
        except AssertionError as e:
            pred = dspy.ChainOfThought("prompt, error -> summary")
            summary = pred(prompt=prompt, error=str(e)).summary
            
            if self.validate_output(summary):
                return summary


story = """Chaining language model (LM) calls as com- posable modules is fueling a new powerful way of programming. 
However, ensuring that LMs adhere to important constraints remains a key challenge, one often addressed with 
heuristic “prompt engineering”. We introduce LM Asser- tions, a new programming construct for express- ing 
computational constraints that LMs should satisfy. We integrate our constructs into the re- cent DSPy programming 
model for LMs, and present new strategies that allow DSPy to com- pile programs with arbitrary LM Assertions into 
systems that are more reliable and more accu- rate. In DSPy, LM Assertions can be integrated at compile time, 
via automatic prompt optimiza- tion, and/or at inference time, via automatic self- refinement and backtracking. We 
report on two early case studies for complex question answer- ing (QA), in which the LM program must iter- atively 
retrieve information in multiple hops and synthesize a long-form answer with citations. We find that LM Assertions 
improve not only compli- ance with imposed rules and guidelines but also enhance downstream task performance, 
deliver- ing intrinsic and extrinsic gains up to 35.7% and 13.3%, respectively. Our reference implementa- tion of LM 
Assertions is integrated into DSPy at dspy.ai."""


def main():
    init_dspy()    
    
    temp_module = TempModule(min_summary_len=int(len(story)/4))
    summary = temp_module.forward(story)
    
    print(summary)
    

if __name__ == "__main__":
    main()
    