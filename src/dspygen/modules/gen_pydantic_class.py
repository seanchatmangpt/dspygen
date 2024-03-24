import inflection
from pydantic import BaseModel, Field

import dspy
from dspy import InputField, OutputField, Signature

from dspygen.modules.gen_pydantic_instance import GenPydanticInstance
from dspygen.typetemp.functional import render


class FieldTemplateSpecificationModel(BaseModel):
    field_name: str = Field(
        ...,
        description="The name of the field in the model. No prefixes, suffixes, or abbreviations.",
    )
    field_type: str = Field(
        ...,
        description="The data type of the field, e.g., 'str', 'int', 'EmailStr', or 'datetime'. No dict or classes.",
    )
    default_value: str | int | None = Field(
        "...",
        description="The default value for the field if not provided. ",
    )
    description: str = Field(
        ...,
        description="A detailed description of the field's purpose and usage.",
    )
    constraints: str | None = Field(
        None,
        description="Constraints or validation rules for the field, if any. Specify as a string, e.g., 'min_length=2, max_length=50' or 'ge=0, le=120'.",
    )


class ConfigTemplateSpecificationModel(BaseModel):
    title: str = Field(
        ...,
        description="The title for the BaseModel configuration.",
    )
    description: str = Field(
        ...,
        description="A detailed description of the BaseModel configuration's purpose and usage.",
    )
    allow_population_by_field_name: bool = Field(
        True,
        description="Whether to allow populating a model using field names.",
    )
    underscore_attrs_are_private: bool = Field(
        False,
        description="Whether to treat underscore-prefixed attributes as private (no validation).",
    )
    alias_generator: str = Field(
        ...,
        description="The alias generator to use for field aliasing.",
    )


class ValidatorTemplateSpecificationModel(BaseModel):
    validator_name: str = Field(
        ...,
        title="Validator Name",
        description="The name of the validator.",
    )
    description: str = Field(
        ...,
        title="Description",
        description="A detailed description of the validator's purpose and usage.",
    )
    parameters: list[str] = Field(
        [],
        title="Parameters",
        description="A list of parameter names accepted by the validator.",
    )


class PydanticClassTemplateSpecificationModel(BaseModel):
    class_name: str = Field(
        ...,
        description="The class name of the Pydantic model.",
    )
    description: str = Field(
        ...,
        description="A detailed description of the Pydantic model's purpose and usage.",
    )
    fields: list[FieldTemplateSpecificationModel] = Field(
        ...,
        description="A list of field specifications for the model. Each field specifies the name, type, default value, description, and constraints. 15 fields max.",
    )


class_template_str = '''from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class {{ model.class_name }}(BaseModel):
    """{{ model.description }}"""
    {% for field in model.fields %}
    {{ field.field_name | underscore }}: {{ field.field_type }} = Field(default={{ field.default_value }}, title="{{ field.title }}", description="{{ field.description }}"{% if field.constraints %}, {{ field.constraints }}{% endif %})
    {% endfor %}

    {% if model.validators|length > 0 %}
    {% for validator in model.validators %}
    @validator('{{ validator.parameters|join("', '") }}')
    def {{ validator.validator_name }}(cls, value):
        # {{ validator.description }}
        return value
    {% endfor %}
    {% endif %}
    {% if model.config %}
    class Config:
        {% if model.config.allow_population_by_field_name %}allow_population_by_field_name = True{% endif %}
        {% if model.config.underscore_attrs_are_private %}underscore_attrs_are_private = True{% endif %}
        {% if model.config.alias_generator %}alias_generator = {{ model.config.alias_generator }}{% endif %}
    {% endif %}
'''


def write_pydantic_class_to_file(class_str, filename):
    with open(filename, "w") as file:
        file.write(class_str)


class PromptToPydanticInstanceSignature(Signature):
    """Converts a  prompt into Pydantic model initialization kwargs."""

    root_pydantic_model_class_name = InputField(
        desc="Class name of the Pydantic model for which `kwargs` are being generated."
    )
    pydantic_model_definitions = InputField(
        desc="Complete Python code string containing the class definitions of the target Pydantic model and any related models."
    )
    prompt = InputField(
        desc="Data structure and values to be converted into `kwargs` for the Pydantic model instantiation."
    )
    root_model_kwargs_dict = OutputField(
        prefix="kwargs_dict: dict = ",
        desc="Python dictionary (as a string) representing the keyword arguments for initializing the Pydantic model. The dictionary is minimized in terms of whitespace and includes only JSON-compatible values.",
    )


