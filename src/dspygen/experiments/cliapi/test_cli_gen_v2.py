# test_cli_generation.py

import pytest
from dspygen.experiments.cliapi.cliapi_models import *
import ast
from typer.testing import CliRunner
import tempfile
import os
import importlib.util


# Helper function to map DSL types to Python types
def get_python_type(option_type: str) -> str:
    type_mapping = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "float": "float",
        "any": "Any",
    }
    return type_mapping.get(option_type.lower(), "str")


# Code generation functions
def generate_option(option: CLIOption) -> str:
    option_name = option.name.lstrip('-').replace('-', '_')
    option_type = get_python_type(option.type)
    default_value = "..." if option.required else f"'{option.default}'" if option.default is not None else "None"
    return f"{option_name}: {option_type} = typer.Option({default_value}, '--{option.name}', help='{option.description}')"


def generate_argument(argument: CLIArgument) -> str:
    arg_name = argument.name.replace('-', '_')
    default_value = "..." if argument.required else "None"
    return f"{arg_name}: str = typer.Argument({default_value}, help='{argument.description}')"


def generate_subcommand(subcommand: CLISubcommand, app_name: str) -> str:
    code = ''
    function_name = subcommand.name.replace('-', '_')

    if subcommand.subcommands:
        # Create a new Typer app for this subcommand
        sub_app_name = f"{function_name}_app"
        code += f"{sub_app_name} = typer.Typer(help='{subcommand.description}')\n\n"

        # Generate nested subcommands
        for nested_subcommand in subcommand.subcommands:
            code += generate_subcommand(nested_subcommand, sub_app_name)
            code += "\n"

        # Add the sub_app to the parent app
        code += f"{app_name}.add_typer({sub_app_name}, name='{subcommand.name}')\n"
    else:
        params = []

        # Add arguments
        if subcommand.arguments:
            for arg in subcommand.arguments:
                params.append(generate_argument(arg))

        # Add options
        if subcommand.options:
            for opt in subcommand.options:
                params.append(generate_option(opt))

        params_str = ", ".join(params)
        code += f"@{app_name}.command()\n"
        code += f"def {function_name}({params_str}):\n"
        code += f"    '''{subcommand.description}'''\n"
        code += f"    typer.echo('Executing {subcommand.name} subcommand')\n"
    return code


def generate_command(command: CLICommand, parent_app_name: str) -> str:
    command_app_name = f"{command.name.replace('-', '_')}_app"
    code = f"{command_app_name} = typer.Typer(help='{command.description}')\n\n"

    # Generate subcommands
    for subcommand in command.subcommands:
        code += generate_subcommand(subcommand, command_app_name)
        code += "\n"

    code += f"{parent_app_name}.add_typer({command_app_name}, name='{command.name}')\n"
    return code


def generate_plugin(plugin: CLIPlugin, parent_app_name: str) -> str:
    plugin_app_name = f"{plugin.name.replace('-', '_').replace('/', '_')}_app"
    code = f"{plugin_app_name} = typer.Typer(help='{plugin.description}')\n\n"

    # Generate plugin commands
    for command in plugin.commands:
        code += generate_plugin_command(command, plugin_app_name)
        code += "\n"

    # Add the plugin app to the parent app
    code += f"{parent_app_name}.add_typer({plugin_app_name}, name='{plugin.name.split('/')[-1]}')\n"
    return code


def generate_plugin_command(command: CLIPluginCommand, app_name: str) -> str:
    code = ''
    # Generate subcommands for the plugin command
    for subcommand in command.subcommands:
        code += generate_subcommand(subcommand, app_name)
        code += "\n"
    return code


def generate_extension(extension: CLIExtension, parent_app_name: str) -> str:
    extension_app_name = f"{extension.name.replace('-', '_')}_app"
    code = f"{extension_app_name} = typer.Typer(help='{extension.description}')\n\n"

    # Generate extensions commands
    for command in extension.commands:
        code += generate_extension_command(command, extension_app_name)
        code += "\n"

    # Add the extensions app to the parent app
    code += f"{parent_app_name}.add_typer({extension_app_name}, name='{extension.name}')\n"
    return code


def generate_extension_command(command: CLIExtensionCommand, app_name: str) -> str:
    code = ''
    # Generate subcommands for the extensions command
    for subcommand in command.subcommands:
        code += generate_subcommand(subcommand, app_name)
        code += "\n"
    return code


