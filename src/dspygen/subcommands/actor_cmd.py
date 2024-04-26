import asyncio

import typer
from subprocess import Popen, PIPE, CalledProcessError
import os
import signal

from dspygen.async_typer import AsyncTyper
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.actor_system import ActorSystem

app = AsyncTyper(help="")

MOSQUITTO_BINARY = os.getenv("MOSQUITTO_BINARY", default="/usr/sbin/mosquitto")
MOSQUITTO_CONF = os.getenv("MOSQUITTO_CONF", default="/etc/mosquitto/mosquitto.conf")
PID_FILE = '/tmp/mosquitto.pid'


def process_is_running(pid: int) -> bool:
    """Check if there's a running process with the given PID."""
    try:
        os.kill(pid, 0)  # No signal is sent, but error checking is still performed
    except OSError:
        return False
    else:
        return True


@app.command(name="start")
async def start_mqtt(broker_path: str = MOSQUITTO_BINARY, config_path: str = MOSQUITTO_CONF):
    """Starts the Mosquitto MQTT broker."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as file:
            pid = int(file.read().strip())
            if process_is_running(pid):
                typer.echo("MQTT Broker is already running.")
                raise typer.Exit()
            else:
                os.remove(PID_FILE)  # PID file is stale, remove it

    if not os.path.exists(broker_path):
        typer.echo(f"The specified broker path does not exist: {broker_path}")
        raise typer.Exit()

    if not os.path.exists(config_path):
        typer.echo(f"The specified config path does not exist: {config_path}")
        raise typer.Exit()

    mqtt_process = Popen([broker_path, '-c', config_path])

    with open(PID_FILE, 'w') as file:
        file.write(str(mqtt_process.pid))

    typer.echo("MQTT Broker started.")


@app.command(name="sys")
async def sys_cmd():
    """Starts the ActorSystem."""
    actor_system = ActorSystem()

    while True:
        await asyncio.sleep(5)


@app.command(name="stop")
def stop_mqtt():
    """Stops the Mosquitto MQTT broker."""
    if not os.path.exists(PID_FILE):
        typer.echo("MQTT Broker is not running or PID file is missing.")
        raise typer.Exit()

    with open(PID_FILE, 'r') as file:
        pid = int(file.read().strip())

    if process_is_running(pid):
        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)
        typer.echo("MQTT Broker stopped.")
    else:
        os.remove(PID_FILE)  # Clean up stale PID file
        typer.echo("MQTT Broker was not running. Cleaned up PID file.")


@app.command(name="msg")
async def start_actor_system(message: str):
    """Starts the actor system with MQTT integration."""
    actor_system = ActorSystem()

    await actor_system.publish(BaseCommand(content=message))


@app.command(name="new")
async def new_actor():
    """Uses a Jinja template to generate a new actor."""


if __name__ == "__main__":
    app()
