
import pytest
from typer.testing import CliRunner
from cli_app import app

runner = CliRunner()

def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{{ cli_api.metadata.version }}" in result.output

{% for command in cli_api.commands %}
def test_{{ command.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ command.name }}"])
    assert result.exit_code == 0
    assert "Executing {{ command.name }} command" in result.output

    {% for subcommand in command.subcommands %}
def test_{{ command.name.replace('-', '_') }}_{{ subcommand.name.replace('-', '_') }}():
    args = ["{{ command.name }}", "{{ subcommand.name }}"]
    {% for arg in subcommand.arguments %}
    args.append("test-{{ arg.name }}")
    {% endfor %}
    {% for option in subcommand.options %}
    args.extend(["{{ option.name }}", "test-value"])
    {% endfor %}
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "Executing {{ subcommand.name }} subcommand" in result.output
    {% endfor %}
{% endfor %}

{% for plugin in cli_api.plugins %}
def test_plugin_{{ plugin.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ plugin.name }}"])
    assert result.exit_code == 0
    # Add assertions as needed

    {% for command in plugin.commands %}
def test_plugin_{{ plugin.name.replace('-', '_') }}_{{ command.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ plugin.name }}", "{{ command.name }}"])
    assert result.exit_code == 0
    assert "Executing {{ command.name }} plugin command" in result.output
    {% endfor %}
{% endfor %}

{% for extension in cli_api.extensions %}
def test_extension_{{ extension.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ extensions.name }}"])
    assert result.exit_code == 0
    # Add assertions as needed

    {% for command in extension.commands %}
def test_extension_{{ extension.name.replace('-', '_') }}_{{ command.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ extensions.name }}", "{{ command.name }}"])
    assert result.exit_code == 0
    assert "Executing {{ command.name }} extensions command" in result.output
    {% endfor %}
{% endfor %}

{% if cli_api.marketplace %}
def test_marketplace_{{ cli_api.marketplace.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ cli_api.marketplace.name }}"])
    assert result.exit_code == 0
    # Add assertions as needed

    {% for subcommand in cli_api.marketplace.subcommands %}
def test_marketplace_{{ cli_api.marketplace.name.replace('-', '_') }}_{{ subcommand.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ cli_api.marketplace.name }}", "{{ subcommand.name }}"])
    assert result.exit_code == 0
    assert "Executing {{ subcommand.name }} marketplace command" in result.output
    {% endfor %}
{% endif %}

{% if cli_api.integrations %}
{% if cli_api.integrations.hygen %}
def test_integration_hygen():
    result = runner.invoke(app, ["hygen"])
    assert result.exit_code == 0
    # Add assertions as needed
{% endif %}

{% if cli_api.integrations.llm_code_assistants %}
def test_integration_llm():
    result = runner.invoke(app, ["assist"])
    assert result.exit_code == 0
    # Add assertions as needed
{% endif %}
{% endif %}