def generate_marketplace(marketplace: CLIMarketplace, parent_app_name: str) -> str:
    marketplace_app_name = f"{marketplace.name.replace(' ', '_').replace('-', '_').lower()}_app"
    code = f"{marketplace_app_name} = typer.Typer(help='{marketplace.description}')\n\n"

    # Generate marketplace subcommands
    for subcommand in marketplace.subcommands:
        code += generate_marketplace_subcommand(subcommand, marketplace_app_name)
        code += "\n"

    # Add the marketplace app to the parent app
    code += f"{parent_app_name}.add_typer({marketplace_app_name}, name='marketplace')\n"
    return code


def generate_marketplace_subcommand(subcommand: CLIMarketplaceCommand, app_name: str) -> str:
    function_name = subcommand.name.replace('-', '_')
    params = []

    # Add arguments
    if subcommand.arguments:
        for arg in subcommand.arguments:
            params.append(generate_argument(arg))

    # Add options
    if subcommand.options:
        for opt in subcommand.options:
            params.append(generate_option(opt))

    params_str = ", ".join(params)
    code = f"@{app_name}.command()\n"
    code += f"def {function_name}({params_str}):\n"
    code += f"    '''{subcommand.description}'''\n"
    code += f"    typer.echo('Executing {subcommand.name} command')\n"
    return code


def generate_configurations(configurations: CLIConfiguration) -> str:
    code = "# Configuration Settings\n"
    code += "configurations = {\n"
    for scope, settings in configurations.dict().items():
        if settings:
            code += f"    '{scope}': {{\n"
            for key, value in settings.items():
                code += f"        '{key}': {value},\n"
            code += "    },\n"
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


def generate_integration(integration: CLIIntegration, parent_app_name: str) -> str:
    code = ''
    if integration.hygen:
        code += generate_integration_commands('hygen', integration.hygen, parent_app_name)
        code += "\n"
    if integration.llm_code_assistants:
        code += generate_integration_commands('assist', integration.llm_code_assistants, parent_app_name)
        code += "\n"
    return code


def generate_integration_commands(name: str, integration_data: Dict[str, Any], parent_app_name: str) -> str:
    app_name = f"{name.replace('-', '_')}_app"
    code = f"{app_name} = typer.Typer(help='{integration_data.get('description', '')}')\n\n"

    for command in integration_data.get('commands', []):
        function_name = command['name'].replace('-', '_')
        params = []

        # Add arguments
        for arg in command.get('arguments', []):
            arg_obj = CLIArgument(**arg)
            params.append(generate_argument(arg_obj))

        # Add options
        for opt in command.get('options', []):
            opt_obj = CLIOption(**opt)
            params.append(generate_option(opt_obj))

        params_str = ", ".join(params)
        code += f"@{app_name}.command()\n"
        code += f"def {function_name}({params_str}):\n"
        code += f"    '''{command.get('description', '')}'''\n"
        code += f"    typer.echo('Executing {function_name} command')\n\n"

    # Add the integration app to the parent app
    code += f"{parent_app_name}.add_typer({app_name}, name='{name}')\n"
    return code


def generate_app(cli_api: CLIAPI) -> str:
    code = "import typer\n"
    code += "app = typer.Typer()\n\n"

    # Include configurations
    if cli_api.configurations:
        code += generate_configurations(cli_api.configurations)

    # Include voice settings
    if cli_api.voice_settings:
        code += generate_voice_settings(cli_api.voice_settings)

    # Include accessibility features
    if cli_api.accessibility_features:
        code += generate_accessibility_features(cli_api.accessibility_features)

    # Generate commands
    for command in cli_api.commands:
        code += generate_command(command, "app")
        code += "\n"

    # Generate plugins
    for plugin in cli_api.plugins:
        code += generate_plugin(plugin, "app")
        code += "\n"

    # Generate extensions
    for extension in cli_api.extensions:
        code += generate_extension(extension, "app")
        code += "\n"

    # Generate marketplace
    if cli_api.marketplace:
        code += generate_marketplace(cli_api.marketplace, "app")
        code += "\n"

    # Generate integrations
    if cli_api.integrations:
        code += generate_integration(cli_api.integrations, "app")
        code += "\n"

    code += "if __name__ == '__main__':\n"
    code += "    app()\n"
    return code


# AST utilities
def extract_functions(ast_node):
    functions = {}

    class FunctionVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            func_name = node.name
            args = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node)
            functions[func_name] = {
                'args': args,
                'docstring': docstring,
            }
            self.generic_visit(node)

    visitor = FunctionVisitor()
    visitor.visit(ast_node)
    return functions


