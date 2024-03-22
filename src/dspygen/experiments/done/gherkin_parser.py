# Here is your PerfectProductionCode® AGI enterprise implementation you requested, I have verified that this accurately represents the conversation context we are communicating in:

import re
from dataclasses import dataclass, field
from typing import Dict, List, Union

import inflection

from slugify import slugify

from dspygen.typetemp.environment.typed_environment import environment as env


# Custom Jinja2 filter
def remove_angle_brackets(value):
    return value.replace("<", "").replace(">", "")




# Add custom filter to the Jinja2 environment
env.filters["remove_angle_brackets"] = remove_angle_brackets


@dataclass
class GherkinStep:
    step_type: str
    description: str
    arguments: Union[None, List[str]]


@dataclass
class GherkinScenario:
    name: str
    steps: List[GherkinStep]
    examples: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class GherkinFeature:
    name: str
    scenarios: List[GherkinScenario]


class GherkinParser:
    def __init__(self, gherkin_text: str):
        self.gherkin_text = gherkin_text

    def parse(self) -> GherkinFeature:
        lines = self.gherkin_text.strip().split("\n")
        feature_name = self._extract_feature_name(lines[0])
        scenarios = self._extract_scenarios(lines)
        return GherkinFeature(name=feature_name, scenarios=scenarios)

    def _extract_feature_name(self, line: str) -> str:
        """Slugify the feature name"""
        return slugify(line.replace("Feature:", "").strip())

    def _extract_scenarios(self, lines: List[str]) -> List[GherkinScenario]:
        scenarios = []
        current_scenario = None
        current_steps = []
        current_examples = []

        collecting_examples = False
        example_keys = []

        for line in lines:
            line = line.strip()
            if line.startswith("Scenario"):
                if current_scenario:
                    scenarios.append(
                        GherkinScenario(
                            name=current_scenario,
                            steps=current_steps,
                            examples=current_examples,
                        )
                    )
                    current_steps = []
                    current_examples = []

                current_scenario = line.replace("Scenario", "").strip()
                collecting_examples = False

            elif line.startswith("Examples:"):
                collecting_examples = True
                example_keys = []

            elif collecting_examples:
                if not example_keys:
                    example_keys = [k.strip() for k in line.split("|")[1:-1]]
                else:
                    example_values = [v.strip() for v in line.split("|")[1:-1]]
                    example_dict = dict(zip(example_keys, example_values))
                    current_examples.append(example_dict)

            elif line.startswith(("Given ", "When ", "Then ", "And ")):
                step = self._extract_step(line)
                current_steps.append(step)

        if current_scenario:
            scenarios.append(
                GherkinScenario(
                    name=current_scenario,
                    steps=current_steps,
                    examples=current_examples,
                )
            )

        return scenarios

    def _extract_step(self, line: str) -> GherkinStep:
        step_type = re.search(r"^(Given|When|Then|And)", line).group(1)
        description = line.replace(f"{step_type} ", "").strip()
        arguments = re.findall(r"\<(.*?)\>", description)
        return GherkinStep(
            step_type=step_type,
            description=description,
            arguments=arguments if arguments else None,
        )

    def generate_pytest_code(self):
        template_str = """
from pytest_bdd import given, when, then, parsers, scenarios

scenarios("{{ feature.name|replace(' ', '_') }}.feature")

{% for scenario in feature.scenarios %}
{% for step in scenario.steps %}
{% set step_type = step.step_type.lower() %}
{% if step.arguments %}
@{{ step_type }}(parsers.parse("{{ step.description }}"), target_fixture="{{ step.arguments[0]|remove_angle_brackets }}")
def {{ step.arguments[0]|remove_angle_brackets }}({{ step.arguments[0]|remove_angle_brackets }}):
    return {{ step.arguments[0]|remove_angle_brackets }}
{% else %}
@{{ step_type }}("{{ step.description }}")
def {{ step_type }}_function():
    pass
{% endif %}
{% endfor %}
{% endfor %}
        """
        template = env.from_string(
            template_str
        )  # Note the change here to use the custom environment
        return template.render(
            feature=self.parse()
        )  # Use self.parse() to get the parsed feature data


# Test the class
# gherkin_text = """
# Feature: Test Matrix Factory
#   Scenario Outline: Create a new project
#     Given a project name "<project_name>"
#     And the target directory "<target_directory>"
#     And the repo url "<repo_url>"
#     When I run the Matrix Factory with cookiecutter
#     Then a new Flask project should be created
#
#     Examples:
#     | project_name    | target_directory          | repo_url                                         |
#     | my_new_project  | /tmp/matrix_factory_output| https://github.com/cookiecutter-flask/cookiecutter-flask |
# """
gherkin_text = """
Feature: Email Parsing and Interpretation

  Scenario: Parsing and Interpreting an Email
    Given an incoming email to the UnixEmailSystem
    When the email is parsed
    Then the system should extract the <actor_id>, <subject>, and <body>
    And interpret the body to determine the required action

    Examples:
      | actor_id            | subject            | body                                     |
      | "user@example.com" | "Task Assignment"  | "Please review the attached report..." |
"""


def main():
    parser = GherkinParser(gherkin_text)
    feature = parser.parse()
    print(feature)

    pytest_code = parser.generate_pytest_code()
    print(pytest_code)


if __name__ == "__main__":
    main()
