import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import MIPRO
from dspygen.experiments.mock_gen.swe_bench import SWEBench
from dspygen.utils.dspy_tools import init_ol

# Initialize DSPy settings with a retrieval model and a language model
colbert_v2_endpoint = "http://20.102.90.50:2017/wiki17_abstracts"
colbertv2 = dspy.ColBERTv2(url=colbert_v2_endpoint)
lm = init_ol()
dspy.settings.configure(rm=colbertv2, lm=lm)

class IssueToPatchSignature(dspy.Signature):
    """ Transforms detailed descriptions of software issues, especially those occurring in high-stakes, large-scale production environments (such as those at FAANG companies), into actionable, ready-to-deploy git patch files. This Signature class focuses on creating highly reliable and targeted solutions that can be applied with a near-certain guarantee of success, backed by a deep understanding of system architecture and software engineering best practices. Ideal for simulating the process of a FAANG System Architect resolving complex software issues under stringent operational requirements, where patches must achieve near-perfect reliability to maintain system integrity and performance. """
    # Input field: Detailed issue description including specific technologies involved,
    # error logs, system environment details, and failure impact assessment.
    issue = dspy.InputField(desc="Comprehensive, multi-faceted description of the software issue, \
including stack traces, environment specifics, configurations, and a criticality assessment, \
to ensure a highly contextual and accurate patch formulation.")

    # Output field: A git-formatted patch file, thoroughly commented and adhering to best
    # software engineering practices, ready for deployment in production systems.
    git_patch_diff = dspy.OutputField(desc="A meticulously crafted git patch file, incorporating \
extensive comments and adhering to industry-leading software engineering standards. \
Designed to ensure seamless integration and deployment, minimizing disruption and maximizing system stability.",
                                      prefix="```diff\n")

class GeneratePatch(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_patch = dspy.ChainOfThought(IssueToPatchSignature)

    def forward(self, issue):
        return self.generate_patch(issue=issue)

def main():
    """Main function"""
    # Load SWEBench dataset
    swe_bench = SWEBench()
    trainset = swe_bench.train[:50]  # Example subset for training
    devset = swe_bench.dev[:50]  # Example subset for development

    # Initialize the program
    program = GeneratePatch()

    # Define a metric for evaluating the effectiveness of the patches
    def patch_effectiveness_metric(gold, pred, trace=None):
        return gold.patch == pred.git_patch_diff  # This is a simplification; you might need a more complex comparison

    # Initialize MIPRO for optimizing the generation of patches
    teleprompter = MIPRO(prompt_model=lm, task_model=lm, metric=patch_effectiveness_metric, num_candidates=10,
                         init_temperature=1.0, verbose=True, )
    compiled_program = teleprompter.compile(program, trainset=trainset, num_trials=30,
                                            max_bootstrapped_demos=1, max_labeled_demos=2,
                                            eval_kwargs={'num_threads': 10, 'display_progress': True},
                                            requires_permission_to_run=False)

    from time import time
    compiled_program.save(f"optimized_swe_mipro_program_{str(time())}.json")

    # Evaluate the optimized program
    evaluate = Evaluate(devset=devset, metric=patch_effectiveness_metric, num_threads=10, display_progress=True)
    results = evaluate(compiled_program)
    print(f"Evaluation Results: {results}")

if __name__ == '__main__':
    main()
