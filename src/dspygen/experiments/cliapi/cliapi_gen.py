from typing import List, Dict, Any
import typer

from dspygen.experiments.cliapi.cliapi_models import *

cli_template = """{{ generate_main_app(cli_api) }}

{% if cli_api.configurations %}
{{ generate_configurations(cli_api.configurations) }}
{% endif %}

{% if cli_api.voice_settings %}
{{ generate_voice_settings(cli_api.voice_settings) }}
{% endif %}

{% if cli_api.accessibility_features %}
{{ generate_accessibility_features(cli_api.accessibility_features) }}
{% endif %}

{% for command in cli_api.commands %}
{{ generate_command(command, 'app') }}
{% endfor %}

{% for plugin in cli_api.plugins %}
{{ generate_plugin(plugin, 'app') }}
{% endfor %}

{% for extensions in cli_api.extensions %}
{{ generate_extension(extensions, 'app') }}
{% endfor %}

{% if cli_api.marketplace %}
{{ generate_marketplace(cli_api.marketplace, 'app') }}
{% endif %}

{% if cli_api.integrations %}
{{ generate_integration(cli_api.integrations, 'app') }}
{% endif %}

if __name__ == "__main__":
    app()

"""

pytest_template = """{% raw %}
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

{% for extensions in cli_api.extensions %}
def test_extension_{{ extensions.name.replace('-', '_') }}():
    result = runner.invoke(app, ["{{ extensions.name }}"])
    assert result.exit_code == 0
    # Add assertions as needed

    {% for command in extensions.commands %}
def test_extension_{{ extensions.name.replace('-', '_') }}_{{ command.name.replace('-', '_') }}():
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
{% endraw %}
"""
def generate_metadata(metadata: CLIMetadata) -> str:
    return f"""
__app_name__ = '{metadata.name}'
__version__ = '{metadata.version}'
__description__ = '''{metadata.description}'''
__author__ = '{metadata.author}'

"""


def generate_option(option: CLIOption) -> str:
    option_name = option.name.lstrip('-').replace('-', '_')
    option_type = get_python_type(option.type)
    default = f" = {option.default}" if option.default is not None else ""
    required = option.required
    if option.type.lower() == 'boolean':
        default_value = "False" if not required else "..."
        return f"{option_name}: bool = typer.Option({default_value}, help='{option.description}')"
    else:
        default_value = "..." if required else "None"
        return f"{option_name}: {option_type} = typer.Option({default_value}, help='{option.description}')"

def generate_argument(argument: CLIArgument) -> str:
    arg_name = argument.name.replace('-', '_')
    default_value = "..." if argument.required else "None"
    return f"{arg_name}: str = typer.Argument({default_value}, help='{argument.description}')"

def get_python_type(option_type: str) -> str:
    type_mapping = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "float": "float",
        "any": "Any",
    }
    return type_mapping.get(option_type.lower(), "str")


def generate_subcommand(subcommand: CLISubcommand, parent_app: str) -> str:
    sub_app_name = f"{subcommand.name.replace('-', '_')}_app"
    code = ""

    if subcommand.subcommands:
        # Nested subcommands
        code += f"{sub_app_name} = typer.Typer(help='{subcommand.description}')\n\n"
        for nested_subcommand in subcommand.subcommands:
            code += generate_subcommand(nested_subcommand, sub_app_name)
        code += f"{parent_app}.add_typer({sub_app_name}, name='{subcommand.name}')\n\n"
    else:
        # Leaf subcommand
        function_name = subcommand.name.replace('-', '_')
        code += f"@{parent_app}.command(name='{subcommand.name}', help='{subcommand.description}')\n"
        code += f"def {function_name}("
        params = []
        # Add arguments
        for arg in subcommand.arguments:
            params.append(generate_argument(arg))
        # Add options
        for opt in subcommand.options:
            params.append(generate_option(opt))
        code += ", ".join(params)
        code += "):\n"
        code += f"    '''{subcommand.description}'''\n"
        code += f"    typer.echo('Executing {subcommand.name} subcommand')\n"
        if subcommand.examples:
            code += "    # Examples:\n"
            for example in subcommand.examples:
                code += f"    # {example}\n"
        code += "\n"
    return code

