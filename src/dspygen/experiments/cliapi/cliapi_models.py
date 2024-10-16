from dspygen.utils.dsl_tools import DSLModel
from typing import List, Optional, Dict, Any, Type, TypeVar
from pydantic import Field, ValidationError


class CLIMetadata(DSLModel):
    name: str = Field(..., description="Name of the CLI tool.")
    version: str = Field(..., description="Version of the CLI tool.")
    description: str = Field(..., description="Description of the CLI tool.")
    author: str = Field(..., description="Author or organization responsible for the CLI tool.")


class CLIOption(DSLModel):
    name: str = Field(..., description="The name of the option (e.g., '--help').")
    description: str = Field(..., description="Description of what the option does.")
    type: str = Field(..., description="Data type of the option (e.g., 'boolean', 'string').")
    default: Optional[Any] = Field(None, description="Default value of the option if not provided.")
    required: bool = Field(False, description="Whether the option is required.")
    aliases: Optional[List[str]] = Field(None, description="Alternative names for the option.")


class CLIArgument(DSLModel):
    name: str = Field(..., description="The name of the argument.")
    description: str = Field(..., description="Description of the argument.")
    required: bool = Field(False, description="Whether the argument is required.")


class CLISubcommand(DSLModel):
    name: str = Field(..., description="The name of the subcommand.")
    description: str = Field(..., description="Description of the subcommand.")
    options: List[CLIOption] = Field(default_factory=list, description="List of options available for the subcommand.")
    arguments: List[CLIArgument] = Field(default_factory=list, description="List of arguments required by the subcommand.")
    examples: Optional[List[str]] = Field(None, description="Example usages of the subcommand.")
    subcommands: Optional[List['CLISubcommand']] = Field(None, description="Nested subcommands.")


class CLICommand(DSLModel):
    name: str = Field(..., description="The name of the command.")
    description: str = Field(..., description="Description of the command.")
    global_options: List[CLIOption] = Field(default_factory=list, description="List of global options applicable to the command.")
    subcommands: List[CLISubcommand] = Field(default_factory=list, description="List of subcommands under the command.")


class CLIPluginCommand(DSLModel):
    name: str = Field(..., description="The name of the plugin command.")
    description: str = Field(..., description="Description of the plugin command.")
    subcommands: List[CLISubcommand] = Field(default_factory=list, description="List of subcommands under the plugin command.")


class CLIPlugin(DSLModel):
    name: str = Field(..., description="The name of the plugin.")
    description: str = Field(..., description="Description of the plugin.")
    commands: List[CLIPluginCommand] = Field(default_factory=list, description="List of commands provided by the plugin.")


class CLIExtensionCommand(DSLModel):
    name: str = Field(..., description="The name of the extensions command.")
    description: str = Field(..., description="Description of the extensions command.")
    subcommands: List[CLISubcommand] = Field(default_factory=list, description="List of subcommands under the extensions command.")


class CLIExtension(DSLModel):
    name: str = Field(..., description="The name of the extensions.")
    description: str = Field(..., description="Description of the extensions.")
    commands: List[CLIExtensionCommand] = Field(default_factory=list, description="List of commands provided by the extensions.")


class CLIMarketplaceCommand(DSLModel):
    name: str = Field(..., description="The name of the marketplace command.")
    description: str = Field(..., description="Description of the marketplace command.")
    options: List[CLIOption] = Field(default_factory=list, description="List of options available for the marketplace command.")
    arguments: List[CLIArgument] = Field(default_factory=list, description="List of arguments required by the marketplace command.")
    examples: Optional[List[str]] = Field(None, description="Example usages of the marketplace command.")


class CLIMarketplace(DSLModel):
    name: str = Field(..., description="The name of the marketplace.")
    description: str = Field(..., description="Description of the marketplace.")
    subcommands: List[CLIMarketplaceCommand] = Field(default_factory=list, description="List of marketplace-related commands.")


class CLIConfiguration(DSLModel):
    globals: Dict[str, Any] = Field(default_factory=dict, description="Global configuration settings.")
    repository: Dict[str, Any] = Field(default_factory=dict, description="Repository-specific configuration settings.")


class CLIVoiceSettings(DSLModel):
    voice_format: str = Field("wav", description="Audio format for voice recording.")
    voice_language: str = Field("en", description="Language for voice commands using ISO 639-1 code.")


