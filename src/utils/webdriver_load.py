from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from src.configuration.config import URL


class WebDriverLoad:
    def __init__(self) -> None:
        self.website = URL
        self.webdriver_load()

    def webdriver_load(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        self.driver = webdriver.Chrome(options=options)
        self.wait1 = WebDriverWait(self.driver, 3)
        self.wait2 = WebDriverWait(self.driver, 5)
        self.wait3 = WebDriverWait(self.driver, 30)
        self.driver.get(self.website)
