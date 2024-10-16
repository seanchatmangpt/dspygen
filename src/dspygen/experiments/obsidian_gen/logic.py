import os
import sys
import time
import yaml
from pydantic import ValidationError, BaseModel
from pathlib import Path


# ---------- Pydantic Models for YAML Schema ----------
class Scenario(BaseModel):
    name: str
    description: str
    steps: list[str]


class Feature(BaseModel):
    feature_name: str
    scenarios: list[Scenario]


# Core code generation logic instance
# codegeneration = CodeGeneration()
# db_tools = DB_Tools()


def read_logs(log_file_path: str = "logs/logs.log") -> str:
    sys.stdout.flush()
    with open(log_file_path, "r") as f:
        return f.read()


def load_yaml(file_path: str) -> Feature:
    """
    Load YAML input and validate it against the Pydantic model.
    """
    with open(file_path, 'r') as stream:
        try:
            return Feature(**yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            raise RuntimeError(f"Error reading YAML: {exc}")
        except ValidationError as ve:
            raise RuntimeError(f"Validation error: {ve}")


def generate_scenarios(feature: Feature):
    """
    Logic for generating scenarios from a YAML feature input.
    """
    feature2scenarios_list = db_tools.select_all()
    similar_Feature2Scenarios = codegeneration.TopN_Feature2Scenarios(
        feature2scenarios_list, feature.feature_name)

    # Gherkin Response Generation
    Gherkin_response, messages = codegeneration.Gherkin_generation(feature.feature_name, similar_Feature2Scenarios)

    # Parse the Gherkin response to scenarios
    Scenarios_List = codegeneration.Scenario_Parsing(Gherkin_response)

    # Convert Gherkin to Natural Language (NL)
    Gherkin_NL_List = codegeneration.Gherkin2NL(Scenarios_List, messages)

    # Optionally, insert into the database
    db_tools.insert(feature.feature_name, Gherkin_NL_List)

    return Gherkin_NL_List


def generate_code(feature: Feature):
    """
    Generate code based on the Gherkin scenarios provided in YAML.
    """
    codegeneration.clear_static_html_dir()

    Gherkin_NL_List = [scenario.description for scenario in feature.scenarios]

    # Insert scenarios into the database
    db_tools.insert(feature.feature_name, Gherkin_NL_List)

    # Convert Natural Language to Gherkin
    Gherkin_result = codegeneration.NL2Gherkin(Gherkin_NL_List, feature.feature_name)

    # Generate Design page template
    Design_page_template = codegeneration.Design_page_template_generation(Gherkin_result)

    # Generate Visual design template
    Visual_design_template = codegeneration.Visual_design_template_generation(Design_page_template)

    # Generate the code based on visual and design templates
    Generated_code, loop_number = codegeneration.Code_generation(
        Visual_design_template, Design_page_template, feature.feature_name, Gherkin_result)

    # Create the output HTML file and zip it
    output_path = os.path.join(codegeneration.args.static_dir, "html.zip")
    zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)

    return Generated_code, output_path


def modify_code(suggestion: str, generated_code: str):
    """
    Modify generated code based on suggestions.
    """
    codegeneration.clear_static_html_dir()

    modified_code, messages, loop_number = codegeneration.Code_Modification(
        generated_code, suggestion)

    output_path = os.path.join(codegeneration.args.static_dir, "html.zip")
    zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)

    return modified_code, output_path


def modify_design(suggestion: str, generated_code: str):
    """
    Modify design based on suggestions.
    """
    codegeneration.clear_static_html_dir()

    modified_code, messages, loop_number = codegeneration.Design_Modification(
        generated_code, suggestion)

    output_path = os.path.join(codegeneration.args.static_dir, "html.zip")
    zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)

    return modified_code, output_path
