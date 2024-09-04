import typer
import os
from pathlib import Path
import yaml
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dspygen.utils.cli_tools import chatbot
from dspygen.workflow.workflow_executor import execute_workflow, schedule_workflow
from dspygen.workflow.workflow_models import Workflow, Job
from sungen.typetemp.functional import render
from dspygen.utils.file_tools import rm_dir

app = typer.Typer(help="Language Workflow Domain Specific Language commands for DSPyGen.")

# Workflow template
workflow_template = """
name: {{ name }}
triggers:
  - cron: "0 0 * * *"  # Daily at midnight

jobs:
  - name: ExampleJob
    runner: python
    steps:
      - name: ExampleStep
        code: |
          print("Hello from {{ name }} workflow!")

"""

def wf_dir():
    """Returns the directory where workflows are stored."""
    return os.path.join(os.path.dirname(__file__), "..", "workflows")

@app.command("new")
def new_workflow(name: str = typer.Argument(...)):
    """Generates a new workflow YAML file."""
    to = wf_dir()
    os.makedirs(to, exist_ok=True)
    file_path = os.path.join(to, f"{name.lower()}_workflow.yaml")
    
    content = render(workflow_template, name=name)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    typer.echo(f"New workflow created at: {file_path}")
    typer.echo("Workflow content:")
    typer.echo(content)

@app.command("run")
def run_workflow(yaml_file: str = typer.Argument("/Users/sac/dev/dspygen/src/dspygen/experiments/workflow/control_flow_workflow.yaml")):
    """
    Run a workflow defined in a YAML file. Default is workflow.yaml
    """
    wf = Workflow.from_yaml(yaml_file)
    result = execute_workflow(wf)
    typer.echo(f"Workflow execution result: {result}")

