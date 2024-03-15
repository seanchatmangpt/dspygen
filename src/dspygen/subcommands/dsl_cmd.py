"""dsl"""
import typer

from dspygen.dsl.dsl_pipeline_executor import execute_pipeline

app = typer.Typer()


@app.command("run")
def run_pipeline(yaml_file: str = "pipeline.yaml"):
    """
    Run a pipeline defined in a YAML file. Default is pipeline.yaml
    """
    result = execute_pipeline(yaml_file)
    print(result)
