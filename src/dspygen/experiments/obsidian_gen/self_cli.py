import os
import typer
from pathlib import Path
from logic import load_yaml, generate_scenarios, generate_code, modify_code
from utils.log import Logger

app = typer.Typer()

VAULT_DIR = "/Users/sac/dev/vault/myvault"


def scan_notes(directory: str):
    """
    Recursively scan all markdown (.md) files in the vault directory.
    """
    notes = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                note_path = os.path.join(root, file)
                with open(note_path, 'r') as f:
                    content = f.read()
                    notes.append((note_path, content))
    return notes


def extract_scenarios_from_notes(notes):
    """
    Extract scenarios from notes using simple NLP and pattern matching.
    This can be improved with ML or more advanced NLP if needed.
    """
    scenarios = []
    for note_path, content in notes:
        # Heuristic to find Gherkin-like structure in notes
        lines = content.splitlines()
        feature_name = None
        scenario_steps = []
        in_scenario = False

        for line in lines:
            if line.lower().startswith("feature:"):
                feature_name = line[8:].strip()
            elif line.lower().startswith("scenario:"):
                if in_scenario and scenario_steps:
                    scenarios.append({"feature": feature_name, "steps": scenario_steps})
                    scenario_steps = []
                in_scenario = True
                scenario_steps.append(line.strip())
            elif line.strip().startswith("Given") or line.strip().startswith("When") or line.strip().startswith("Then"):
                scenario_steps.append(line.strip())

        # If we end on a scenario
        if in_scenario and scenario_steps:
            scenarios.append({"feature": feature_name, "steps": scenario_steps})

    return scenarios


def parse_scenarios_to_yaml(scenarios):
    """
    Convert extracted scenarios to a YAML format for Gherkin generation.
    """
    yaml_data = []
    for scenario in scenarios:
        feature_name = scenario["feature"]
        steps = scenario["steps"]

        yaml_data.append({
            "feature_name": feature_name,
            "scenarios": [{
                "name": "Extracted Scenario",
                "description": steps[0],  # Simplistic, assuming the first line is the description
                "steps": steps[1:]  # Remaining lines as steps
            }]
        })

    return yaml_data


def apply_modifications(notes, generated_code):
    """
    Use notes to apply modifications or suggestions to the generated code.
    Look for sections that seem like instructions for modifications.
    """
    for note_path, content in notes:
        lines = content.splitlines()
        for line in lines:
            if "modify" in line.lower() or "improve" in line.lower():
                # Use some heuristic or pattern matching to find suggestions
                suggestion = line.strip()
                typer.echo(f"Applying suggestion: {suggestion}")
                modified_code, _ = modify_code(suggestion, generated_code)
                generated_code = modified_code

    return generated_code


@app.command()
def run_self_play():
    """
    Run the self-play loop using notes from the vault to generate scenarios, create code,
    and apply modifications in a loop.
    """
    # 1. Scan the vault
    notes = scan_notes(VAULT_DIR)
    typer.echo(f"Found {len(notes)} notes in the vault.")

    # 2. Extract scenarios from the notes
    scenarios = extract_scenarios_from_notes(notes)
    if not scenarios:
        typer.echo("No scenarios found.")
        raise typer.Exit()

    # 3. Convert extracted scenarios into YAML format
    yaml_scenarios = parse_scenarios_to_yaml(scenarios)

    # 4. Run through each scenario, generate code, and apply modifications
    for yaml_data in yaml_scenarios:
        # Load the scenario data as a Pydantic Feature model
        feature = Feature(**yaml_data)

        # 5. Generate the code from the scenario
        generated_code, _ = generate_code(feature)

        # 6. Apply modifications to the generated code based on notes
        modified_code = apply_modifications(notes, generated_code)

        # Log and output the results for each loop
        typer.echo(f"Generated and modified code:\n{modified_code}")


if __name__ == "__main__":
    app()
