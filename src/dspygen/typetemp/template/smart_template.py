import asyncio
import json
import subprocess
import sys
from textwrap import dedent

import typer

from dspygen.async_typer import AsyncTyper
from dspygen.typetemp.template.async_render_mixin import AsyncRenderMixin
from dspygen.utils.complete import LLMConfig
from dspygen.utils.file_tools import write

app = AsyncTyper()


class SmartTemplate(AsyncRenderMixin):
    """Base class for creating templated classes. Uses the jinja2 templating engine
    to render templates. Allows for usage of macros and filters.
    """

    config: LLMConfig  # The LLMConfig object
    source: str  # The string template to be rendered
    to: str  # The "to" property for rendering destination
    output: str  # The rendered output

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.config = LLMConfig() if "config" not in kwargs else kwargs["config"]

    async def render(self, use_native=False, **kwargs) -> str:
        # Use NativeEnvironment when use_native is True, else use default Environment
        self.source = dedent(self.source)
        print(f"SmartTemplate kwargs: {kwargs}")
        print(f"SmartTemplate source: {self.source}")
        await self._render(use_native=use_native, **kwargs)
        print(f"SmartTemplate output: {self.output}")

        return self.output


async def render_template(source, hygen_vars, to):
    # Initialize LLMConfig and SmartTemplate with the piped source and hygen_vars
    config = LLMConfig(max_tokens=10)  # Update as needed
    template = SmartTemplate(source=source, to=to, config=config, **hygen_vars)

    # Render the SmartTemplate
    output = await template.render()
    await write(source, filename="write.txt")

    return output


async def run_shell_command(command):
    process = await asyncio.create_subprocess_shell(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = await process.communicate()
    return stdout, stderr


@app.command()
async def main(
    hygen_vars: str = typer.Option(..., "--hygen-vars"),
    to: str = typer.Option(None, help="Destination URL"),
    from_: str = typer.Option(None, "--from", help="Source URL"),
    force: bool = typer.Option(False, help="Force the generation"),
    unless_exists: bool = typer.Option(False, help="Unless the file exists"),
    inject: bool = typer.Option(False, help="Inject something"),
    after: str = typer.Option(None, help="Regex pattern for 'after'"),
    skip_if: str = typer.Option(None, help="Regex pattern for 'skip_if'"),
    sh: str = typer.Option(None, help="Shell command to execute"),
):
    typer.echo(f"Generating using hygen-vars: {hygen_vars}")
    typer.echo(f"Destination URL: {to}")
    typer.echo(f"Source URL: {from_}")
    typer.echo(f"Force: {force}")
    typer.echo(f"Unless exists: {unless_exists}")
    typer.echo(f"Inject: {inject}")
    typer.echo(f"After regex: {after}")
    typer.echo(f"Skip if regex: {skip_if}")

    source = sys.stdin.read()
    typer.echo(f"Piped text input: {source}")
    await render_template(source, json.loads(hygen_vars), to)

    if sh:
        typer.echo(f"Executing shell command: {sh}")
        stdout, stderr = await run_shell_command(sh)
        typer.echo("Shell command result:")
        typer.echo(f"STDOUT: {stdout.decode()}")
        typer.echo(f"STDERR: {stderr.decode()}")


if __name__ == "__main__":
    app()
