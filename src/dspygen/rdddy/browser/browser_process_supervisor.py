import asyncio
import os
import psutil
from asyncio.subprocess import Process

from loguru import logger

from dspygen.rdddy.base_actor import BaseActor
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.rdddy.browser.browser_domain import *
from dspygen.rdddy.browser.browser_worker import BrowserWorker


os.environ["PLAYWRIGHT_BROWSER"] = "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"


class BrowserProcessSupervisor(BaseActor):
    def __init__(self, actor_system):
        super().__init__(actor_system)
        self.processes: dict[str, Process] = {}  # Tracks browser processes by ID
        self.default_args = ["--remote-debugging-port=9222"]  # Default browser args
        self.health_check_running = False

    async def start_browser_process(self, cmd: StartBrowserCommand):
        if not os.getenv("PLAYWRIGHT_BROWSER"):
            raise ValueError("PLAYWRIGHT_BROWSER environment variable not set")

        if cmd.browser_id in self.processes:
            return

        args = self.default_args if cmd.custom_args is None else cmd.custom_args
        self.processes[cmd.browser_id] = await asyncio.create_subprocess_exec(
            os.getenv("PLAYWRIGHT_BROWSER"),
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # await asyncio.sleep(10)
        await self.start_health_check()
        logger.info(f"Started browser process with ID {cmd.browser_id}.")

    async def stop_browser_process(self, cmd: StopBrowserCommand):
        process = self.processes.pop(cmd.browser_id, None)
        if process:
            try:
                process.terminate()
                await self.stop_health_check()
                logger.info(f"Stopped browser process with ID {cmd.browser_id}.")
            except ProcessLookupError:
                logger.info(f"Process already terminated {cmd.browser_id}.")

    async def restart_browser_process(self, cmd: RestartBrowserCommand):
        await self.publish(StopBrowserCommand(browser_id=cmd.browser_id))
        await asyncio.sleep(5)
        await self.publish(StartBrowserCommand(browser_id=cmd.browser_id))

    async def update_browser_config(self, cmd: UpdateBrowserConfigCommand):
        logger.info(
            f"Updating browser configuration for ID {cmd.browser_id}: {cmd.new_args}"
        )
        await self.publish(RestartBrowserCommand())

    async def start_health_check(self):
        self.health_check_running = True

        while self.health_check_running:
            for browser_id, process in self.processes.items():
                stdout, stderr = await process.communicate()
                stdout_buffer_string = stdout.decode().strip()

                logger.debug(f"Starting health check for ID {browser_id}. Process Return: {process.returncode}")
                if process.returncode is None:
                    logger.info(f"Browser process {browser_id} is alive.")
                    await self.publish(BrowserStatusEvent(status="alive"))
                else:
                    logger.warning(
                        f"Browser process {browser_id} is unresponsive. Restarting..."
                    )
                    await self.publish(BrowserStatusEvent(status="dead"))
                    await self.publish(RestartBrowserCommand())
            await asyncio.sleep(10)

    async def stop_health_check(self):
        self.health_check_running = False

    async def handle_browser_status_event(self, event: BrowserStatusEvent):
        print(event)


# Example usage
async def main():
    actor_system = ActorSystem()
    proc_supervisor = await actor_system.actor_of(BrowserProcessSupervisor)
    browser_actor = await actor_system.actor_of(BrowserWorker)

    # Start Chrome Browser
    await actor_system.publish(StartBrowserCommand())

    # await actor_system.publish(StopBrowserCommand())

    # Perform browser actions using BrowserActor
    logger.info("Main function done.")

    # Stop Chrome Browser
    await asyncio.sleep(500)


if __name__ == "__main__":
    asyncio.run(main())
