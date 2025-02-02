from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverManager:
    @staticmethod
    def create_driver(headless: bool = False):
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    @staticmethod
    def create_remote_driver(url: str = 'http://localhost:4444/wd/hub'):
        options = ChromeOptions()
        driver = webdriver.Remote(
            command_executor=url,
            options=options
        )
        return driver