def generate_command(command: CLICommand, parent_app: str) -> str:
    command_app_name = f"{command.name.replace('-', '_')}_app"
    code = f"{command_app_name} = typer.Typer(help='{command.description}')\n\n"

    if command.global_options:
        # Handle global options for the command
        code += f"@{command_app_name}.callback()\n"
        code += f"def {command.name.replace('-', '_')}_callback("
        params = [generate_option(opt) for opt in command.global_options]
        code += ", ".join(params)
        code += "):\n"
        code += "    pass\n\n"

    for subcommand in command.subcommands:
        code += generate_subcommand(subcommand, command_app_name)

    code += f"{parent_app}.add_typer({command_app_name}, name='{command.name}')\n\n"
    return code


def generate_plugin(plugin: CLIPlugin, parent_app: str) -> str:
    plugin_app_name = f"{plugin.name.replace('-', '_')}_app"
    code = f"{plugin_app_name} = typer.Typer(help='{plugin.description}')\n\n"
    for command in plugin.commands:
        code += generate_plugin_command(command, plugin_app_name)
    code += f"{parent_app}.add_typer({plugin_app_name}, name='{plugin.name}')\n\n"
    return code

def generate_plugin_command(command: CLIPluginCommand, parent_app: str) -> str:
    return generate_subcommand(CLISubcommand(
        name=command.name,
        description=command.description,
        options=[],
        arguments=[],
        examples=[],
        subcommands=command.subcommands
    ), parent_app)

def generate_extension(extension: CLIExtension, parent_app: str) -> str:
    extension_app_name = f"{extension.name.replace('-', '_')}_app"
    code = f"{extension_app_name} = typer.Typer(help='{extension.description}')\n\n"
    for command in extension.commands:
        code += generate_extension_command(command, extension_app_name)
    code += f"{parent_app}.add_typer({extension_app_name}, name='{extension.name}')\n\n"
    return code

def generate_extension_command(command: CLIExtensionCommand, parent_app: str) -> str:
    return generate_subcommand(CLISubcommand(
        name=command.name,
        description=command.description,
        options=[],
        arguments=[],
        examples=[],
        subcommands=command.subcommands
    ), parent_app)


def generate_marketplace(marketplace: CLIMarketplace, parent_app: str) -> str:
    marketplace_app_name = f"{marketplace.name.replace('-', '_')}_app"
    code = f"{marketplace_app_name} = typer.Typer(help='{marketplace.description}')\n\n"
    for command in marketplace.subcommands:
        code += generate_marketplace_command(command, marketplace_app_name)
    code += f"{parent_app}.add_typer({marketplace_app_name}, name='{marketplace.name}')\n\n"
    return code

def generate_marketplace_command(command: CLIMarketplaceCommand, parent_app: str) -> str:
    function_name = command.name.replace('-', '_')
    code = f"@{parent_app}.command(name='{command.name}', help='{command.description}')\n"
    code += f"def {function_name}("
    params = []
    # Add arguments
    for arg in command.arguments:
        params.append(generate_argument(arg))
    # Add options
    for opt in command.options:
        params.append(generate_option(opt))
    code += ", ".join(params)
    code += "):\n"
    code += f"    '''{command.description}'''\n"
    code += f"    typer.echo('Executing {command.name} marketplace command')\n"
    if command.examples:
        code += "    # Examples:\n"
        for example in command.examples:
            code += f"    # {example}\n"
    code += "\n"
    return code


def generate_configurations(config: CLIConfiguration) -> str:
    code = "# Configurations\n"
    code += "configurations = {\n"
    code += "    'globals': {\n"
    for key, value in config.globals.items():
        code += f"        '{key}': {value},\n"
    code += "    },\n"
    code += "    'repository': {\n"
    for key, value in config.repository.items():
        code += f"        '{key}': {value},\n"
    code += "    }\n"
    code += "}\n\n"
    return code

def generate_voice_settings(voice_settings: CLIVoiceSettings) -> str:
    code = "# Voice Settings\n"
    code += f"voice_settings = {voice_settings.dict()}\n\n"
    return code

