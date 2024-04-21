# DSPyGen: Phyton - for JavaScript use: npm dpgjs
The idea of this fork is to follow up with the genius developer Sean Chatman and his work (https://github.com/seanchatmangpt/dspygen) and find out how to best and quickly get started producing the best quality.

The purpose is to use it mostly everywhere: Expert chatbots, workflows, code/data retrievers...

Thanks, and find out about the great DSPy project here https://github.com/stanfordnlp/dspy.

# My ideas: Structuring Code - A new class of Digital Assets = Dematerialized Commodity
Coming from Financial Engineering and Structuring Financial Products and also from Software Engineering to Avaloq Param, my goals are about getting all Code-Gen Systems to work in compliance and not just mixing others' IP as AI seems mostly to do today.

For such, any creator of something new and valuable should have options to receive a (micro-) payment any time their code is analyzed, cloned, or even used, especially at the enterprise level, where masses of payments might just not be paid.

The bases for all valuable, useful code should then be a new form of NFT - a Structured Commodity of Code - a variant of a Dematerialized Asset - such as I earlier created my Meta-Bricks Repo for.

Having a massive store of runnable and easily pluggable/composable elements of code, paired with terms and conditions we know from classical structured products (see e.g., Ricardian Contracts), Retrievers should use those for Code-Gen workflows, especially to keep legal risks lowest and always send payments or pay shares/revenues from their new meta-bricks derived to the creators owning the underlying product. But we are not here yet, and not many LLMs can and will reference where the code was taken from... I'm sure that can be fixed now.

# Getting Started - Find out simple structures of game code or how creators can get into 'owning' and incentivize code
First: Also in terms of privacy / data loss protection, I try to switch the init to use ollama since this week llama3 came out with decent figures.

To install ollama first go: https://ollama.com/

The default LLM should be set to model="llama3:8b-instruct-q5_1" or "llama3:70b-instruct-q3_K_M"
use 
from dspygen.lm.groq_lm import Groq
from dspygen.lm.ollama_lm import Ollama
and the init:
init_dspy(Ollama, model="llama3:8b-instruct-q5_1", max_tokens=8000)
or just run the blog_mudule.py 

Use Groq - get the API KEY from https://console.groq.com/keys
and modify your .env like seen in .envDemo 
dont forget to init
init_dspy(Groq, model="llama3-70b-8192", max_tokens=8000)

# DSPyGen: Streamlining AI Development

DSPyGen, influenced by the efficiency and modularity of Ruby on Rails, is a powerful command-line interface (CLI) designed to revolutionize AI development by leveraging DSPy modules. This tool simplifies the process of creating, developing, and deploying language model (LM) pipelines, embodying the Ruby on Rails philosophy of "Convention over Configuration" for AI projects.

### Custom GPT

[DSPyGen 2024.2.26](https://chat.openai.com/g/g-3r2Si6zdP-dspygen-2024-2-26)

## Features

- **Quick Initialization**: Set up your DSPyGen project in seconds, echoing Ruby on Rails' ease of starting new projects.
- **Modular Approach**: Inspired by Ruby on Rails' modular design, DSPyGen allows for the easy generation and enhancement of DSPy modules.
- **Intuitive Command Structure**: With user-friendly commands, managing your AI development workflow becomes as straightforward as web development with Ruby on Rails.
- **Embedded Chatbot Assistance**: For guidance and support, DSPyGen includes a chatbot, making it easier to navigate through your development process.

## Getting Started


[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?
url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/user/my-package)

or

Ensure Python is installed on your system.

Devs and local changes seems to be always compiled ok with conda for env management

conda create -n dspygen_py python=3.10
conda activate dspygen_py
poetry config virtualenvs.create false

in case needed
poetry update or add <package> 

using VS Code - Confirm correct (conda env!) Python Interpreter in VS Code
Ensure that VS Code is using the correct Python interpreter from your virtual environment where dspy-ai is installed:

- Open Command Palette in VS Code: Use Ctrl+Shift+P or Cmd+Shift+P on macOS.
- Select Interpreter: Type and select "Python: Select Interpreter."
- Choose the Correct Environment: Pick the interpreter from the virtual environment associated with your project (\envs\dspygen_py).

pip install -e . develop

on Win get your CLI up to speed and alias

Set-Alias -Name dg -Value dspygen

and 

dg --help

should work

try and run the blog-creator and run 
src\dspygen\modules\blog_module.py
compare to my run:
src\dspygen\experiments\blog\Tetris_1.md

For production envs:

```bash
pip install dspygen
```

Enhance your experience with shell completion by using the `--install-completion` option.


## Using

_Python package_: to add and install this package as a dependency of your project, run `poetry add dspygen`.

_Python CLI_: to view this app's CLI commands once it's installed, run `dspygen --help`.

_Python application_: to serve this REST API, run `docker compose up app` and open [localhost:8888](http://localhost:8000) in your browser. Within the Dev Container, this is equivalent to running `poe api`.


## Usage Overview

```plaintext
dspygen [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `--install-completion`: Adds shell completion.
- `--show-completion`: Displays the shell completion script.
- `--help`: Brings up the help message.

### Core Commands

- `command`: Adds or creates new subcommands in a Ruby on Rails-inspired CLI structure.
- `help`: Accesses a supportive chatbot for quick assistance.
- `init`: Initializes a DSPyGen project, setting up a structured environment similar to Ruby on Rails.
- `module`: Manages DSPy modules, enabling easy modifications or the creation of new ones.

### Command Details

#### Managing Commands

- **Add a Command**: Extend functionality seamlessly, reminiscent of Ruby on Rails plugins.

  ```bash
  dspygen command add [existing_command] [new_command]
  ```

- **New Command Module**: Start new functionalities with ease.

  ```bash
  dspygen command new [new_command_name]
  ```

### Modules Management

- **New Module Generation**: Create new DSPy modules to extend your project's capabilities.

  ```bash
  dspygen module new 'text -> summary'
  ```

## Project Structure

Following a clear and organized structure influenced by Ruby on Rails, DSPyGen projects are easy to navigate:

```
.
├── src
│   ├── dspygen
│   │   ├── modules
│   │   └── subcommands
│   └── typetemp
└── tests
```

## Help and Documentation

For detailed command information or assistance, use:

```bash
dspygen [command] --help
```

## Contributing

We welcome contributions to DSPyGen, whether it's new features, improvements, or bug fixes. Feel free to fork the repository, make changes, and submit a pull request.

## License

DSPyGen is open-source, licensed under the MIT License.

Adopting DSPyGen for your AI projects not only simplifies the development process but also incorporates the structured, efficient approach pioneered by Ruby on Rails into the realm of AI and machine learning.

## Contributing

<details>
<summary>Prerequisites</summary>

<details>
<summary>1. Set up Git to use SSH</summary>

1. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) and [add the SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
1. Configure SSH to automatically load your SSH keys:
    ```sh
    cat << EOF >> ~/.ssh/config
    Host *
      AddKeysToAgent yes
      IgnoreUnknown UseKeychain
      UseKeychain yes
    EOF
    ```

</details>

<details>
<summary>2. Install Docker</summary>

1. [Install Docker Desktop](https://www.docker.com/get-started).
    - Enable _Use Docker Compose V2_ in Docker Desktop's preferences window.
    - _Linux only_:
        - Export your user's user id and group id so that [files created in the Dev Container are owned by your user](https://github.com/moby/moby/issues/3206):
            ```sh
            cat << EOF >> ~/.bashrc
            export UID=$(id --user)
            export GID=$(id --group)
            EOF
            ```

</details>

<details>
<summary>3. Install VS Code or PyCharm</summary>

1. [Install VS Code](https://code.visualstudio.com/) and [VS Code's Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Alternatively, install [PyCharm](https://www.jetbrains.com/pycharm/download/).
2. _Optional:_ install a [Nerd Font](https://www.nerdfonts.com/font-downloads) such as [FiraCode Nerd Font](https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/FiraCode) and [configure VS Code](https://github.com/tonsky/FiraCode/wiki/VS-Code-Instructions) or [configure PyCharm](https://github.com/tonsky/FiraCode/wiki/Intellij-products-instructions) to use it.

</details>

</details>

<details open>
<summary>Development environments</summary>

The following development environments are supported:

1. ⭐️ _GitHub Codespaces_: click on _Code_ and select _Create codespace_ to start a Dev Container with [GitHub Codespaces](https://github.com/features/codespaces).
1. ⭐️ _Dev Container (with container volume)_: click on [Open in Dev Containers](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/user/my-package) to clone this repository in a container volume and create a Dev Container with VS Code.
1. _Dev Container_: clone this repository, open it with VS Code, and run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Dev Containers: Reopen in Container_.
1. _PyCharm_: clone this repository, open it with PyCharm, and [configure Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote) with the `dev` service.
1. _Terminal_: clone this repository, open it with your terminal, and run `docker compose up --detach dev` to start a Dev Container in the background, and then run `docker compose exec dev zsh` to open a shell prompt in the Dev Container.

</details>

<details>
<summary>Developing</summary>

- Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available to run on this project.
- Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml` and `poetry.lock`. Add `--group test` or `--group dev` to install a CI or development dependency, respectively.
- Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.

</details>