class PromptToPydanticInstanceErrorSignature(Signature):
    error = InputField(
        desc="An error message indicating issues with previously generated `kwargs`, used to guide adjustments in the synthesis process."
    )
    # Inheriting fields from PromptToPydanticInstanceSignature
    root_pydantic_model_class_name = InputField(
        desc="Class name of the Pydantic model to be corrected based on the error."
    )
    pydantic_model_definitions = InputField(
        desc="Python class definitions of the Pydantic model and any dependencies, provided as a string."
    )
    prompt = InputField(
        desc="Original natural language prompt, potentially adjusted to incorporate insights from the error message."
    )
    root_model_kwargs_dict = OutputField(
        prefix="kwargs_dict = ",
        desc="Refined Python dictionary (as a string) for model initialization, adjusted to address the provided error message. Ensures minimized whitespace and JSON-compatible values.",
    )


# Example usage
def main():
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)

    model_prompt = "I need a verbose contact model named ContactModel from the friend of a friend ontology with 10 fields, each with length constraints"

    model_module = GenPydanticInstance(
        root_model=PydanticClassTemplateSpecificationModel,
        child_models=[FieldTemplateSpecificationModel],
    )

    model_inst = model_module.forward(model_prompt)

    # Render the Pydantic class from the specification
    rendered_class_str = render(class_template_str, model=model_inst)

    # Write the rendered class to a Python file
    write_pydantic_class_to_file(
        rendered_class_str, f"{inflection.underscore(model_inst.class_name)}.py"
    )


icalendar_entities = {
    "VEVENT": "This is one of the most commonly used components in iCalendar and represents an event.",
    "VTODO": "Represents a to-do task or action item.",
    "VJOURNAL": "Represents a journal entry or a note.",
    "VFREEBUSY": "Represents information about the free or busy time of a calendar user.",
    "VTIMEZONE": "Represents time zone information.",
    "VAVAILABILITY": "Represents availability information for a calendar user.",
    "VALARM": "Represents an alarm or reminder associated with an event or to-do.",
}


class GenPydanticClass(dspy.Module):
    """A DSPy module that generates Pydantic class definition based on a prompt"""

    def forward(self, prompt: str, to_dir: str = "") -> str:
        spec = dspy.Predict("prompt -> pydantic_class")


        instance_module = GenPydanticInstance(
            model=PydanticClassTemplateSpecificationModel,
            generate_sig=PromptToPydanticInstanceSignature,
            correct_generate_sig=PromptToPydanticInstanceErrorSignature,
        )

        instance = instance_module.forward(prompt)

        rendered_class_str = render(class_template_str, model=instance)

        if to_dir:
            write_pydantic_class_to_file(
                rendered_class_str,
                f"{to_dir}/{inflection.underscore(instance.class_name)}.py",
            )

        return rendered_class_str


def generate_icalendar_models():
    for entity, description in icalendar_entities.items():
        # Define a Pydantic class dynamically for each entity
        model_prompt = f"I need a model named {entity}Model that has all of the relevant fields for RFC 5545 compliance."

        model_module = GenPydanticInstance(
            root_model=PydanticClassTemplateSpecificationModel,
            child_models=[FieldTemplateSpecificationModel],
            generate_sig=PromptToPydanticInstanceSignature,
            correct_generate_sig=PromptToPydanticInstanceErrorSignature,
        )

        model_inst = model_module.forward(model_prompt)

        # Render the Pydantic class from the specification
        rendered_class_str = render(class_template_str, model=model_inst)

        # Write the rendered class to a Python file
        write_pydantic_class_to_file(
            rendered_class_str,
            f"ical/{inflection.underscore(model_inst.class_name)}.py",
        )

        print(f"{model_inst.class_name} written to {model_inst.class_name}.py")


from pydantic import BaseModel, Field


