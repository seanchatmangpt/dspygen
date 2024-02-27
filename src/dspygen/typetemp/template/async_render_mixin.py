from typing import Any

import anyio

from dspygen.typetemp.environment.typed_environment import async_environment
from dspygen.typetemp.environment.typed_native_environment import (
    async_native_environment,
)
from dspygen.typetemp.template.render_funcs import arender_str
from dspygen.utils.complete import acreate
from dspygen.utils.file_tools import write


class AsyncRenderMixin:
    """An async mixin class that encapsulates the render and _render_vars functionality."""

    def __init__(self):
        self.source = ""
        self.to = ""
        self.config = None

    async def _render(self, use_native=False, **kwargs) -> Any:
        """Render the template."""
        self._env = async_native_environment if use_native else async_environment

        template = self._env.from_string(
            self.source
        )  # Assuming self.env is a jinja2.Environment

        render_dict = kwargs.copy()
        render_dict.update(await self._render_vars())

        self.output = await template.render_async(**render_dict)
        # print("render output", self.output)

        await self._llm_call()

        if self.to == "stdout":
            print(self.output)
        elif self.to:
            # to_template = self._env.from_string(self.to)
            try:
                await write(self.output, filename=self.to)
            except FileNotFoundError as e:
                print("Did you include the correct path?")
                raise e

        return self.output

    async def _render_vars(self) -> dict[str, Any]:
        properties = self.__class__.__dict__.copy()
        properties.update(self.__dict__.copy())
        # print(properties)

        async with anyio.create_task_group() as tg:
            for name, value in properties.items():
                if isinstance(value, AsyncRenderMixin):
                    tg.start_soon(self._concurrent_render, name, value, properties)
                elif isinstance(value, str):
                    properties[name] = await arender_str(value)

        return properties

    async def _concurrent_render(
        self, name: str, value: "AsyncRenderMixin", properties: dict[str, Any]
    ):
        properties[name] = await value._render()

    async def _llm_call(self):
        """Use a LLM to render the template as a prompt."""
        if self.config:
            # print(self.output)
            self.output = await acreate(prompt=self.output, config=self.config)