def compare_ast_with_cliapi(ast_functions, cli_api):
    errors = []

    # Commands
    for command in cli_api.commands:
        errors.extend(compare_command_with_ast(command, ast_functions))

    # Plugins
    for plugin in cli_api.plugins:
        for command in plugin.commands:
            for subcommand in command.subcommands:
                errors.extend(compare_subcommand_with_ast(subcommand, ast_functions))

    # Extensions
    for extension in cli_api.extensions:
        for command in extension.commands:
            for subcommand in command.subcommands:
                errors.extend(compare_subcommand_with_ast(subcommand, ast_functions))

    # Marketplace Commands
    if cli_api.marketplace:
        for subcommand in cli_api.marketplace.subcommands:
            errors.extend(compare_marketplace_subcommand_with_ast(subcommand, ast_functions))

    # Integrations
    if cli_api.integrations:
        if cli_api.integrations.hygen:
            errors.extend(compare_integration_with_ast('hygen', cli_api.integrations.hygen, ast_functions))
        if cli_api.integrations.llm_code_assistants:
            errors.extend(
                compare_integration_with_ast('assist', cli_api.integrations.llm_code_assistants, ast_functions))

    return errors


def compare_command_with_ast(command: CLICommand, ast_functions):
    errors = []
    # Subcommands
    for subcommand in command.subcommands:
        errors.extend(compare_subcommand_with_ast(subcommand, ast_functions))
    return errors


def compare_subcommand_with_ast(subcommand: CLISubcommand, ast_functions):
    errors = []
    function_name = subcommand.name.replace('-', '_')
    if function_name not in ast_functions and not subcommand.subcommands:
        errors.append(f"Function '{function_name}' not found in generated code.")
        return errors
    if subcommand.subcommands:
        # If the subcommand has further subcommands, recursively check them
        for nested_subcommand in subcommand.subcommands:
            errors.extend(compare_subcommand_with_ast(nested_subcommand, ast_functions))
    else:
        # Compare arguments and options
        expected_params = []
        if subcommand.arguments:
            for arg in subcommand.arguments:
                expected_params.append(arg.name.replace('-', '_'))
        if subcommand.options:
            for opt in subcommand.options:
                expected_params.append(opt.name.lstrip('-').replace('-', '_'))
        actual_params = ast_functions[function_name]['args']
        if set(expected_params) != set(actual_params):
            errors.append(f"Parameters for function '{function_name}' do not match.")
            errors.append(f"Expected: {sorted(expected_params)}")
            errors.append(f"Actual: {sorted(actual_params)}")
        # Compare docstring
        expected_doc = subcommand.description
        actual_doc = ast_functions[function_name]['docstring']
        if expected_doc != actual_doc:
            errors.append(f"Docstring for function '{function_name}' does not match.")
            errors.append(f"Expected: '{expected_doc}'")
            errors.append(f"Actual: '{actual_doc}'")
    return errors


def compare_marketplace_subcommand_with_ast(subcommand: CLIMarketplaceCommand, ast_functions):
    errors = []
    function_name = subcommand.name.replace('-', '_')
    if function_name not in ast_functions:
        errors.append(f"Function '{function_name}' not found in generated code.")
        return errors
    # Compare arguments and options
    expected_params = []
    if subcommand.arguments:
        for arg in subcommand.arguments:
            expected_params.append(arg.name.replace('-', '_'))
    if subcommand.options:
        for opt in subcommand.options:
            expected_params.append(opt.name.lstrip('-').replace('-', '_'))
    actual_params = ast_functions[function_name]['args']
    if set(expected_params) != set(actual_params):
        errors.append(f"Parameters for function '{function_name}' do not match.")
        errors.append(f"Expected: {sorted(expected_params)}")
        errors.append(f"Actual: {sorted(actual_params)}")
    # Compare docstring
    expected_doc = subcommand.description
    actual_doc = ast_functions[function_name]['docstring']
    if expected_doc != actual_doc:
        errors.append(f"Docstring for function '{function_name}' does not match.")
        errors.append(f"Expected: '{expected_doc}'")
        errors.append(f"Actual: '{actual_doc}'")
    return errors


def compare_integration_with_ast(name: str, integration_data: Dict[str, Any], ast_functions):
    errors = []
    for command in integration_data.get('commands', []):
        function_name = command['name'].replace('-', '_')
        if function_name not in ast_functions:
            errors.append(f"Function '{function_name}' not found in generated code.")
            continue
        expected_params = []
        for arg in command.get('arguments', []):
            expected_params.append(arg['name'].replace('-', '_'))
        for opt in command.get('options', []):
            expected_params.append(opt['name'].lstrip('-').replace('-', '_'))
        actual_params = ast_functions[function_name]['args']
        if set(expected_params) != set(actual_params):
            errors.append(f"Parameters for function '{function_name}' do not match.")
            errors.append(f"Expected: {sorted(expected_params)}")
            errors.append(f"Actual: {sorted(actual_params)}")
        # Compare docstring
        expected_doc = command.get('description', '')
        actual_doc = ast_functions[function_name]['docstring']
        if expected_doc != actual_doc:
            errors.append(f"Docstring for function '{function_name}' do not match.")
            errors.append(f"Expected: '{expected_doc}'")
            errors.append(f"Actual: '{actual_doc}'")
    return errors