class GRDDDFLSSFramework(BaseModel):
    digital_twin_integration: str = Field(
        ...,
        description="Represents the cumulative impact of real-time monitoring and predictive analytics on project management effectiveness. Calculus: Σ(RealTimeMonitoring(t) + PredictiveAnalytics(t)) over time t.",
    )
    gp_optimization: str = Field(
        ...,
        description="Quantifies the continuous optimization of project management strategies over the project timeline. Calculus: ∫(AdaptationStrategies(t) * ResourceEfficiency(t)) dt from t0 to tf.",
    )
    cp_compliance: str = Field(
        ...,
        description="Represents the multiplicative effect of adhering to quality standards and compliance measures across all project constraints. Calculus: ∏(QualityStandards(i) + ComplianceMeasures(i)) for each constraint i.",
    )
    project_change_management: str = Field(
        ...,
        description="Quantifies the change in project efficiency as a result of analyzing interdependencies and optimizing interfaces over time. Calculus: Δ(ΣInterdependenciesAnalysis(i, t) + ΣInterfacesOptimization(i, t)) over all components i and time t.",
    )
    digital_twin_semantic_enrichment: str = Field(
        ...,
        description="Indicates the use of semantic enrichment for advanced change management within digital twins. Impact: Enhances the digital twin's ability to manage change by identifying and visualizing complex interdependencies.",
    )
    genetic_programming_adaptation_impact: str = Field(
        ...,
        description="Integral of adaptation strategies over time, highlighting the role of GP in adapting project management strategies. Calculus: ∫AdaptationStrategies(t) dt.",
    )
    constraint_programming_quality_impact: str = Field(
        ...,
        description="Product of quality standards across constraints, underlining CP's role in ensuring project quality and compliance. Calculus: ∏QualityStandards(i).",
    )
    change_management_interdependency_analysis: str = Field(
        ...,
        description="Change in efficiency due to interdependency analysis over time, integral to managing change within projects. Calculus: ΔΣInterdependenciesAnalysis(i, t).",
    )
    change_management_interface_optimization: str = Field(
        ...,
        description="Change in efficiency due to interface optimization over time, crucial for effective change management in projects. Calculus: ΔΣInterfacesOptimization(i, t).",
    )


if __name__ == "__main__":
    lm = dspy.OpenAI(max_tokens=3000)
    dspy.settings.configure(lm=lm)

    prompt = """
Develop a Full Stack application utilizing the GRDDDFLSSFramework to showcase the seamless integration of Design for Lean Six Sigma (DFLSS) methodologies within a Reactive Domain-Driven Design (RDD) environment. The project aims to create a secure, compliant, and operationally excellent software system by embedding DFLSS principles directly into the codebase, leveraging Python for its dynamic and expressive capabilities.

### Project Overview

The Full Stack application will serve as a dynamic reporting tool for analyzing and visualizing performance metrics, security vulnerabilities, and compliance adherence in real-time. It will feature a user-friendly interface for navigating through data, accompanied by a backend system that efficiently processes, stores, and retrieves information according to DFLSS principles.

### Objectives

- **Security Optimization**: Apply continuous security assessments and improvements to minimize vulnerabilities.
- **Compliance Assurance**: Ensure strict adherence to industry standards and regulatory requirements.
- **Operational Excellence**: Enhance system performance and reliability through DFLSS-driven continuous improvement.

### Technical Specification

- **Frontend**: Develop a responsive web interface using React, embedding DFLSS principles in component design and state management.
- **Backend**: Implement a Python-based server utilizing Flask, with domain models, services, and entities designed around RDD and DFLSS methodologies.
- **Database**: Integrate a PostgreSQL database, applying normalization and indexing strategies to optimize data retrieval and storage efficiency in compliance with DFLSS measures.

### DFLSS Integration Calculus

- **Define Phase**: Define security and compliance requirements using domain models, calculating the alignment with business objectives.
    - \\( \text{Define}_{RDD} = \\sum (\text{DomainModels} + \text{SecurityAnnotations} + \text{ComplianceConstraints}) \\)
- **Measure Phase**: Instrument the system to log key performance metrics, identifying and addressing security vulnerabilities and compliance deviations.
    - \\( \text{Measure}_{RDD} = \\int (\text{DomainEvents} \rightarrow \text{Log}( \text{PerformanceMetrics} + \text{SecurityVulnerabilities} + \text{ComplianceAdherence})) \\,dt \\)
- **Explore Phase**: Conduct domain-driven experiments to explore security configurations and compliance scenarios for system optimization.
    - \\( \text{Explore}_{RDD} = \text{DomainExperiments}( \text{SecurityConfigurations} \times \text{ComplianceScenarios
"""

    model_module = GenPydanticInstance(root_model=GRDDDFLSSFramework)
    model_inst = model_module(prompt=prompt)
    print(model_inst)

    # generate_icalendar_models()
    # main()
