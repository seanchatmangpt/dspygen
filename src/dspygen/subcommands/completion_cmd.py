"""Shell completion subcommand for dspygen."""
import subprocess
import sys

import typer

app = typer.Typer(help="Generate shell completion scripts")

SUPPORTED_SHELLS = ["bash", "zsh", "fish", "powershell"]

INSTALL_PATHS = {
    "bash": "~/.bashrc",
    "zsh": "~/.zshrc",
    "fish": "~/.config/fish/completions/dspygen.fish",
    "powershell": "~/.config/powershell/Microsoft.PowerShell_profile.ps1",
}

INSTALL_LINES = {
    "bash": 'source <(_DSPYGEN_COMPLETE=bash_source dspygen)',
    "zsh": 'source <(_DSPYGEN_COMPLETE=zsh_source dspygen)',
    "fish": None,  # Fish writes directly to a file
    "powershell": None,
}


@app.command("install")
def install_completion(
    shell: str = typer.Argument("bash", help="Shell to install completions for: bash, zsh, fish, powershell"),
):
    """Install shell completions for dspygen into your shell's config file."""
    if shell not in SUPPORTED_SHELLS:
        typer.echo(f"Unsupported shell: {shell!r}. Choose from: {', '.join(SUPPORTED_SHELLS)}", err=True)
        raise typer.Exit(1)

    env_var = f"_DSPYGEN_COMPLETE={shell}_source"

    # Generate the completion script
    try:
        result = subprocess.run(
            ["env", env_var, "dspygen"],
            capture_output=True,
            text=True,
        )
        completion_script = result.stdout
    except FileNotFoundError:
        # Fallback: try to produce it via the current Python executable
        result = subprocess.run(
            [sys.executable, "-m", "dspygen"],
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "_DSPYGEN_COMPLETE": f"{shell}_source"},
        )
        completion_script = result.stdout

    if shell == "fish":
        import os
        from pathlib import Path

        fish_dir = Path.home() / ".config" / "fish" / "completions"
        fish_dir.mkdir(parents=True, exist_ok=True)
        dest = fish_dir / "dspygen.fish"
        dest.write_text(completion_script)
        typer.echo(f"Fish completions installed to {dest}")
        return

    if shell == "powershell":
        import os
        from pathlib import Path

        ps_profile = Path(INSTALL_PATHS["powershell"]).expanduser()
        ps_profile.parent.mkdir(parents=True, exist_ok=True)
        line = f'Register-ArgumentCompleter -Native -CommandName dspygen -ScriptBlock ${{scriptBlock}}'
        with ps_profile.open("a") as f:
            f.write(f"\n# dspygen shell completion\n{completion_script}\n")
        typer.echo(f"PowerShell completions appended to {ps_profile}")
        return

    # bash / zsh: append a source line to the RC file
    from pathlib import Path

    rc_file = Path(INSTALL_PATHS[shell]).expanduser()
    source_line = INSTALL_LINES[shell]

    existing = rc_file.read_text() if rc_file.exists() else ""
    if source_line in existing:
        typer.echo(f"Completion already installed in {rc_file}. Nothing to do.")
        return

    with rc_file.open("a") as f:
        f.write(f"\n# dspygen shell completion\n{source_line}\n")

    typer.echo(f"Completions installed. Reload your shell or run:\n  source {rc_file}")


@app.command("show")
def show_completion(
    shell: str = typer.Argument("bash", help="Shell to show completions for: bash, zsh, fish, powershell"),
):
    """Print the completion script to stdout (for manual sourcing)."""
    if shell not in SUPPORTED_SHELLS:
        typer.echo(f"Unsupported shell: {shell!r}. Choose from: {', '.join(SUPPORTED_SHELLS)}", err=True)
        raise typer.Exit(1)

    import os

    env = {**os.environ, "_DSPYGEN_COMPLETE": f"{shell}_source"}
    try:
        result = subprocess.run(
            ["dspygen"],
            capture_output=True,
            text=True,
            env=env,
        )
        if result.stdout:
            typer.echo(result.stdout, nl=False)
        else:
            typer.echo(result.stderr or "(no output from completion generator)", err=True)
    except FileNotFoundError:
        result = subprocess.run(
            [sys.executable, "-m", "dspygen"],
            capture_output=True,
            text=True,
            env=env,
        )
        typer.echo(result.stdout, nl=False)
