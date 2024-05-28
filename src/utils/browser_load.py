from RPA.Browser.Selenium import Selenium

from src.configuration.config import URL

class LoadBrowser:
    def __init__(self) -> None:
        self.browser = Selenium()
        self.browser_load()

    def browser_load(self):
        self.browser.open_available_browser(URL)
        self.browser.maximize_browser_window()
        self.browser.wait_until_element_is_visible("//body", timeout=10)