from pydantic import Field
from typing import List, Optional

from dspygen.utils.dsl_tools import DSLModel
from sungen.typetemp.template.render_mixin import RenderMixin
from sungen.typetemp.template.typed_template import TypedTemplate


# Extend each Pydantic model with TypedTemplate for rendering
# class LiteralInterpretationRule(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 0: Literal Interpretation Rule.
#     """
#     problem_statements: List[str] = Field(
#         ...,
#         description="Interpret every statement in the problem LITERALLY. Do not assume any implications or consequences beyond what is explicitly stated."
#     )
#     straightforward_interpretation: bool = Field(
#         default=True,
#         description="Identify the most straightforward interpretation of commonly understood concepts."
#     )
#
#     source: str = """
#     Problem Statements:
#     {% for statement in problem_statements %}
#     - {{ statement }}
#     {% endfor %}
#
#     Straightforward Interpretation: {{ straightforward_interpretation }}
#     """
#
#
# class StrictInterpretationRule(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 1: Strict Interpretation Rule.
#     """
#     stick_to_explicit_info: bool = Field(
#         default=True,
#         description="Stick ONLY to what is explicitly stated in the problem."
#     )
#     no_assumptions_or_inferences: bool = Field(
#         default=True,
#         description="Do not make any assumptions or inferences beyond the exact wording."
#     )
#     explicit_state: Optional[str] = Field(
#         None,
#         description="If the problem doesn’t provide enough information to draw a conclusion, explicitly state this."
#     )
#
#     source: str = """
#     Stick to explicit info: {{ stick_to_explicit_info }}
#     No Assumptions or Inferences: {{ no_assumptions_or_inferences }}
#     Explicit State: {{ explicit_state }}
#     """
#
#
# class ComprehensiveFeatureAnalysis(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 2: Comprehensive Feature Analysis.
#     """
#     steps: List[str] = Field(
#         ...,
#         description="A list of steps to analyze every feature in the problem."
#     )
#     include: List[str] = Field(
#         ...,
#         description="A list of specific elements to include, such as objects, actors, actions, spatial relations, etc."
#     )
#     potential_implication: str = Field(
#         default="Potential implication: Note but do not treat as fact.",
#         description="A guideline to handle implications."
#     )
#     note_significance: Optional[str] = Field(
#         None,
#         description="Optional notes on the significance of each feature, but only based on explicit statements."
#     )
#
#     source: str = """
#     Steps:
#     {% for step in steps %}
#     - {{ step }}
#     {% endfor %}
#
#     Include:
#     {% for item in include %}
#     - {{ item }}
#     {% endfor %}
#
#     Potential Implication: {{ potential_implication }}
#     Note Significance: {{ note_significance }}
#     """
#
#
# class SequentialAndMechanicalProcessCheck(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 3: Sequential and Mechanical Process Check.
#     """
#     action: List[str] = Field(
#         ...,
#         description="A list of actions to analyze sequential, cyclical, or mechanical processes."
#     )
#     key_questions: List[str] = Field(
#         ...,
#         description="Key questions to assess the impact of sequences or mechanical steps on the overall problem."
#     )
#
#     source: str = """
#     Actions:
#     {% for act in action %}
#     - {{ act }}
#     {% endfor %}
#
#     Key Questions:
#     {% for question in key_questions %}
#     - {{ question }}
#     {% endfor %}
#     """
#
#
# class KeyInsightCheck(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 4: Key Insight Check.
#     """
#     action: List[str] = Field(
#         ...,
#         description="Steps to identify key insights or details that could immediately simplify or reveal the solution."
#     )
#     possible_insights: List[str] = Field(
#         ...,
#         description="A list of possible insights that could lead to a quick solution or eliminate many options."
#     )
#     result: Optional[str] = Field(
#         None,
#         description="If a solution is found, state the result. Otherwise, proceed with further analysis."
#     )
#
#     source: str = """
#     Actions:
#     {% for act in action %}
#     - {{ act }}
#     {% endfor %}
#
#     Possible Insights:
#     {% for insight in possible_insights %}
#     - {{ insight }}
#     {% endfor %}
#
#     Result: {{ result }}
#     """
#
#
# class KnownAndDeducedInformation(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 5: Known and Deduced Information.
#     """
#     explicit_facts: List[str] = Field(
#         ...,
#         description="List of exact quotes or facts stated explicitly in the problem."
#     )
#     deductions: List[str] = Field(
#         ...,
#         description="Valid deductions that are 100% certain based on the explicit wording of the problem."
#     )
#     deduction_format: str = Field(
#         "Deduction: [Inference] - Logical Basis: [Reason] - Based on: [Quote(s)]",
#         description="Format for representing deductions."
#     )
#     key_questions: List[str] = Field(
#         ...,
#         description="Key questions to ensure that the deductions address the core problem."
#     )
#
#     source: str = """
#     Explicit Facts:
#     {% for fact in explicit_facts %}
#     - {{ fact }}
#     {% endfor %}
#
#     Deductions:
#     {% for deduction in deductions %}
#     - {{ deduction }}
#     {% endfor %}
#
#     Deduction Format: {{ deduction_format }}
#
#     Key Questions:
#     {% for question in key_questions %}
#     - {{ question }}
#     {% endfor %}
#     """
#
#
# class ProblemDecomposition(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 6: Problem Decomposition.
#     """
#     components: List[str] = Field(
#         ...,
#         description="Key components of the problem, broken into manageable parts."
#     )
#     supporting_quotes: List[str] = Field(
#         ...,
#         description="Exact quotes from the problem statement supporting each component."
#     )
#     deductions: Optional[List[str]] = Field(
#         None,
#         description="Any deductions that led to the decomposition, with clear explanations."
#     )
#
#     source: str = """
#     Components:
#     {% for component in components %}
#     - {{ component }}
#     {% endfor %}
#
#     Supporting Quotes:
#     {% for quote in supporting_quotes %}
#     - {{ quote }}
#     {% endfor %}
#
#     Deductions:
#     {% if deductions %}
#     {% for deduction in deductions %}
#     - {{ deduction }}
#     {% endfor %}
#     {% endif %}
#     """
#
#
# class GraphOfThought(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 7: Graph of Thought.
#     """
#     key_concepts: List[str] = Field(
#         ...,
#         description="Main concepts or subproblems identified explicitly in the problem."
#     )
#     relationships: List[str] = Field(
#         ...,
#         description="Connections between key concepts based on explicit information."
#     )
#     output_format: str = Field(
#         "If visual: Draw a graph; If textual: Create a list of nodes and connections",
#         description="Format for visual or textual graph representation."
#     )
#
#     source: str = """
#     Key Concepts:
#     {% for concept in key_concepts %}
#     - {{ concept }}
#     {% endfor %}
#
#     Relationships:
#     {% for relationship in relationships %}
#     - {{ relationship }}
#     {% endfor %}
#
#     Output Format: {{ output_format }}
#     """
#
#
# class SpatialAndObjectAnalysis(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 8: Spatial and Object Analysis.
#     """
#     objects: List[str] = Field(
#         ...,
#         description="List of physical objects explicitly mentioned in the problem."
#     )
#     spatial_relationships: List[str] = Field(
#         ...,
#         description="Spatial relationships between objects, based on explicit statements."
#     )
#     movement_dynamics: Optional[str] = Field(
#         None,
#         description="If applicable, movement or interactions of objects over time."
#     )
#     constraints: Optional[List[str]] = Field(
#         None,
#         description="Any physical limitations or boundaries explicitly mentioned."
#     )
#
#     source: str = """
#     Objects:
#     {% for obj in objects %}
#     - {{ obj }}
#     {% endfor %}
#
#     Spatial Relationships:
#     {% for relation in spatial_relationships %}
#     - {{ relation }}
#     {% endfor %}
#
#     Movement Dynamics: {{ movement_dynamics }}
#     Constraints:
#     {% if constraints %}
#     {% for constraint in constraints %}
#     - {{ constraint }}
#     {% endfor %}
#     {% endif %}
#     """
#
#
class BayesianThinking(DSLModel, TypedTemplate):
    """
    Pydantic model for REAP Step 9: Bayesian Thinking.
    """
    potential_implications: str = Field(
        "Potential implication: Note but do not use it to update beliefs.",
        description="How to treat implied information."
    )

    # source: str = """
    # Update Beliefs: {{ update_beliefs }}
    # Potential Implications: {{ potential_implications }}
