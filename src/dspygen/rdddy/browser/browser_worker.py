import asyncio
from typing import Optional

from loguru import logger
from playwright.async_api import async_playwright

from dspygen.rdddy.base_actor import BaseActor
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.rdddy.browser.browser_domain import *
from dspygen.rdddy.base_message import *


class BrowserWorker(BaseActor):
    def __init__(
        self,
        actor_system: ActorSystem,
        actor_id: Optional[int] = None,
        page: Optional[Page] = None,
        browser=None
    ):
        super().__init__(actor_system, actor_id)
        self.page = page
        self.browser = browser

    async def handle_click(self, click_cmd: Click) -> None:
        await self.page.click(
            selector=click_cmd.selector,
        )

    async def handle_goto(self, goto_cmd: Goto) -> None:
        await self.page.goto(
            url=goto_cmd.url
        )

    async def handle_type(self, type_cmd: TypeText) -> None:
        await self.page.type(
            selector=type_cmd.selector,
            text=type_cmd.text,
        )

    async def handle_send_chatgpt(self, send_cmd: SendChatGPT) -> None:
        SLEEP = 2
        #
        await asyncio.sleep(SLEEP)
        await self.publish(Click(selector="#prompt-textarea"))
        # # pyperclip.copy(publish_cmd.prompt)
        # # pyperclip.paste()
        await self.publish(TypeText(selector="#prompt-textarea", text=send_cmd.prompt))
        await asyncio.sleep(SLEEP * 5)
        await self.publish(Click(selector='[data-testid="send-button"]'))
        await asyncio.sleep(SLEEP)
        #
        # response = await process_new_responses(self.component)
        # await asyncio.sleep(SLEEP)

        # await self.actor_system.publish(ChatGPTResponse(content=response))
        # await asyncio.sleep(SLEEP)
        # print(send_cmd.prompt)

    async def handle_chatgpt_response(self, response: ChatGPTResponse) -> None:
        logger.info(f"ChatGPT response:\n\n{response}")

    async def handle_find_element(self, find_element_cmd: FindElement) -> None:
        # Implement code to find the element and send ElementFound event
        element_info = await self.page.query_selector(find_element_cmd.selector)
        if element_info:
            await self.publish(ElementFound(content=element_info))
        else:
            # Handle the case when the element is not found
            pass

    async def handle_navigate_back(self, navigate_back_cmd: NavigateBack) -> None:
        await self.page.go_back()
        # Optionally, send a navigation event indicating the back action

    async def handle_navigate_forward(
        self, navigate_forward_cmd: NavigateForward
    ) -> None:
        await self.page.go_forward()
        # Optionally, send a navigation event indicating the forward action

    async def handle_reload_page(self, reload_page_cmd: ReloadPage) -> None:
        await self.page.reload()
        # Optionally, send an event indicating that the component has been reloaded

    async def handle_get_page_content(
        self, get_page_content_cmd: GetPageContent
    ) -> None:
        page_content = await self.page.content()
        await self.publish(PageContent(content=page_content))

    async def handle_execute_script(self, execute_script_cmd: ExecuteScript) -> None:
        script_result = await self.page.evaluate(execute_script_cmd.script)
        await self.publish(ScriptResult(result=script_result))

    async def handle_close_browser(self, close_browser_cmd: CloseBrowser) -> None:
        await self.publish(BrowserClosed())

    async def handle_set_viewport_size(
        self, set_viewport_size_cmd: SetViewportSize
    ) -> None:
        await self.page.set_viewport_size(
            viewport_size={
                "width": set_viewport_size_cmd.width,
                "height": set_viewport_size_cmd.height,
            }
        )
        await self.publish(ViewportSizeSet())


async def main():
    async with async_playwright() as p:
        # Connect to an existing instance of Chrome using the connect_over_cdp method.
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")

        # Retrieve the first context of the browser.
        default_context = browser.contexts[0]

        # Retrieve the first component in the context.
        page = default_context.pages[0]

        await page.goto("https://chat.openai.com", wait_until="domcontentloaded")

        asys = ActorSystem()

        actor = await asys.actor_of(BrowserWorker, browser=browser, page=page)

        # List of prompts for generating documents
        prompts = [
            "Hello World"
        ]

        # Broadcast SendChatGPT events for each prompt
        for prompt in prompts:
            # url = "https://chat.openai.com/g/g-JWcKIFe74-bucky-v10133/c/28ccc59a-0dc5-46da-9dee-f37d71781beb"
            url = "https://chat.openai.com/"
            await asys.publish(Goto(url=url))
            await asyncio.sleep(3)
            await asys.publish(
                SendChatGPT(
                    prompt=f"Write the chapter contents like a Python enterprise architect MBBB. Full text not a summary. {prompt}. Create chapter using streamlitgen and TRIZ methodology. Combine this with the rest of what we have discussed to synthesize innovation implementation and deployment using CLI help. Add detailed section on adding to marketplace and generating revenue."
                )
            )
            await asyncio.sleep(90)


if __name__ == "__main__":
    asyncio.run(main())