def generate_accessibility_features(features: CLIAccessibilityFeatures) -> str:
    code = "# Accessibility Features\n"
    code += f"accessibility_features = {features.dict()}\n\n"
    return code


def generate_integration(integration: CLIIntegration, parent_app: str) -> str:
    code = ""
    if integration.hygen:
        code += generate_hygen_integration(integration.hygen, parent_app)
    if integration.llm_code_assistants:
        code += generate_llm_integration(integration.llm_code_assistants, parent_app)
    return code

def generate_hygen_integration(hygen_config: Dict[str, Any], parent_app: str) -> str:
    hygen_app_name = "hygen_app"
    code = f"{hygen_app_name} = typer.Typer(help='{hygen_config.get('description', '')}')\n\n"
    for command in hygen_config.get('commands', []):
        code += generate_generic_command(command, hygen_app_name)
    code += f"{parent_app}.add_typer({hygen_app_name}, name='hygen')\n\n"
    return code

def generate_llm_integration(llm_config: Dict[str, Any], parent_app: str) -> str:
    llm_app_name = "assist_app"
    code = f"{llm_app_name} = typer.Typer(help='{llm_config.get('description', '')}')\n\n"
    for command in llm_config.get('commands', []):
        code += generate_generic_command(command, llm_app_name)
    code += f"{parent_app}.add_typer({llm_app_name}, name='assist')\n\n"
    return code

def generate_generic_command(command: Dict[str, Any], parent_app: str) -> str:
    function_name = command['name'].replace('-', '_')
    code = f"@{parent_app}.command(name='{command['name']}', help='{command['description']}')\n"
    code += f"def {function_name}("
    params = []
    # Options
    for opt in command.get('options', []):
        opt_obj = CLIOption(
            name=opt['name'],
            description=opt['description'],
            type=opt['type'],
            default=opt.get('default', None),
            required=opt.get('required', False)
        )
        params.append(generate_option(opt_obj))
    # Arguments
    for arg in command.get('arguments', []):
        arg_obj = CLIArgument(
            name=arg['name'],
            description=arg['description'],
            required=arg.get('required', False)
        )
        params.append(generate_argument(arg_obj))
    code += ", ".join(params)
    code += "):\n"
    code += f"    '''{command['description']}'''\n"
    code += f"    typer.echo('Executing {command['name']} command')\n"
    if 'examples' in command:
        code += "    # Examples:\n"
        for example in command['examples']:
            code += f"    # {example}\n"
    code += "\n"
    return code

def generate_main_app(cli_api: CLIAPI) -> str:
    code = ""
    code += generate_metadata(cli_api.metadata)
    code += "import typer\n\n"
    code += "app = typer.Typer(help=__description__)\n\n"
    return code



from jinja2 import Environment

def main():
    """Main function"""
    # Create a Jinja2 environments and add helper functions
    env = Environment()
    env.globals.update({
        'generate_main_app': generate_main_app,
        'generate_metadata': generate_metadata,
        'generate_command': generate_command,
        'generate_subcommand': generate_subcommand,
        'generate_option': generate_option,
        'generate_argument': generate_argument,
        'get_python_type': get_python_type,
        'generate_plugin': generate_plugin,
        'generate_plugin_command': generate_plugin_command,
        'generate_extension': generate_extension,
        'generate_extension_command': generate_extension_command,
        'generate_marketplace': generate_marketplace,
        'generate_marketplace_command': generate_marketplace_command,
        'generate_configurations': generate_configurations,
        'generate_voice_settings': generate_voice_settings,
        'generate_accessibility_features': generate_accessibility_features,
        'generate_integration': generate_integration,
        'generate_generic_command': generate_generic_command,
    })

    cli_api = CLIAPI.from_yaml("github_cli.yaml")

    # Render the templates
    cli_template_code = env.from_string(cli_template).render(cli_api=cli_api)
    pytest_template_code = env.from_string(pytest_template).render(cli_api=cli_api)

    # Write the CLI code to a file
    with open("cli_app.py", "w") as f:
        f.write(cli_template_code)

    # Write the test code to a file
    with open("test_cli_app.py", "w") as f:
        f.write(pytest_template_code)

    print("CLI and test files generated successfully.")

if __name__ == '__main__':
    main()
