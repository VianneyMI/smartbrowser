"""Communication layer between the UI and the Browser Use."""

from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.browser import BrowserContext, BrowserContextConfig

def work(**kwargs)->None:
    """Sends a request to browser use."""


def dummy_work(**kwargs)->None:
    """Does nothing.
    Here for debugging and development purposes.
    """