"""
This code imports the necessary libraries and modules to run the DFLSSModule.
"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class DesignForLeanSixSigma(dspy.Signature):
    """
    Processes a design scenario to generate detailed, tailored documentation that incorporates lean six sigma methodologies.
    This allows for specification of the type of documentation required, ensuring outputs are customized to guide improvements
    in design efficiency and effectiveness based on user-defined criteria.
    """
    scenario_description = dspy.InputField(
        desc="A comprehensive description of the project or design process under review.")
    document_type = dspy.InputField(
        desc="Specify the type of lean six sigma document required. Options include but are not limited to: Voice of the Customer, "
             "Quality Function Deployment, Target Costing, Scorecards, Intro to Minitab, Basic Statistics, Understanding Variation "
             "and Control Charts, Measurement Systems Analysis, Process Capability, Concept Generation, TRIZ for New Product Design, "
             "Transactional TRIZ, Concept Selection – Pugh and AHP, Statistical Tolerance Design, Monte Carlo Simulation, Hypothesis "
             "Testing, Confidence Intervals, Testing Means, Medians, and Variances, Proportion and Chi-Square, Simple and Multiple "
             "Regression, Multi-Vari Analysis, Design FMEA, Detailed Design, 2-Way ANOVA, Intro to Design of Experiments, Full-Factorial "
             "DOE, Fractional Factorial DOE, DOE Catapult Simulation, Key Lean Concepts, Lean Design, Design for Manufacture and Assembly, "
             "Intro to Reliability, Design of Experiments with Curvature, Conjoint Analysis, Mixture Designs, Robust Design, Helicopter "
             "RSM Simulation, Prototype and Pilot, Process Control, Implementation Planning, DMEDI Capstone.")
    dflss_documentation = dspy.OutputField(
        desc="Customized lean six sigma documentation for specified document type. Written in the style of a "
             "Master Black Belt", prefix="Here is the generated document:\n\n```markdown\n # Document")


class DFLSSModule(dspy.Module):
    """DFLSSModule"""

    def forward(self, scenario_description, document_type):
        pred = dspy.ChainOfThought("scenario_description -> dflss_documentation")
        result = pred(scenario_description=scenario_description, document_type=document_type).dflss_documentation
        return result


def dflss_call(scenario_description, document_type, to=None):
    dflss = DFLSSModule()
    output = dflss.forward(scenario_description=scenario_description, document_type=document_type)
    if to:
        # Write the output to a file
        with open(to, "w") as f:
            f.write(output)
    return output


charter = """
Business Case:
The current order processing system, implemented via a finite state machine, is functional but lacks the flexibility and modularity needed for easy scalability and maintenance. By integrating DSPy, the system can benefit from more structured data handling, automatic state management, and enhanced debugging capabilities through systematic logging and validation.

Project Scope:
Convert existing order processing methods and transitions into DSPy-compatible modules.
Use DSPy's capabilities to handle different states of an order's lifecycle within a declarative pipeline environment.
Implement validation and action triggers as modular components.
Integrate state change triggers with conditions and actions based on DSPy’s event-driven architecture.
Maintain all functionality within Python, ensuring no external system dependencies at this stage.
"""


def main():
    from dspygen.lm.groq_lm import Groq
    init_dspy(Groq, 1000, "mixtral-8x7b-32768")
    # init_dspy(Groq, max_tokens=1000, model="llama3-70b-8192")  # for Groq you must pass an Groq provided model
    scenario_description = charter
    document_type = "Requirement Analysis Document"

    # Add the project charter as the scenario description
    print(dflss_call(scenario_description=scenario_description,
                     document_type=document_type,
                     to="dflss_output.txt"))


if __name__ == "__main__":
    main()