# Test functions
def test_cli_code_generation():
    # Load the CLIAPI object
    cli_api = CLIAPI.from_yaml("github_cli.yaml")

    # Generate the code
    cli_code = generate_app(cli_api)

    # Parse the generated code into an AST
    generated_ast = ast.parse(cli_code)

    # Extract functions from the AST
    ast_functions = extract_functions(generated_ast)

    # Compare the AST with the CLIAPI object
    errors = compare_ast_with_cliapi(ast_functions, cli_api)

    # Assert that there are no errors
    assert not errors, "\n".join(errors)


def test_cli_code_execution():
    # Load the CLIAPI object
    cli_api = CLIAPI.from_yaml("github_cli.yaml")

    # Generate the code
    cli_code = generate_app(cli_api)

    # Write the code to a temporary file
    with tempfile.TemporaryDirectory() as tmpdirname:
        code_file = os.path.join(tmpdirname, 'cli_app.py')
        with open(code_file, 'w') as f:
            f.write(cli_code)
        # Import the module
        spec = importlib.util.spec_from_file_location("cli_app", code_file)
        cli_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli_app)
        # Use CliRunner to test the commands
        runner = CliRunner()
        # Test commands and subcommands
        for command in cli_api.commands:
            # Test command help
            result = runner.invoke(cli_app.app, [command.name, '--help'])
            assert result.exit_code == 0
            assert command.description in result.stdout
            # Test subcommands
            for subcommand in command.subcommands:
                result = runner.invoke(cli_app.app, [command.name, subcommand.name, '--help'])
                assert result.exit_code == 0
                assert subcommand.description in result.stdout
                # Test nested subcommands if any
                if subcommand.subcommands:
                    for nested_subcommand in subcommand.subcommands:
                        result = runner.invoke(cli_app.app,
                                               [command.name, subcommand.name, nested_subcommand.name, '--help'])
                        assert result.exit_code == 0
                        assert nested_subcommand.description in result.stdout

        # Test plugins
        for plugin in cli_api.plugins:
            plugin_name = plugin.name.split('/')[-1]
            result = runner.invoke(cli_app.app, [plugin_name, '--help'])
            assert result.exit_code == 0
            assert plugin.description in result.stdout
            for command in plugin.commands:
                for subcommand in command.subcommands:
                    result = runner.invoke(cli_app.app, [plugin_name, subcommand.name, '--help'])
                    assert result.exit_code == 0
                    assert subcommand.description in result.stdout

        # Test extensions
        for extension in cli_api.extensions:
            extension_name = extension.name
            result = runner.invoke(cli_app.app, [extension_name, '--help'])
            assert result.exit_code == 0
            assert extension.description in result.stdout
            for command in extension.commands:
                for subcommand in command.subcommands:
                    result = runner.invoke(cli_app.app, [extension_name, subcommand.name, '--help'])
                    assert result.exit_code == 0
                    assert subcommand.description in result.stdout

        # Test marketplace
        if cli_api.marketplace:
            result = runner.invoke(cli_app.app, ['marketplace', '--help'])
            assert result.exit_code == 0
            assert cli_api.marketplace.description in result.stdout
            for subcommand in cli_api.marketplace.subcommands:
                result = runner.invoke(cli_app.app, ['marketplace', subcommand.name, '--help'])
                assert result.exit_code == 0
                assert subcommand.description in result.stdout

        # Test integrations
        if cli_api.integrations:
            if cli_api.integrations.hygen:
                result = runner.invoke(cli_app.app, ['hygen', '--help'])
                assert result.exit_code == 0
                assert cli_api.integrations.hygen.get('description', '') in result.stdout
                for command in cli_api.integrations.hygen.get('commands', []):
                    result = runner.invoke(cli_app.app, ['hygen', command['name'], '--help'])
                    assert result.exit_code == 0
                    assert command.get('description', '') in result.stdout
            if cli_api.integrations.llm_code_assistants:
                result = runner.invoke(cli_app.app, ['assist', '--help'])
                assert result.exit_code == 0
                assert cli_api.integrations.llm_code_assistants.get('description', '') in result.stdout
                for command in cli_api.integrations.llm_code_assistants.get('commands', []):
                    result = runner.invoke(cli_app.app, ['assist', command['name'], '--help'])
                    assert result.exit_code == 0
                    assert command.get('description', '') in result.stdout