#     """
#
#
# class EthicalCheckAndDecisionMaking(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 10: Ethical Check and Decision-Making Under Uncertainty.
#     """
#     assess_information: str = Field(
#         "Review explicit information to assess known risks.",
#         description="Step to assess information for decision-making."
#     )
#     risk_aversion: str = Field(
#         "Prioritize actions that minimize or avoid risks in uncertain situations.",
#         description="Rule for making decisions when outcomes involve significant risks."
#     )
#
#     source: str = """
#     Assess Information: {{ assess_information }}
#     Risk Aversion: {{ risk_aversion }}
#     """
#
#
# class MultipleSolutionGeneration(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 11: Multiple Solution Generation.
#     """
#     solutions: List[str] = Field(
#         ...,
#         description="List of potential solutions generated based on explicit information."
#     )
#     supporting_information: List[str] = Field(
#         ...,
#         description="Explicit information from the problem statement supporting each solution."
#     )
#
#     source: str = """
#     Solutions:
#     {% for solution in solutions %}
#     - {{ solution }}
#     {% endfor %}
#
#     Supporting Information:
#     {% for info in supporting_information %}
#     - {{ info }}
#     {% endfor %}
#     """
#
#
# class QuickestAndEasiestSolution(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 12: Quickest and Easiest Solution.
#     """
#     simplest_solution: str = Field(
#         ...,
#         description="The simplest and safest solution based ONLY on explicit information."
#     )
#     reasoning: List[str] = Field(
#         ...,
#         description="Exact quotes from the problem statement supporting the simplest solution."
#     )
#
#     source: str = """
#     Simplest Solution: {{ simplest_solution }}
#
#     Reasoning:
#     {% for reason in reasoning %}
#     - {{ reason }}
#     {% endfor %}
#     """
#
#
# class Reflection(DSLModel, TypedTemplate):
#     """
#     Pydantic model for REAP Step 13: Reflection.
#     """
#     contradictions_check: bool = Field(
#         default=True,
#         description="Review solutions and check for contradictions with known/deduced information."
#     )
#     assumptions_revised: bool = Field(
#         default=True,
#         description="Revise any assumptions or inferences that went beyond the explicit problem wording."
#     )
#
#     source: str = """
#     Contradictions Check: {{ contradictions_check }}
#     Assumptions Revised: {{ assumptions_revised }}
#     """


