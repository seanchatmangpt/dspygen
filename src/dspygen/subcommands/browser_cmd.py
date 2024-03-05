"""browser"""
import asyncio

import typer

from dspygen.async_typer import AsyncTyper
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.rdddy.browser.browser_domain import StartBrowserCommand
from dspygen.rdddy.browser.browser_process_supervisor import BrowserProcessSupervisor
from dspygen.rdddy.browser.browser_worker import BrowserWorker

app = AsyncTyper()


@app.command(name="browser")
def browser():
    """browser"""
    typer.echo("Running browser subcommand.")


@app.command(name="open")
async def browser_open(lifetime: int = 60*60):
    """Open a browser with the given lifetime with a browser process supervisor."""
    actor_system = ActorSystem()
    proc_supervisor = await actor_system.actor_of(BrowserProcessSupervisor)
    browser_actor = await actor_system.actor_of(BrowserWorker)

    # Start Chrome Browser
    await actor_system.publish(StartBrowserCommand())

    # await actor_system.publish(StopBrowserCommand())

    # Perform browser actions using BrowserActor
    typer.echo("Main function done.")

    # Stop Chrome Browser
    await asyncio.sleep(lifetime)
