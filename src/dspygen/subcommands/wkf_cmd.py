import typer

from dspygen.utils.cli_tools import chatbot
from dspygen.workflow.workflow_executor import execute_workflow
from dspygen.workflow.workflow_models import Workflow

app = typer.Typer(help="Language Workflow Domain Specific Language commands for DSPyGen.")


@app.command("run")
def run_workflow(yaml_file: str = typer.Argument("/Users/sac/dev/dspygen/src/dspygen/experiments/workflow/control_flow_workflow.yaml")):
    """
    Run a workflow defined in a YAML file. Default is workflow.yaml
    """
    wf = Workflow.from_yaml(yaml_file)
    result = execute_workflow(wf)
    # print(result)


TUTOR_CONTEXT = '''The DSPyGen DSL has several key elements that you'll need to grasp:

Signatures (SignatureDSLModel) Think of signatures as blueprints for your AI modules. They define:

Name: A unique identifier for the signature.
Docstring: Explains the purpose of the signature.
Inputs (InputFieldModel): The information the module needs to function. Each input field has a name, description, and optional prefix for additional labeling.
Outputs (OutputFieldModel): The data the module will generate. Like inputs, each output field is described (name, description, optional prefix).
Modules (ModuleDSLModel) Modules are the building blocks of your AI workflow. They contain:

Name: Used to reference the module within the workflow.
Signature: Associates the module with a specific signature.
Predictor: Indicates the type of predictor needed (Predict or ChainOfThought).
Args: A list of arguments passed to the module when it runs.
Workflow Steps (StepDSLModel) Steps outline the sequential actions in your workflow. A step includes:

Module: The name of the module to run.
Signature: If necessary, the signature to use within the module.
lm_model: The language model for the step.
rm_model: The retrieval model for the step (if applicable).
args: Specific arguments for the module in that step.
Configuration (LanguageModelConfig, RetrievalModelConfig, WorkflowConfigModel) This section handles essential settings:

Language Models: Defines the language models you'll use (with labels for referencing).
Retrieval Models: Does the same thing for retrieval models.
Global Signatures: Signatures available throughout the workflow.
Current Step: Tracks the active step (optional).
Workflow Creation (The WorkflowDSLModel)

The WorkflowDSLModel ties everything together. It's your workflow's master structure, containing lists of all your signatures, modules, steps, and configurations, along with:

Context: A dictionary for global values shared across the workflow.
Putting it into Practice: A Simple Example

```python
# workflow_models.py
class WorkflowDSLModel(BaseModel, YAMLMixin):
    lm_models: list[LanguageModelConfig] = Field(default=[], description="list of language model configurations used in the workflow.")
    rm_models: list[RetrievalModelConfig] = Field(default=[], description="list of retrieval model configurations used in the workflow.")
    signatures: list[SignatureDSLModel] = Field(default=[], description="list of signatures defined for use in the workflow.")
    modules: list[ModuleDSLModel] = Field(default=[], description="list of modules defined for execution in the workflow.")
    steps: list[StepDSLModel] = Field(default=[], description="Sequential steps to be executed in the workflow.")
    context: dict = Field(default={}, description="A context dictionary for storing global values accessible across the workflow.")
    config: WorkflowConfigModel = Field(default_factory=WorkflowConfigModel, description="Configuration settings for the workflow execution.")
```                                        

Let's imagine a basic text summarization workflow:

```yaml
# example_workflow.yaml
lm_models:
  - label: "default"
    name: "OpenAI"
    args:
      model: "gpt-3.5-turbo"
      max_tokens: 4096
  - label: "fast"
    name: "OpenAI"
    args:
      model: "gpt-3.5-turbo"
      max_tokens: 2048
  - label: "slow"
    name: "T5Large"
    args:
      model: "fine-tuned-t5-large-1234"
      max_tokens: 100

rm_models:
  - label: "default"
    name: "ColBERTv2"

signatures:
  - name: "ProcessDataSignature"
    docstring: "Processes raw data to synthesize into a structured format suitable for report generation."
    inputs:
      - name: "raw_data"
        desc: "Raw data input that needs processing."
      - name: "data_format"
        desc: "The desired format of the output data."
    outputs:
      - name: "processed_data"
        desc: "Data processed into a structured format."
  - name: "GenerateReportSignature"
    docstring: "Generates a comprehensive report from structured data."
    inputs:
      - name: "processed_data"
        desc: "Structured data to be included in the report."
      - name: "report_template"
        desc: "Template specifying the report's format and structure."
    outputs:
      - name: "report"
        desc: "The final report generated from the structured data."

modules:
  - name: "DataProcessorModule"
    signature: "ProcessDataSignature"
    predictor: "Predict"
    args:
      - name: "raw_data"
        value: "{{ user_input }}"
      - name: "data_format"
        value: "JSON"

  - name: "ReportGeneratorModule"
    signature: "GenerateReportSignature"
    predictor: "ChainOfThought"
    args:
      - name: "report_template"
        value: "StandardReportTemplate"

steps:
  - module: "DataProcessorModule"
    lm_model: "default"
    args:
      raw_data: "id, name, age\n1, John, 25\n2, Jane, 30"
      data_format: "YAML"

  - module: "ReportGeneratorModule"
    lm_model: "fast"
    args:
      processed_data: "{{ processed_data }}"
      report_template: "templates/standard_report.html"
```

```yaml
# sql_to_natural_signature.yaml
lm_models:
  - label: "default"
    name: "OpenAI"
    args:
      max_tokens: 3000

steps:
  - signature: "signature/sql_to_natural_signature.yaml"
```

```yaml
# signature/sql_to_natural_signature.yaml
docstring: Generates a natural language description of an SQL query.
inputs:
- desc: The SQL query to be translated into natural language.
  name: query
  prefix: ''
name: SQLQueryToNL
outputs:
- desc: The natural language description of the SQL query.
  name: description
  prefix: ''
- desc: The optimized SQL query.
  name: optimized_query
  prefix: '```sql'
```

Use code with caution.
The Role of a DSPyGen Tutor

A DSPyGen tutor could provide the following:

Interactive Guidance: Step-by-step walkthroughs for creating and modifying workflow components (signatures, modules, etc.).
DSL Explanation: Breakdowns of syntax and the purpose of each DSL element.
Best Practices: Tips on designing efficient and modular workflows.
Example Workflows: Showcases of common use cases to illustrate DSL usage.
Debugging Help: Assistance with troubleshooting DSL implementation and workflow execution.

'''


@app.command(name="tutor")
def tutor(question: str = ""):
    """Guide you through developing a project with DSPyGen DSL."""
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy(max_tokens=3000, model="gpt-4")
    chatbot(question, TUTOR_CONTEXT)