class FinalOutputAndRecommendation(DSLModel, TypedTemplate):
    """
    Pydantic model for REAP Step 14: Final Output and Recommendation.
    """
    comprehensive_feature_list: List[str] = Field(
        ...,
        description="List of all features (with explicit quotes) identified during the analysis."
    )
    sequential_and_mechanical_check: Optional[str] = Field(
        None,
        description="Summary of the sequential and mechanical process checks."
    )
    key_insight_results: Optional[str] = Field(
        None,
        description="Results from the key insight check."
    )
    rephrased_question: Optional[str] = Field(
        None,
        description="Simplified version of the core question."
    )
    known_and_deduced_information: List[str] = Field(
        ...,
        description="Known and deduced information used to answer the question."
    )
    problem_decomposition: List[str] = Field(
        ...,
        description="Breakdown of the problem into key components."
    )
    graph_of_thought: List[str] = Field(
        ...,
        description="Connections and insights from the graph of thought analysis."
    )
    spatial_and_object_analysis: List[str] = Field(
        ...,
        description="Summary of the spatial relationships and objects identified. MUST BE LIST"
    )
    bayesian_updates: Optional[str] = Field(
        None,
        description="Any updates based on Bayesian thinking."
    )
    ethical_check: str = Field(
        ...,
        description="Summary of ethical checks and decision-making steps."
    )
    multiple_solutions: List[str] = Field(
        ...,
        description="List of potential solutions."
    )
    quickest_solution: str = Field(
        ...,
        description="The simplest and safest solution, based on explicit information."
    )
    reflection_summary: str = Field(
        ...,
        description="Summary of reflections and final review."
    )
    recommendation: str = Field(
        ...,
        description="Final recommendation based on explicit information, prioritizing safety and ethics."
    )



# Example usage for one of the models
# rule = LiteralInterpretationRule(
#     problem_statements=["The box is red", "It is heavy"],
#     straightforward_interpretation=True
# )
#
# # Render the template for the model
# output = rule.render()
# print(output)

def main():
    """Main function"""
    from sungen.utils.dspy_tools import init_text, init_instant
    # init_text()
    init_instant()

#     bay = BayesianThinking.from_prompt("""A farmer wants to cross a river and take with him a wolf, a goat, and a
# cabbage. He has a boat with three secure separate compartments. If the wolf and the
# goat are alone on one shore, the wolf will eat the goat. If the goat and the cabbage are
# alone on the shore, the goat will eat the cabbage. How can the farmer efficiently bring
# the wolf, the goat, and the cabbage across the river without anything being eaten?""")
#     print(bay)

    rec = FinalOutputAndRecommendation.from_prompt("""A farmer wants to cross a river and take with him a wolf, a goat, and a
cabbage. He has a boat with three secure separate compartments. If the wolf and the
goat are alone on one shore, the wolf will eat the goat. If the goat and the cabbage are
alone on the shore, the goat will eat the cabbage. How can the farmer efficiently bring
the wolf, the goat, and the cabbage across the river without anything being eaten?

""")
    print(rec.recommendation)


if __name__ == '__main__':
    main()

