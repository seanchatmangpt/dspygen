import dspy
from dspy.teleprompt import MIPRO

from dspygen.experiments.mock_gen.swe_bench import SWEBench
from dspygen.utils.dspy_tools import init_ol


class CoT(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("issue -> patch")

    def forward(self, issue):
        return self.prog(issue=issue)


def main():
    """Main function"""
    from dspy.teleprompt import BootstrapFewShot
    # Set up the LM
    lm = init_ol()

    # Load the SWE-bench dataset
    swe_bench = SWEBench()
    swe_bench_trainset, swe_bench_devset = swe_bench.train[:25], swe_bench.dev[:25]

    print(swe_bench_trainset)

    # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 4-shot examples of our CoT program.
    config = dict(max_bootstrapped_demos=4, max_labeled_demos=4)

    # Define a custom metric for evaluating patches
    def swebench_metric(gold, pred, trace=None):
        # This is a placeholder metric; adjust based on actual evaluation needs
        return gold.patch == pred.patch

    teleprompter = MIPRO(metric=swebench_metric, **config)
    optimized_cot = teleprompter.compile(CoT(), trainset=swe_bench_trainset)
    optimized_cot.save("optimized_cot.json")

    from dspy.evaluate import Evaluate

    # Set up the evaluator, which can be used multiple times.
    evaluate = Evaluate(devset=swe_bench_devset, metric=swebench_metric, num_threads=8, display_progress=True,
                        display_table=0)

    # Evaluate our `optimized_cot` program.
    evaluate(optimized_cot)


    lm.inspect_history(n=1)


if __name__ == '__main__':
    main()
