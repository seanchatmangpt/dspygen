Installation
============

Install dspygen using pip or poetry:

.. code-block:: bash

    pip install dspygen
    # or
    poetry add dspygen

Shell Completions
-----------------

dspygen supports shell completions for bash, zsh, fish, and PowerShell.
There are two ways to enable completions:

**Automatic install (recommended)**

Use the built-in ``completion install`` subcommand to append the necessary
source line to your shell's RC file automatically:

.. code-block:: bash

    # Bash
    dspygen completion install bash

    # Zsh
    dspygen completion install zsh

    # Fish
    dspygen completion install fish

    # PowerShell
    dspygen completion install powershell

After running the command, reload your shell:

.. code-block:: bash

    source ~/.bashrc   # bash
    source ~/.zshrc    # zsh
    # fish and PowerShell pick up changes automatically on next launch

**Manual install**

Print the completion script to stdout and source it yourself:

.. code-block:: bash

    # Bash — add to ~/.bashrc
    source <(dspygen completion show bash)

    # Zsh — add to ~/.zshrc
    source <(dspygen completion show zsh)

    # Fish — write to the completions directory
    dspygen completion show fish > ~/.config/fish/completions/dspygen.fish

**Using Typer's built-in mechanism directly**

Typer also exposes completion generation via environment variables:

.. code-block:: bash

    # Generate and source in one step (bash)
    source <(_DSPYGEN_COMPLETE=bash_source dspygen)

    # Generate and source in one step (zsh)
    source <(_DSPYGEN_COMPLETE=zsh_source dspygen)

**Static completion scripts**

Pre-built completion scripts ship with dspygen in the
``src/dspygen/completions/`` directory:

- ``bash_completion.sh`` — Bash
- ``zsh_completion.zsh`` — Zsh
- ``fish_completion.fish`` — Fish

To use them directly:

.. code-block:: bash

    # Bash
    source /path/to/site-packages/dspygen/completions/bash_completion.sh

    # Zsh (copy to a directory on your $fpath)
    cp /path/to/site-packages/dspygen/completions/zsh_completion.zsh \
        ~/.zsh/completions/_dspygen
    autoload -Uz compinit && compinit

    # Fish
    cp /path/to/site-packages/dspygen/completions/fish_completion.fish \
        ~/.config/fish/completions/dspygen.fish