def run_workflows_in_directory(directory: str, recursive: bool = True):
    """
    Run all YAML workflow files in the specified directory and its subdirectories.
    """
    scheduler = BackgroundScheduler()
    scheduler.start()

    workflows_found = False

    def process_workflow_file(file_path):
        nonlocal workflows_found
        try:
            workflow = Workflow.from_yaml(file_path)
            typer.echo(f"Scheduling workflow from file: {file_path}")
            schedule_workflow(workflow, scheduler)
            workflows_found = True
        except Exception as e:
            typer.echo(f"Error processing workflow file {file_path}: {str(e)}", err=True)

    def search_workflows(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(('.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    process_workflow_file(file_path)
            if not recursive:
                break  # Stop after processing the top-level directory

    search_workflows(directory)

    if not workflows_found:
        typer.echo("No workflows found or scheduled.")
        scheduler.shutdown()
        return None

    return scheduler

@app.command("run-all")
def run_all_workflows(
    directory: str = typer.Argument(".", help="Directory containing YAML workflow files"),
    recursive: bool = typer.Option(True, help="Search subdirectories recursively")
):
    """
    Run all YAML workflow files in the specified directory and its subdirectories.
    """
    scheduler = run_workflows_in_directory(directory, recursive)
    if scheduler:
        typer.echo("All workflows scheduled. Press Ctrl+C to exit.")
        try:
            # Keep the script running
            scheduler.print_jobs()
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            typer.echo("Shutting down scheduler...")
            scheduler.shutdown()
            typer.echo("Scheduler shut down. Exiting.")

TUTOR_CONTEXT = '''The DSPyGen DSL has several key elements that you'll need to grasp:

Signatures (SignatureDSLModel) Think of signatures as blueprints for your AI dspy_modules. They define:

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

The WorkflowDSLModel ties everything together. It's your workflow's master structure, containing lists of all your signatures, dspy_modules, steps, and configurations, along with:

Context: A dictionary for global values shared across the workflow.
Putting it into Practice: A Simple Example

```python
# workflow_models.py
class WorkflowDSLModel(BaseModel, YAMLMixin):
    lm_models: list[LanguageModelConfig] = Field(default=[], description="list of language model configurations used in the workflow.")
    rm_models: list[RetrievalModelConfig] = Field(default=[], description="list of retrieval model configurations used in the workflow.")
    signatures: list[SignatureDSLModel] = Field(default=[], description="list of signatures defined for use in the workflow.")
    dspy_modules: list[ModuleDSLModel] = Field(default=[], description="list of dspy_modules defined for execution in the workflow.")
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

dspy_modules:
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

Interactive Guidance: Step-by-step walkthroughs for creating and modifying workflow components (signatures, dspy_modules, etc.).
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

@app.command("list")
def list_workflows(directory: str = typer.Argument(wf_dir(), help="Directory containing workflow files")):
    """List all workflows in a specified directory."""
    workflows = []
    for file in os.listdir(directory):
        if file.endswith(('.yaml', '.yml')):
            workflows.append(file)
    
    if workflows:
        typer.echo("Available workflows:")
        for wf in workflows:
            typer.echo(f"- {wf}")
    else:
        typer.echo("No workflows found in the specified directory.")

@app.command("show")
def show_workflow(workflow_name: str):
    """Display details about a specific workflow."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    typer.echo(f"Content of workflow {workflow_name}:")
    typer.echo(content)

@app.command("delete")
def delete_workflow(workflow_name: str):
    """Delete a specific workflow file."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    os.remove(file_path)
    typer.echo(f"Workflow {workflow_name} has been deleted.")

@app.command("trigger")
def trigger_workflow(workflow_name: str):
    """Manually trigger a specific workflow."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    result = execute_workflow(wf)
    typer.echo(f"Workflow {workflow_name} triggered. Execution result: {result}")

@app.command("pause")
def pause_workflow(workflow_name: str):
    """Pause a specific workflow."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    wf.paused = True
    wf.to_yaml(file_path)
    typer.echo(f"Workflow {workflow_name} has been paused.")

@app.command("unpause")
def unpause_workflow(workflow_name: str):
    """Unpause a specific workflow."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    wf.paused = False
    wf.to_yaml(file_path)
    typer.echo(f"Workflow {workflow_name} has been unpaused.")

@app.command("test")
def test_workflow(workflow_name: str):
    """Test a workflow without executing its tasks."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    typer.echo(f"Testing workflow: {workflow_name}")
    typer.echo(f"Number of jobs: {len(wf.jobs)}")
    for job in wf.jobs:
        typer.echo(f"  Job: {job.name}")
        typer.echo(f"    Number of steps: {len(job.steps)}")
    typer.echo("Workflow structure is valid.")

@app.command("list-jobs")
def list_jobs(workflow_name: str):
    """List all jobs in a specific workflow."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    typer.echo(f"Jobs in workflow {workflow_name}:")
    for job in wf.jobs:
        typer.echo(f"- {job.name}")

@app.command("test-job")
def test_job(workflow_name: str, job_name: str):
    """Test a specific job in a workflow."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    job = next((job for job in wf.jobs if job.name == job_name), None)
    if not job:
        typer.echo(f"Job {job_name} not found in workflow {workflow_name}.")
        return
    
    typer.echo(f"Testing job: {job_name}")
    typer.echo(f"Number of steps: {len(job.steps)}")
    for step in job.steps:
        typer.echo(f"  Step: {step.name}")
        typer.echo(f"    Code: {step.code[:50]}...")  # Show first 50 characters of code
    typer.echo("Job structure is valid.")

@app.command("clear-job")
def clear_job(workflow_name: str, job_name: str):
    """Clear the state of a specific job instance."""
    file_path = os.path.join(wf_dir(), f"{workflow_name}.yaml")
    if not os.path.exists(file_path):
        typer.echo(f"Workflow {workflow_name} not found.")
        return
    
    wf = Workflow.from_yaml(file_path)
    job = next((job for job in wf.jobs if job.name == job_name), None)
    if not job:
        typer.echo(f"Job {job_name} not found in workflow {workflow_name}.")
        return
    
    # Implement job state clearing logic here
    typer.echo(f"Clearing state for job {job_name} in workflow {workflow_name}... (Not implemented)")

@app.command("backfill")
def backfill(workflow_name: str, start_date: str, end_date: str):
    """Run a workflow for a specified historical time range."""
    typer.echo(f"Backfilling workflow {workflow_name} from {start_date} to {end_date}... (Not implemented)")

@app.command("logs")
def show_logs(workflow_name: str, job_name: str):
    """Display logs for a specific job run."""
    typer.echo(f"Showing logs for job {job_name} in workflow {workflow_name}... (Not implemented)")

@app.command("export")
def export_workflow(workflow_name: str, output_file: str):
    """Export a workflow definition to a file."""
    typer.echo(f"Exporting workflow {workflow_name} to {output_file}... (Not implemented)")

@app.command("import")
def import_workflow(input_file: str):
    """Import a workflow definition from a file."""
    typer.echo(f"Importing workflow from {input_file}... (Not implemented)")

@app.command("scheduler-health")
def scheduler_health():
    """Check the status of the scheduler."""
    typer.echo("Checking scheduler health... (Not implemented)")

@app.command("version")
def version():
    """Display the version of the workflow system."""
    typer.echo("Workflow system version: X.Y.Z (Not implemented)")

if __name__ == "__main__":
    app()