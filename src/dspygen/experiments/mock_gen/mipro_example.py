import re

import dspy
from dspy.evaluate import Evaluate
from dspy.datasets import HotPotQA
from dsp.utils import EM
from dspy.teleprompt import BayesianSignatureOptimizer, MIPRO

from dspygen.utils.dspy_tools import init_ol


colbert_v2_endpoint = "http://20.102.90.50:2017/wiki17_abstracts"
colbertv2 = dspy.ColBERTv2(url=colbert_v2_endpoint)


lm = init_ol()

dspy.settings.configure(rm=colbertv2, lm=lm)


class ReturnRankedDocuments(dspy.Signature):
    """Given a question we are trying to answer and a list of passages, return a comma separated list of the numbers associated with each passage. These numbers should be ordered by helpfulness in answering the question, with most helpful passage number first, and the least helpful last."""
    question = dspy.InputField(desc="The question we're trying to answer.")
    context = dspy.InputField(desc="List of potentially related passages.")
    ranking = dspy.OutputField(
        desc="A comma separated list of numbers corresponding to passage indices, ranked in descending order by their helpfulness in answering our question.")


class RankingMultiHop(dspy.Module):
    def __init__(self, hops, num_passages_to_retrieve, max_passages_in_context):
        super().__init__()
        self.hops = hops
        self.num_passages_to_retrieve = num_passages_to_retrieve
        self.max_passages_in_context = max_passages_in_context
        self.retrieve = dspy.Retrieve(k=self.num_passages_to_retrieve)
        self.generate_query = dspy.ChainOfThought("context ,question->search_query")
        self.generate_answer = dspy.ChainOfThought("context ,question->answer")
        self.generate_ranking = dspy.ChainOfThought(ReturnRankedDocuments)

    def forward(self, question):
        context = []
        full_context = []
        top_context = []
        max_passage_num = self.max_passages_in_context
        for hop in range(self.hops):
            # Get a new query
            query = self.generate_query(context=context, question=question).search_query
            # Get new passages
            context = self.retrieve(query).passages
            # Add these new passages to the previous top context
            full_context = top_context + context
            # Get the most important indices, ranked
            most_important_indices = self.generate_ranking(question=question, context=full_context).ranking
            indices = [int(num) for num in re.findall(r'\d+', most_important_indices)]

            if len(indices) < max_passage_num:
                indices = range(1, max_passage_num + 1)

            valid_indices = [index - 1 for index in indices if index - 1 < len(context)]
            top_indices = sorted(valid_indices, key=lambda x: x)[:max_passage_num + 1]
            most_important_context_list = [context[idx] for idx in top_indices]
            # Save the top context
            top_context = most_important_context_list

        return dspy.Prediction(context=context,
                               answer=self.generate_answer(context=top_context, question=question).answer)


def main():
    """Main function"""
    program = RankingMultiHop(hops=4, num_passages_to_retrieve=5, max_passages_in_context=5)

    # Load and configure the datasets.
    TRAIN_SIZE = 5
    EVAL_SIZE = 5

    hotpot_dataset = HotPotQA(train_seed=1, eval_seed=2023, test_size=0)
    trainset = [x.with_inputs('question') for x in hotpot_dataset.train][:TRAIN_SIZE]
    devset = [x.with_inputs('question') for x in hotpot_dataset.dev][:EVAL_SIZE]

    # Set up metrics
    NUM_THREADS = 10

    metric = dspy.evaluate.answer_exact_match

    kwargs = dict(num_threads=NUM_THREADS, display_progress=True)
    evaluate = Evaluate(devset=devset, metric=metric, **kwargs)

    # baseline_train_score = evaluate(program, devset=trainset)
    # baseline_eval_score = evaluate(program, devset=devset)

    # Define hyperparameters:
    N = 10  # The number of instructions and fewshot examples that we will generate and optimize over
    trials = 30  # The number of optimization trials to be run (we will test out a new combination of instructions and fewshot examples in each trial)
    temperature = 1.0  # The temperature configured for generating new instructions

    # Compile
    eval_kwargs = dict(num_threads=16, display_progress=True, display_table=0)
    teleprompter = MIPRO(prompt_model=lm, task_model=lm, metric=metric, num_candidates=N,
                         init_temperature=temperature, verbose=True)
    compiled_program = teleprompter.compile(program, trainset=trainset, num_trials=trials, max_bootstrapped_demos=1,
                                            max_labeled_demos=2, eval_kwargs=eval_kwargs)

    best_score = 0

    def get_signature(predictor):
        if (hasattr(predictor, 'extended_signature')):
            return predictor.extended_signature
        elif (hasattr(predictor, 'signature')):
            return predictor.signature

    print(f"Basline program | Score: {best_score}:")
    for i, predictor in enumerate(program.predictors()):
        print(f"Prompt {i + 1} Instruction: {get_signature(predictor).instructions}")
    print()

    print("----------------")

    for trial_num in compiled_program.trial_logs:
        program_score = compiled_program.trial_logs[trial_num]["score"]
        program_pruned = compiled_program.trial_logs[trial_num]["pruned"]
        if program_score > best_score and not program_pruned:
            best_score = program_score
            best_program_so_far = compiled_program.trial_logs[trial_num]["program"]
        if trial_num % 5 == 0:
            print(f"Best program after {trial_num} trials | Score: {best_score}:")
            for i, predictor in enumerate(best_program_so_far.predictors()):
                print(f"Prompt {i + 1} Instruction: {get_signature(predictor).instructions}")
            print()


if __name__ == '__main__':
    main()
