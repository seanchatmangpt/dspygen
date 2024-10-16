from dspygen.experiments.cliapi.cliapi_models import *


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_lm
    init_lm()

    # Define CLI Metadata
    rovo_cli_metadata = CLIMetadata(
        name="Atlassian Rovo CLI",
        version="1.0.0",
        description="A command-line tool for interacting with Atlassian Rovo, powered by Generative AI.",
        author="Atlassian, Inc."
    )

    # Define Global Options
    global_options = [
        CLIOption(
            name="--version",
            description="Display the version of Rovo CLI.",
            type="boolean",
            required=False
        ),
        CLIOption(
            name="--help",
            description="Show help information for Rovo CLI.",
            type="boolean",
            required=False
        )
    ]

    # Define Commands
    rovo_commands = [
        CLICommand(
            name="find",
            description="Search across all connected SaaS applications.",
            global_options=[],
            subcommands=[
                CLISubcommand(
                    name="search",
                    description="Search for specific information across integrated apps.",
                    options=[
                        CLIOption(
                            name="--query",
                            description="The search query string.",
                            type="string",
                            required=True
                        ),
                        CLIOption(
                            name="--app",
                            description="Specify the app to search within.",
                            type="string",
                            required=False,
                            aliases=["-a"]
                        )
                    ],
                    arguments=[],
                    examples=[
                        "rovo find search --query 'Project Plan' --app 'Confluence'",
                        "rovo find search --query 'Bug Reports'"
                    ]
                )
            ]
        ),
        CLICommand(
            name="learn",
            description="Interact with Rovo Chat to gain insights and understand organizational topics.",
            global_options=[],
            subcommands=[
                CLISubcommand(
                    name="chat",
                    description="Start an intelligent conversation with Rovo Chat.",
                    options=[
                        CLIOption(
                            name="--topic",
                            description="Topic to discuss with Rovo Chat.",
                            type="string",
                            required=True
                        )
                    ],
                    arguments=[],
                    examples=[
                        "rovo learn chat --topic 'Team Performance Metrics'",
                        "rovo learn chat --topic 'Product Roadmap'"
                    ]
                )
            ]
        ),
        CLICommand(
            name="act",
            description="Utilize Rovo Agents to perform automated tasks and streamline workflows.",
            global_options=[],
            subcommands=[
                CLISubcommand(
                    name="agents",
                    description="Manage Rovo Agents for various tasks.",
                    options=[],
                    arguments=[],
                    subcommands=[
                        CLISubcommand(
                            name="create",
                            description="Create a new Rovo Agent.",
                            options=[
                                CLIOption(
                                    name="--name",
                                    description="Name of the new agent.",
                                    type="string",
                                    required=True
                                ),
                                CLIOption(
                                    name="--type",
                                    description="Type of agent to create (e.g., 'workflow', 'knowledge').",
                                    type="string",
                                    required=True
                                )
                            ],
                            arguments=[],
                            examples=[
                                "rovo act agents create --name 'DeploymentAgent' --type 'workflow'",
                                "rovo act agents create --name 'KnowledgeBot' --type 'knowledge'"
                            ]
                        ),
                        CLISubcommand(
                            name="list",
                            description="List all existing Rovo Agents.",
                            options=[],
                            arguments=[],
                            examples=[
                                "rovo act agents list"
                            ]
                        ),
                        CLISubcommand(
                            name="delete",
                            description="Delete an existing Rovo Agent.",
                            options=[
                                CLIOption(
                                    name="--id",
                                    description="ID of the agent to delete.",
                                    type="string",
                                    required=True
                                )
                            ],
                            arguments=[],
                            examples=[
                                "rovo act agents delete --id 'agent_12345'"
                            ]
                        )
                    ],
                    examples=[
                        "rovo act agents create --name 'DeploymentAgent' --type 'workflow'",
                        "rovo act agents list",
                        "rovo act agents delete --id 'agent_12345'"
                    ]
                )
            ]
        ),
        CLICommand(
            name="integrations",
            description="Manage integrations with other SaaS applications.",
            global_options=[],
            subcommands=[
                CLISubcommand(
                    name="add",
                    description="Add a new integration.",
                    options=[
                        CLIOption(
                            name="--app",
                            description="Name of the application to integrate (e.g., 'Slack', 'GitHub').",
                            type="string",
                            required=True
                        ),
                        CLIOption(
                            name="--config",
                            description="Path to the configuration file for the integration.",
                            type="string",
                            required=False
                        )
                    ],
                    arguments=[],
                    examples=[
                        "rovo integrations add --app 'Slack' --config './configs/slack.yaml'",
                        "rovo integrations add --app 'GitHub'"
                    ]
                ),
                CLISubcommand(
                    name="remove",
                    description="Remove an existing integration.",
                    options=[
                        CLIOption(
                            name="--app",
                            description="Name of the application to remove integration for.",
                            type="string",
                            required=True
                        )
                    ],
                    arguments=[],
                    examples=[
                        "rovo integrations remove --app 'Slack'",
                        "rovo integrations remove --app 'GitHub'"
                    ]
                ),
                CLISubcommand(
                    name="list",
                    description="List all current integrations.",
                    options=[],
                    arguments=[],
                    examples=[
                        "rovo integrations list"
                    ]
                )
            ],
            examples=[
                "rovo integrations add --app 'Slack' --config './configs/slack.yaml'",
                "rovo integrations list",
                "rovo integrations remove --app 'GitHub'"
            ]
        )
    ]

    # Define Plugins (if any)
    rovo_plugins = [
        CLIPlugin(
            name="RovoAnalytics",
            description="Enhance Rovo CLI with advanced analytics capabilities.",
            commands=[
                CLIPluginCommand(
                    name="analytics",
                    description="Perform analytics tasks.",
                    subcommands=[
                        CLISubcommand(
                            name="generate-report",
                            description="Generate an analytics report.",
                            options=[
                                CLIOption(
                                    name="--type",
                                    description="Type of report to generate (e.g., 'monthly', 'quarterly').",
                                    type="string",
                                    required=True
                                )
                            ],
                            arguments=[],
                            examples=[
                                "rovo analytics generate-report --type 'monthly'",
                                "rovo analytics generate-report --type 'quarterly'"
                            ]
                        )
                    ],
                    examples=[
                        "rovo analytics generate-report --type 'monthly'"
                    ]
                )
            ]
        )
    ]

    # Define Extensions (if any)
    rovo_extensions = [
        CLIExtension(
            name="RovoCustom",
            description="Custom extensions for Rovo CLI tailored to specific workflows.",
            commands=[
                CLIExtensionCommand(
                    name="custom",
                    description="Manage custom extensions.",
                    subcommands=[
                        CLISubcommand(
                            name="install",
                            description="Install a custom extensions.",
                            options=[
                                CLIOption(
                                    name="--name",
                                    description="Name of the custom extensions to install.",
                                    type="string",
                                    required=True
                                )
                            ],
                            arguments=[],
                            examples=[
                                "rovo custom install --name 'TeamCultureAgent'"
                            ]
                        ),
                        CLISubcommand(
                            name="uninstall",
                            description="Uninstall a custom extensions.",
                            options=[
                                CLIOption(
                                    name="--name",
                                    description="Name of the custom extensions to uninstall.",
                                    type="string",
                                    required=True
                                )
                            ],
                            arguments=[],
                            examples=[
                                "rovo custom uninstall --name 'TeamCultureAgent'"
                            ]
                        )
                    ],
                    examples=[
                        "rovo custom install --name 'TeamCultureAgent'",
                        "rovo custom uninstall --name 'TeamCultureAgent'"
                    ]
                )
            ],
            examples=[
                "rovo custom install --name 'TeamCultureAgent'"
            ]
        )
    ]

    # Define Marketplace (if applicable)
    rovo_marketplace = CLIMarketplace(
        name="Rovo Marketplace",
        description="A marketplace for Rovo CLI plugins and extensions.",
        subcommands=[
            CLIMarketplaceCommand(
                name="browse",
                description="Browse available plugins and extensions in the Rovo Marketplace.",
                options=[
                    CLIOption(
                        name="--category",
                        description="Filter by category.",
                        type="string",
                        required=False
                    ),
                    CLIOption(
                        name="--sort",
                        description="Sort results by criteria (e.g., popularity, date).",
                        type="string",
                        required=False
                    )
                ],
                arguments=[
                    CLIArgument(
                        name="query",
                        description="Search query term.",
                        required=False
                    )
                ],
                examples=[
                    "rovo marketplace browse --category 'Productivity'",
                    "rovo marketplace browse --sort 'popularity'"
                ]
            ),
            CLIMarketplaceCommand(
                name="install",
                description="Install a plugin or extensions from the Rovo Marketplace.",
                options=[
                    CLIOption(
                        name="--source",
                        description="Source repository of the plugin or extensions.",
                        type="string",
                        required=True
                    )
                ],
                arguments=[
                    CLIArgument(
                        name="item-name",
                        description="Name of the plugin or extensions to install.",
                        required=True
                    )
                ],
                examples=[
                    "rovo marketplace install rovo-extensions/analytics-agent"
                ]
            )
        ]
    )

    # Define Configurations
    rovo_configurations = CLIConfiguration(
        globals={
            "editor": {
                "description": "Default text editor for Rovo CLI operations.",
                "type": "string",
                "default": "vim"
            },
            "theme": {
                "description": "Color theme for Rovo CLI output.",
                "type": "string",
                "default": "auto"
            }
        },
        repository={
            "default_integration": {
                "description": "Default SaaS app integration for new projects.",
                "type": "string",
                "default": "Slack"
            },
            "auto_sync": {
                "description": "Enable or disable automatic synchronization of data.",
                "type": "boolean",
                "default": True
            }
        }
    )

    # Define Accessibility Features
    rovo_accessibility = CLIAccessibilityFeatures(
        screen_reader_support=True,
        high_contrast_mode=True,
        keyboard_navigation=True
    )

    # Define Voice Settings
    rovo_voice_settings = CLIVoiceSettings(
        voice_format="wav",
        voice_language="en"
    )

    # Define Integrations
    rovo_integrations = CLIIntegration(
        hygen={
            "description": "Integrate Hygen for code scaffolding.",
            "commands": [
                {
                    "name": "hygen",
                    "description": "Code scaffolding using Hygen templates.",
                    "options": [
                        {
                            "name": "--template",
                            "description": "Select template for scaffolding.",
                            "type": "string",
                            "required": True
                        }
                    ],
                    "arguments": [
                        {
                            "name": "component-name",
                            "description": "Name of the component to scaffold.",
                            "required": True
                        }
                    ],
                    "examples": [
                        "rovo hygen --template react component Button",
                        "rovo hygen --template node service AuthService"
                    ]
                }
            ]
        },
        llm_code_assistants={
            "description": "Integrate LLM-powered code assistants for enhanced code generation and assistance.",
            "commands": [
                {
                    "name": "assist",
                    "description": "Interact with LLM-powered code assistants.",
                    "options": [
                        {
                            "name": "--prompt",
                            "description": "Provide a prompt for the assistant.",
                            "type": "string",
                            "required": True
                        },
                        {
                            "name": "--model",
                            "description": "Specify the LLM model to use.",
                            "type": "string",
                            "default": "gpt-4"
                        }
                    ],
                    "arguments": [
                        {
                            "name": "code-file",
                            "description": "File to apply assistant's suggestions.",
                            "required": False
                        }
                    ],
                    "examples": [
                        "rovo assist --prompt 'Optimize this function' main.py",
                        "rovo assist --prompt 'Generate unit tests' src/utils.py --model gpt-4-turbo"
                    ]
                }
            ]
        }
    )

    # Define the CLIAPI Instance for Rovo
    rovo_cli = CLIAPI(
        metadata=rovo_cli_metadata,
        commands=rovo_commands,
        plugins=rovo_plugins,
        extensions=rovo_extensions,
        marketplace=rovo_marketplace,
        configurations=rovo_configurations,
        voice_settings=rovo_voice_settings,
        integrations=rovo_integrations
    )

    # Serialize the CLIAPI to YAML (optional)
    cliapi_yaml = rovo_cli.to_yaml()
    print("**CLIAPI YAML Representation:**\n")
    print(cliapi_yaml)

    cli_session = CLISession(
        session_id="session_003",
        start_time="2024-05-01T09:00:00Z",
        end_time="2024-05-01T11:00:00Z",
        user="ExpertDev",
        environment={
            "editor": "Visual Studio Code",
            "os": "Windows 10",
            "shell": "PowerShell",
            "AI_Assistants": ["aider", "cursor"],
            "rovo_version": "1.0.0",
        },
        executions=[
            CLIExecution(
                command="rovo find search",
                options={
                    "--query": "Project Plan",
                    "--app": "Confluence"
                },
                arguments=[],
                timestamp="2024-05-01T09:05:00Z",
                output="Found 3 results in Confluence for 'Project Plan'.",
                success=True
            ),
            CLIExecution(
                command="rovo chat",
                options={
                    "--topic": "Team Performance Metrics"
                },
                arguments=[],
                timestamp="2024-05-01T09:10:00Z",
                output="Rovo Chat: Here are the latest team performance metrics...",
                success=True
            ),
            CLIExecution(
                command="rovo act agents create",
                options={
                    "--name": "DeploymentAgent",
                    "--type": "workflow"
                },
                arguments=[],
                timestamp="2024-05-01T09:15:00Z",
                output="Rovo Agent 'DeploymentAgent' of type 'workflow' created successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo act agents list",
                options={},
                arguments=[],
                timestamp="2024-05-01T09:20:00Z",
                output="""Available Rovo Agents:
        - DeploymentAgent (workflow)
        - KnowledgeBot (knowledge)
        - MaintenanceAgent (maintenance)""",
                success=True
            ),
            CLIExecution(
                command="rovo integrations add",
                options={
                    "--app": "Slack",
                    "--config": "./configs/slack.yaml"
                },
                arguments=[],
                timestamp="2024-05-01T09:25:00Z",
                output="Integration with 'Slack' added successfully using configuration './configs/slack.yaml'.",
                success=True
            ),
            CLIExecution(
                command="rovo find search",
                options={
                    "--query": "Bug Reports"
                },
                arguments=[],
                timestamp="2024-05-01T09:30:00Z",
                output="Found 5 results across all integrated applications for 'Bug Reports'.",
                success=True
            ),
            CLIExecution(
                command="rovo act agents create",
                options={
                    "--name": "KnowledgeBot",
                    "--type": "knowledge"
                },
                arguments=[],
                timestamp="2024-05-01T09:35:00Z",
                output="Rovo Agent 'KnowledgeBot' of type 'knowledge' created successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo learn chat",
                options={
                    "--topic": "Product Roadmap"
                },
                arguments=[],
                timestamp="2024-05-01T09:40:00Z",
                output="Rovo Chat: Discussing the Product Roadmap...",
                success=True
            ),
            CLIExecution(
                command="rovo act agents list",
                options={},
                arguments=[],
                timestamp="2024-05-01T09:45:00Z",
                output="""Available Rovo Agents:
        - DeploymentAgent (workflow)
        - KnowledgeBot (knowledge)
        - MaintenanceAgent (maintenance)""",
                success=True
            ),
            CLIExecution(
                command="rovo workflow start",
                options={
                    "--name": "CI Pipeline"
                },
                arguments=[],
                timestamp="2024-05-01T09:50:00Z",
                output="Workflow 'CI Pipeline' started successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo workflow status",
                options={
                    "--name": "CI Pipeline"
                },
                arguments=[],
                timestamp="2024-05-01T09:55:00Z",
                output="Workflow 'CI Pipeline' is currently running.",
                success=True
            ),
            CLIExecution(
                command="rovo agents delete",
                options={
                    "--id": "agent_67890"
                },
                arguments=[],
                timestamp="2024-05-01T10:00:00Z",
                output="Rovo Agent with ID 'agent_67890' deleted successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo integrations list",
                options={},
                arguments=[],
                timestamp="2024-05-01T10:05:00Z",
                output="""Current Integrations:
        - Slack (configured)
        - GitHub (not configured)
        - Google Drive (configured)""",
                success=True
            ),
            CLIExecution(
                command="rovo help",
                options={},
                arguments=[],
                timestamp="2024-05-01T10:10:00Z",
                output="""Atlassian Rovo CLI - Version 1.0.0

        Usage: rovo <command> [options] [arguments]

        Available Commands:
          find         Search across integrated SaaS applications.
          learn        Interact with Rovo Chat for insights.
          act          Utilize Rovo Agents to perform tasks.
          integrations Manage integrations with other SaaS apps.
          workflow     Manage GitHub workflows.
          help         Show help information.

        Use "rovo <command> --help" for more information about a command.""",
                success=True
            ),
            CLIExecution(
                command="rovo act agents create",
                options={
                    "--name": "MaintenanceAgent",
                    "--type": "maintenance"
                },
                arguments=[],
                timestamp="2024-05-01T10:15:00Z",
                output="Rovo Agent 'MaintenanceAgent' of type 'maintenance' created successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo workflow stop",
                options={
                    "--name": "CI Pipeline"
                },
                arguments=[],
                timestamp="2024-05-01T10:20:00Z",
                output="Workflow 'CI Pipeline' stopped successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo act agents list",
                options={},
                arguments=[],
                timestamp="2024-05-01T10:25:00Z",
                output="""Available Rovo Agents:
        - DeploymentAgent (workflow)
        - KnowledgeBot (knowledge)
        - MaintenanceAgent (maintenance)""",
                success=True
            ),
            CLIExecution(
                command="rovo integrations remove",
                options={
                    "--app": "GitHub"
                },
                arguments=[],
                timestamp="2024-05-01T10:30:00Z",
                output="Integration with 'GitHub' removed successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo find search",
                options={
                    "--query": "Performance Metrics",
                    "--app": "Slack"
                },
                arguments=[],
                timestamp="2024-05-01T10:35:00Z",
                output="Found 2 results in Slack for 'Performance Metrics'.",
                success=True
            ),
            CLIExecution(
                command="rovo act agents fix",
                options={
                    "--id": "agent_12345",
                    "--fix": "update configuration"
                },
                arguments=[],
                timestamp="2024-05-01T10:40:00Z",
                output="Rovo Agent 'agent_12345' configuration updated successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo workflow view",
                options={
                    "--web": True,
                    "--name": "CI Pipeline"
                },
                arguments=[],
                timestamp="2024-05-01T10:45:00Z",
                output="Opening workflow 'CI Pipeline' in the browser...",
                success=True
            ),
            CLIExecution(
                command="rovo agents delete",
                options={
                    "--id": "agent_54321"
                },
                arguments=[],
                timestamp="2024-05-01T10:50:00Z",
                output="Rovo Agent with ID 'agent_54321' deleted successfully.",
                success=True
            ),
            CLIExecution(
                command="rovo integrations add",
                options={
                    "--app": "Microsoft Teams",
                    "--config": "./configs/teams.yaml"
                },
                arguments=[],
                timestamp="2024-05-01T10:55:00Z",
                output="Integration with 'Microsoft Teams' added successfully using configuration './configs/teams.yaml'.",
                success=True
            ),
            CLIExecution(
                command="rovo act agents list",
                options={},
                arguments=[],
                timestamp="2024-05-01T11:00:00Z",
                output="""Available Rovo Agents:
        - DeploymentAgent (workflow)
        - KnowledgeBot (knowledge)
        - MaintenanceAgent (maintenance)""",
                success=True
            )
        ]
    )

    # Serialize the CLISession to YAML
    cli_session_yaml = cli_session.to_yaml()
    print("**CLISession YAML Representation:**\n")
    print(cli_session_yaml)


if __name__ == '__main__':
    main()
