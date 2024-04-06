from playwright.async_api import Page

from dspygen.rdddy.abstract_command import AbstractCommand
from dspygen.rdddy.abstract_event import AbstractEvent
from dspygen.rdddy.abstract_message import *


# Define commands and events
class StartBrowserCommand(AbstractCommand):
    browser_id: str = "default"
    custom_args: list[str] = []


class BrowserStartedEvent(AbstractEvent):
    pass


class StopBrowserCommand(AbstractCommand):
    browser_id: str = "default"


class RestartBrowserCommand(AbstractCommand):
    browser_id: str = "default"


# Example command class for updating configuration
class UpdateBrowserConfigCommand(AbstractCommand):
    browser_id: str = "default"
    new_args: dict = {}


class BrowserStatusEvent(AbstractEvent):
    status: str


class Click(AbstractCommand):
    """Matches the playwright component click exactly"""
    selector: str
    options: dict = {}


class Goto(AbstractCommand):
    """Matches the playwright component goto exactly"""
    url: str
    options: dict = {}


class TypeText(AbstractCommand):
    """Matches the playwright component type exactly"""

    selector: str
    text: str
    options: dict = {}


class SendChatGPT(AbstractCommand):
    prompt: str


class ChatGPTResponse(AbstractEvent):
    """Contents are the response from the site"""


class FindElement(AbstractCommand):
    """Find an element by selector"""

    selector: str


class ElementFound(AbstractEvent):
    """Element found in the component"""


class NavigateBack(AbstractCommand):
    """Navigate back in the browser history"""


class NavigateForward(AbstractCommand):
    """Navigate forward in the browser history"""


class ReloadPage(AbstractCommand):
    """Reload the current component"""


class GetPageContent(AbstractCommand):
    """Get the HTML content of the current component"""


class PageContent(AbstractEvent):
    """HTML content of the component"""

    content: str


class ExecuteScript(AbstractCommand):
    """Execute JavaScript code on the component"""

    script: str


class ScriptResult(AbstractEvent):
    """Result of the executed JavaScript code"""

    result: Any  # You can specify the data type based on the expected result


class CloseBrowser(AbstractCommand):
    """Close the browser"""


class BrowserClosed(AbstractEvent):
    """Browser has been closed"""


class SetViewportSize(AbstractCommand):
    """Set the viewport size of the browser"""

    width: int
    height: int


class ViewportSizeSet(AbstractEvent):
    """Viewport size has been set successfully"""
