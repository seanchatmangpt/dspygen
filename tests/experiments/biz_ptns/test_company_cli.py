# test_my_cli.py
import pytest
from typer.testing import CliRunner
from unittest.mock import mock_open, patch


import typer
from typing import Optional
from pydantic import BaseModel, Field
import os
import yaml

from dspygen.lm.groq_lm import Groq
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.pydantic_tools import InstanceMixin
from dspygen.utils.yaml_tools import YAMLMixin

app = typer.Typer()

class Company(BaseModel, YAMLMixin, InstanceMixin):
    name: str = Field(..., description="The name of the company")
    address: str = Field(..., description="The physical address of the company")
    phone: str = Field(..., description="The contact phone number of the company")
    email: str = Field(..., description="The contact email of the company")
    business_model: str = Field(..., description="The business model of the company.")

FILENAME = "companies.yaml"

def save_companies(companies: dict):
    with open(FILENAME, "w") as file:
        yaml.dump(companies, file)

def load_companies() -> dict:
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME) as file:
        return yaml.safe_load(file)

@app.command()
def create(name: str, address: str, phone: str, email: Optional[str]):
    """Create a new company entry."""
    # companies = load_companies()
    # company = Company(name=name, address=address, phone=phone, email=email)
    # companies[name] = company.dict()
    # save_companies(companies)
    init_dspy(model="gpt-4")

    comp = Company.to_inst(f"{name}, {address}, {phone}, Business model: B2B.")

    print(comp)

    typer.echo(f"Company {name} added successfully.")

@app.command()
def read(name: Optional[str] = None):
    """Read and list all companies or a specific company by name."""
    companies = load_companies()
    if name:
        if name in companies:
            typer.echo(companies[name])
        else:
            typer.echo(f"Company {name} not found.")
    else:
        for company_name, details in companies.items():
            typer.echo(f"{company_name}: {details}")

@app.command()
def update(name: str, address: Optional[str] = None, phone: Optional[str] = None, email: Optional[str] = None):
    """Update an existing company's details."""
    companies = load_companies()
    if name in companies:
        company = Company(**companies[name])
        if address:
            company.address = address
        if phone:
            company.phone = phone
        if email:
            company.email = email
        companies[name] = company.dict()
        save_companies(companies)
        typer.echo(f"Company {name} updated successfully.")
    else:
        typer.echo(f"Company {name} not found.")

@app.command()
def delete(name: str):
    """Delete a company by name."""
    companies = load_companies()
    if name in companies:
        del companies[name]
        save_companies(companies)
        typer.echo(f"Company {name} deleted successfully.")
    else:
        typer.echo(f"Company {name} not found.")

# if __name__ == "__main__":
#     app()


runner = CliRunner()

@pytest.fixture
def mock_file_empty():
    with patch("builtins.open", mock_open(read_data="{}")) as mock_file:
        yield mock_file

@pytest.fixture
def mock_file_with_data():
    data = """
    Example Inc.: {'name': 'Example Inc.', 'address': '123 Example Lane', 'phone': '123-456-7890', 'email': 'contact@example.com'}
    """
    with patch("builtins.open", mock_open(read_data=data)) as mock_file:
        yield mock_file

# def test_create_company(mock_file_empty):
#     result = runner.invoke(app, ["create", "Example Inc.", "123 Example Lane", "123-456-7890", "contact@example.com"])
#
#     print(result.output)
#
#     assert "Company Example Inc. added successfully." in result.output


# def test_read_company_empty(mock_file_empty):
#     result = runner.invoke(app, ["read"])
#     assert not result.output.strip()  # No output expected for an empty file
#
# def test_read_specific_company_not_found(mock_file_with_data):
#     result = runner.invoke(app, ["read", "--name", "Nonexistent Inc."])
#     assert "Company Nonexistent Inc. not found." in result.output
#
# def test_read_all_companies(mock_file_with_data):
#     result = runner.invoke(app, ["read"])
#     assert "Example Inc." in result.output
#
# # Additional tests would follow a similar pattern for update and delete commands
#
