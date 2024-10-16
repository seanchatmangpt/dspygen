# Define PredictType for each REAP step group
from dspygen.experiments.obsidian_gen.reap_models import *
from sungen.utils.dspy_tools import PredictType, predict_types

from pydantic import BaseModel, Field
from typing import TypeVar, Type, Generic, List


# Input data for the task
input_data = {
    "problem": "A king has 1000 sweet bottles of wine, and one contains a very bitter poison. "
               "The poison takes effect exactly 24 hours after consumption. The king needs to find "
               "the poisoned bottle in 24 hours for an event. He has 10 prisoners to test the wine. "
               "What is the easiest way for him to identify the poisoned bottle?"
}


def main():
    """Main function to create tasks for all REAP steps"""
    from sungen.utils.dspy_tools import init_dspy
    init_dspy()

    # Define the tasks for each REAP step group

    # Step 0: Literal Interpretation Rule
    task_literal_interpretation = PredictType(
        input_data=input_data,
        output_model=LiteralInterpretationRule
    )

    # Step 1: Strict Interpretation Rule
    task_strict_interpretation = PredictType(
        input_data=input_data,
        output_model=StrictInterpretationRule
    )

    # Step 2: Comprehensive Feature Analysis
    task_feature_analysis = PredictType(
        input_data=input_data,
        output_model=ComprehensiveFeatureAnalysis
    )

    # Step 3: Sequential and Mechanical Process Check
    task_sequential_process_check = PredictType(
        input_data=input_data,
        output_model=SequentialAndMechanicalProcessCheck
    )

    # Step 4: Key Insight Check
    task_key_insight_check = PredictType(
        input_data=input_data,
        output_model=KeyInsightCheck
    )

    # Step 5: Known and Deduced Information
    task_known_and_deduced_info = PredictType(
        input_data=input_data,
        output_model=KnownAndDeducedInformation
    )

    # Step 6: Problem Decomposition
    task_problem_decomposition = PredictType(
        input_data=input_data,
        output_model=ProblemDecomposition
    )

    # Step 7: Graph of Thought
    task_graph_of_thought = PredictType(
        input_data=input_data,
        output_model=GraphOfThought
    )

    # Step 8: Spatial and Object Analysis
    task_spatial_object_analysis = PredictType(
        input_data=input_data,
        output_model=SpatialAndObjectAnalysis
    )

    # Step 9: Bayesian Thinking
    task_bayesian_thinking = PredictType(
        input_data=input_data,
        output_model=BayesianThinking
    )

    # Step 10: Ethical Check and Decision Making Under Uncertainty
    task_ethical_check = PredictType(
        input_data=input_data,
        output_model=EthicalCheckAndDecisionMaking
    )

    # Step 11: Multiple Solution Generation
    task_multiple_solution_generation = PredictType(
        input_data=input_data,
        output_model=MultipleSolutionGeneration
    )

    # Step 12: Quickest and Easiest Solution
    task_quick_solution = PredictType(
        input_data=input_data,
        output_model=QuickestAndEasiestSolution
    )

    # Step 13: Final Output and Recommendation
    task_final_output = PredictType(
        input_data=input_data,
        output_model=FinalOutputAndRecommendation
    )

    # Group all tasks together for concurrent processing
    tasks = [
        # task_literal_interpretation,
        # task_strict_interpretation,
        # task_feature_analysis,
        # task_sequential_process_check,
        # task_key_insight_check,
        # task_known_and_deduced_info,
        # task_problem_decomposition,
        # task_graph_of_thought,
        # task_spatial_object_analysis,
        # task_bayesian_thinking,
        # task_ethical_check,
        # task_multiple_solution_generation,
        # task_quick_solution,
        task_final_output
    ]

    # Execute all the tasks concurrently using predict_types
    results = predict_types(tasks)

    # Process and print the results
    for result in results:
        print(result.render())


if __name__ == '__main__':
    main()

