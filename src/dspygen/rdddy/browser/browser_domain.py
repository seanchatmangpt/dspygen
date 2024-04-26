from playwright.async_api import Page

from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.base_event import BaseEvent
from dspygen.rdddy.base_message import *


# Define commands and events
class StartBrowserCommand(BaseCommand):
    browser_id: str = "default"
    custom_args: list[str] = []


class BrowserStartedEvent(BaseEvent):
    pass


class StopBrowserCommand(BaseCommand):
    browser_id: str = "default"


class RestartBrowserCommand(BaseCommand):
    browser_id: str = "default"


# Example command class for updating configuration
class UpdateBrowserConfigCommand(BaseCommand):
    browser_id: str = "default"
    new_args: dict = {}


class BrowserStatusEvent(BaseEvent):
    status: str


class Click(BaseCommand):
    """Matches the playwright component click exactly"""
    selector: str
    options: dict = {}


class Goto(BaseCommand):
    """Matches the playwright component goto exactly"""
    url: str
    options: dict = {}


class TypeText(BaseCommand):
    """Matches the playwright component type exactly"""

    selector: str
    text: str
    options: dict = {}


class SendChatGPT(BaseCommand):
    prompt: str


class ChatGPTResponse(BaseEvent):
    """Contents are the response from the site"""


class FindElement(BaseCommand):
    """Find an element by selector"""

    selector: str


class ElementFound(BaseEvent):
    """Element found in the component"""


class NavigateBack(BaseCommand):
    """Navigate back in the browser history"""


class NavigateForward(BaseCommand):
    """Navigate forward in the browser history"""


class ReloadPage(BaseCommand):
    """Reload the current component"""


class GetPageContent(BaseCommand):
    """Get the HTML content of the current component"""


class PageContent(BaseEvent):
    """HTML content of the component"""

    content: str


class ExecuteScript(BaseCommand):
    """Execute JavaScript code on the component"""

    script: str


class ScriptResult(BaseEvent):
    """Result of the executed JavaScript code"""

    result: Any  # You can specify the data type based on the expected result


class CloseBrowser(BaseCommand):
    """Close the browser"""


class BrowserClosed(BaseEvent):
    """Browser has been closed"""


class SetViewportSize(BaseCommand):
    """Set the viewport size of the browser"""

    width: int
    height: int


class ViewportSizeSet(BaseEvent):
    """Viewport size has been set successfully"""
