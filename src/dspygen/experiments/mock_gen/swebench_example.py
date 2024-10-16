import dspy

from dspygen.experiments.mock_gen.swe_bench import SWEBench
from dspygen.utils.dspy_tools import init_ol


class IssueToPatchSignature(dspy.Signature):
    """ Transforms detailed descriptions of software issues, especially those occurring in high-stakes, large-scale production environments (such as those at FAANG companies), into actionable, ready-to-deploy git patch files. This Signature class focuses on creating highly reliable and targeted solutions that can be applied with a near-certain guarantee of success, backed by a deep understanding of system architecture and software engineering best practices. Ideal for simulating the process of a FAANG System Architect resolving complex software issues under stringent operational requirements, where patches must achieve near-perfect reliability to maintain system integrity and performance. """
    # Input field: Detailed issue description including specific technologies involved,
    # error logs, system environments details, and failure impact assessment.
    issue = dspy.InputField(desc="Comprehensive, multi-faceted description of the software issue, \
including stack traces, environments specifics, configurations, and a criticality assessment, \
to ensure a highly contextual and accurate patch formulation.")

    # Output field: A git-formatted patch file, thoroughly commented and adhering to best
    # software engineering practices, ready for deployment in production systems.
    git_patch_diff = dspy.OutputField(desc="A meticulously crafted git patch file, incorporating \
extensive comments and adhering to industry-leading software engineering standards. \
Designed to ensure seamless integration and deployment, minimizing disruption and maximizing system stability.",
                                      prefix="```diff\n")


class CoT(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(IssueToPatchSignature)

    def forward(self, issue):
        return self.prog(issue=issue)


def main():
    """Main function"""
    from dspy.teleprompt import BootstrapFewShot
    # Set up the LM
    lm = init_ol(model="phi3:instruct", max_tokens=20000)
    # lm = init_ol(model="llama3", max_tokens=20000)

    # Load the SWE-bench dataset
    swe_bench = SWEBench()
    swe_bench_trainset, swe_bench_devset = swe_bench.train[:50], swe_bench.dev[:50]

    # print(swe_bench_trainset)

    # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 4-shot examples of our CoT program.
    config = dict(max_bootstrapped_demos=4, max_labeled_demos=4)

    # Define a custom metric for evaluating patches
    def swebench_metric(gold, pred, trace=None):
        # This is a placeholder metric; adjust based on actual evaluation needs
        if gold.patch == pred.git_patch_diff:
            print(f"Gold: {gold.patch} matched with Pred: {pred.git_patch_diff}")
        return gold.patch == pred.git_patch_diff

    teleprompter = BootstrapFewShot(metric=swebench_metric, **config)
    optimized_cot = teleprompter.compile(CoT(), trainset=swe_bench_trainset)
    from time import time
    optimized_cot.save(f"optimized_cot_sig_{str(time())}.json")

    from dspy.evaluate import Evaluate

    # Set up the evaluator, which can be used multiple times.
    evaluate = Evaluate(devset=swe_bench_devset, metric=swebench_metric, num_threads=12, display_progress=True,
                        display_table=0)

    # Evaluate our `optimized_cot` program.
    evaluate(optimized_cot)

    print(lm.inspect_history(n=1))


if __name__ == '__main__':
    main()
