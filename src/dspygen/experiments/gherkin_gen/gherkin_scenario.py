from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime

from sungen.utils.yaml_tools import YAMLMixin


class GherkinScenario(BaseModel, YAMLMixin):
    """A Pydantic model representing a Gherkin Scenario."""
    name: str = Field(default=None, title="", description="The name of the scenario.", min_length=1, max_length=255)
    description: str = Field(default=None, title="", description="A brief description of the scenario.", min_length=1, max_length=255)
    steps: list[str] = Field(default=[], title="", description="A list of steps in the scenario.")

