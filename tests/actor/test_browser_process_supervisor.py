import asyncio
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from dspygen.rdddy.service_colony import ServiceColony
from dspygen.rdddy.browser.browser_domain import *
from dspygen.rdddy.browser.browser_process_supervisor import BrowserProcessSupervisor


class MockAsyncProcess:
    def __init__(self):
        self.returncode = None
        # self._populate_stderr()
        self._mock_stderr = MagicMock()
        self._mock_stderr.readline.side_effect = self._simulate_errors()

    def _simulate_errors(self):
        yield "Normal log line\n"
        yield "[ERROR] Simulated Error\n"
        while True:
            yield ""

    async def _populate_stderr(self):
        await self._mock_stderr.put("Normal log line\n")
        await self._mock_stderr.put("[ERROR] Simulated Error\n")
        # Simulate end of stream after error by not putting any more items

    async def communicate(self):
        return "", ""

    @property
    def stderr(self):
        return self

    async def readline(self):
        return await self._mock_stderr.get()

    def terminate(self):
        print("terminate")
        self.returncode = -1

    def poll(self):
        return self.returncode


@pytest.fixture()
def service_colony(event_loop):
    return ServiceColony(event_loop)


@pytest.mark.asyncio()
@pytest.mark.skip(reason="This test is not working as expected")
async def test_chrome_browser_restart(service_colony):
    mock_process = MockAsyncProcess()

    with patch("asyncio.create_subprocess_exec", return_value=mock_process):
        supervisor = await service_colony.inhabitant_of(BrowserProcessSupervisor)

        await service_colony.publish(StartBrowserCommand())

        # Allow time for the inhabitant to process the logs and restart Chrome Browser
        await asyncio.sleep(0.1)  # Adjust sleep time if necessary

        mock_process.terminate()

        message: BrowserStatusEvent = cast(
            BrowserStatusEvent, await service_colony.wait_for_message(BrowserStatusEvent)
        )

        assert message.status == "dead"

        start_cmd = cast(
            StartBrowserCommand,
            await service_colony.wait_for_message(StartBrowserCommand),
        )

        mock_process.returncode = None

        message = cast(
            BrowserStatusEvent, await service_colony.wait_for_message(BrowserStatusEvent)
        )

        assert message.status == "alive"