class CLIAccessibilityFeatures(DSLModel):
    screen_reader_support: bool = Field(True, description="Enable support for screen readers.")
    high_contrast_mode: bool = Field(False, description="Enable high contrast mode for better visibility.")
    keyboard_navigation: bool = Field(True, description="Enable keyboard navigation for CLI interactions.")


class CLIIntegration(DSLModel):
    hygen: Optional[Dict[str, Any]] = Field(None, description="Configuration for Hygen integration.")
    llm_code_assistants: Optional[Dict[str, Any]] = Field(None, description="Configuration for LLM-powered code assistants.")


class CLIAPI(DSLModel):
    metadata: CLIMetadata = Field(..., description="Metadata information for the CLI.")
    commands: List[CLICommand] = Field(default_factory=list, description="List of top-level commands.")
    plugins: List[CLIPlugin] = Field(default_factory=list, description="List of plugins.")
    extensions: List[CLIExtension] = Field(default_factory=list, description="List of extensions.")
    marketplace: Optional[CLIMarketplace] = Field(None, description="Marketplace integration.")
    configurations: Optional[CLIConfiguration] = Field(None, description="Configuration settings.")
    voice_settings: Optional[CLIVoiceSettings] = Field(None, description="Voice control settings.")
    accessibility_features: Optional[CLIAccessibilityFeatures] = Field(None, description="Accessibility features.")
    integrations: Optional[CLIIntegration] = Field(None, description="External tool integrations.")


class CLIExecution(DSLModel):
    command: str = Field(..., description="The CLI command that was executed.")
    options: Dict[str, Any] = Field(default_factory=dict, description="Options provided with the command.")
    arguments: List[str] = Field(default_factory=list, description="Arguments provided to the command.")
    timestamp: str = Field(..., description="Timestamp of when the command was executed.")
    output: Optional[str] = Field(None, description="Output returned by the command.")
    success: bool = Field(..., description="Indicates if the command executed successfully.")
    error_message: Optional[str] = Field(None, description="Error message if the command failed.")


class CLISession(DSLModel):
    session_id: str = Field(..., description="Unique identifier for the CLI session.")
    start_time: str = Field(..., description="Timestamp when the session started.")
    end_time: Optional[str] = Field(None, description="Timestamp when the session ended.")
    executions: List[CLIExecution] = Field(default_factory=list, description="List of CLI executions in the session.")
    user: str = Field(..., description="Username of the individual who initiated the session.")
    environment: Dict[str, Any] = Field(default_factory=dict, description="Environment variables and settings during the session.")


# Example Usage
def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_lm
    init_lm()

    github_cli_metadata = CLIMetadata(
        name="GitHub CLI",
        version="2.35.0",
        description="A command-line tool for interacting with GitHub.",
        author="GitHub, Inc."
    )

    github_cli = CLIAPI(
        metadata=github_cli_metadata,
        commands=[
            CLICommand(
                name="gh",
                description="GitHub CLI main command for interacting with GitHub repositories and services.",
                global_options=[
                    CLIOption(
                        name="--version",
                        description="Display the version of GitHub CLI.",
                        type="boolean"
                    ),
                    CLIOption(
                        name="--help",
                        description="Show help information for GitHub CLI.",
                        type="boolean"
                    )
                ],
                subcommands=[
                    CLISubcommand(
                        name="repo",
                        description="Manage GitHub repositories.",
                        options=[
                            CLIOption(
                                name="--public",
                                description="Create a public repository.",
                                type="boolean"
                            ),
                            CLIOption(
                                name="--private",
                                description="Create a private repository.",
                                type="boolean"
                            )
                        ],
                        arguments=[
                            CLIArgument(
                                name="name",
                                description="Name of the repository.",
                                required=True
                            )
                        ],
                        examples=[
                            "gh repo create my-repo --public",
                            "gh repo clone my-repo"
                        ],
                        subcommands=[
                            CLISubcommand(
                                name="clone",
                                description="Clone a repository to your local machine.",
                                options=[
                                    CLIOption(
                                        name="--depth",
                                        description="Create a shallow clone with a history truncated to the specified number of commits.",
                                        type="integer"
                                    )
                                ],
                                arguments=[
                                    CLIArgument(
                                        name="repository",
                                        description="The repository to clone.",
                                        required=True
                                    )
                                ],
                                examples=[
                                    "gh repo clone owner/repo",
                                    "gh repo clone owner/repo --depth 1"
                                ]
                            )
                        ]
                    ),
                    # Additional subcommands can be added here
                ]
            )
        ],
        plugins=[
            CLIPlugin(
                name="octo-org/octo-plugin",
                description="A plugin to enhance GitHub CLI with additional organizational tools.",
                commands=[
                    CLIPluginCommand(
                        name="octo",
                        description="Organizational tools provided by the octo-plugin.",
                        subcommands=[
                            CLISubcommand(
                                name="sync",
                                description="Synchronize organizational repositories.",
                                options=[
                                    CLIOption(
                                        name="--force",
                                        description="Force synchronization even if conflicts exist.",
                                        type="boolean"
                                    )
                                ],
                                arguments=[
                                    CLIArgument(
                                        name="organization",
                                        description="Name of the organization to synchronize.",
                                        required=True
                                    )
                                ],
                                examples=[
                                    "gh octo sync octo-org --force"
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        extensions=[
            CLIExtension(
                name="gh-extras",
                description="Additional commands and functionalities for GitHub CLI.",
                commands=[
                    CLIExtensionCommand(
                        name="extras",
                        description="Extra tools and utilities.",
                        subcommands=[
                            CLISubcommand(
                                name="deploy",
                                description="Deploy the repository to a specified environments.",
                                options=[
                                    CLIOption(
                                        name="--env",
                                        description="Target environments for deployment.",
                                        type="string",
                                        required=True
                                    )
                                ],
                                arguments=[
                                    CLIArgument(
                                        name="repository",
                                        description="Repository to deploy.",
                                        required=True
                                    )
                                ],
                                examples=[
                                    "gh extras deploy owner/repo --env production"
                                ]
                            ),
                            CLISubcommand(
                                name="backup",
                                description="Backup the repository data.",
                                options=[
                                    CLIOption(
                                        name="--destination",
                                        description="Backup destination path.",
                                        type="string",
                                        required=True
                                    )
                                ],
                                arguments=[
                                    CLIArgument(
                                        name="repository",
                                        description="Repository to backup.",
                                        required=True
                                    )
                                ],
                                examples=[
                                    "gh extras backup owner/repo --destination /backups/repo-backup.tar.gz"
                                ]
                            )
                        ]
                    )
                ]
            )
        ],
        marketplace=CLIMarketplace(
            name="GitHub Marketplace",
            description="A marketplace for GitHub CLI plugins and extensions.",
            subcommands=[
                CLIMarketplaceCommand(
                    name="browse",
                    description="Browse available plugins and extensions in the GitHub Marketplace.",
                    options=[
                        CLIOption(
                            name="--category",
                            description="Filter by category.",
                            type="string"
                        ),
                        CLIOption(
                            name="--sort",
                            description="Sort results by criteria (e.g., popularity, date).",
                            type="string"
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
                        "gh marketplace browse --category productivity",
                        "gh marketplace browse --sort popularity"
                    ]
                ),
                CLIMarketplaceCommand(
                    name="install",
                    description="Install a plugin or extensions from the GitHub Marketplace.",
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
                        "gh marketplace install gh-extras/gh-deploy-plugin"
                    ]
                )
            ]
        ),
        configurations=CLIConfiguration(
            globals={
                "editor": {
                    "description": "Default text editor for GitHub CLI operations.",
                    "type": "string",
                    "default": "vim"
                },
                "pager": {
                    "description": "Default pager for displaying command outputs.",
                    "type": "string",
                    "default": "less"
                },
                "theme": {
                    "description": "Color theme for GitHub CLI output.",
                    "type": "string",
                    "default": "auto"
                }
            },
            repository={
                "default_branch": {
                    "description": "Default branch name for new repositories.",
                    "type": "string",
                    "default": "main"
                },
                "visibility": {
                    "description": "Default visibility for new repositories.",
                    "type": "string",
                    "default": "private"
                }
            }
        ),
        voice_settings=CLIVoiceSettings(
            voice_format="wav",
            voice_language="en"
        ),
        accessibility_features=CLIAccessibilityFeatures(
            screen_reader_support=True,
            high_contrast_mode=False,
            keyboard_navigation=True
        ),
        integrations=CLIIntegration(
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
                            "gh hygen --template react component Button",
                            "gh hygen --template node service AuthService"
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
                            "gh assist --prompt 'Optimize this function' main.py",
                            "gh assist --prompt 'Generate unit tests' src/utils.py --model gpt-4-turbo"
                        ]
                    }
                ]
            }
        )
    )

    # Serialize to YAML
    yaml_output = github_cli.to_yaml("github_cli.yaml")
    print(yaml_output)


if __name__ == '__main__':
    main()
