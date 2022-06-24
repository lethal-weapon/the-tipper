from abc import ABC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

MAX_RETRY_COUNT = 3
RESPONSE_TIMEOUT = 30


class Robot(ABC):

    def get_browser(self):
        retry_count = 0
        while True:
            try:
                return webdriver.Chrome(
                    service=self.__get_browser_service(),
                    options=self.__get_browser_options()
                )
            except Exception as ex:
                retry_count += 1
                if retry_count == MAX_RETRY_COUNT:
                    print(f'Failed to create a browser instance '
                          f'after {MAX_RETRY_COUNT} retries')
                    raise ex

    @staticmethod
    def __get_browser_service():
        return Service(ChromeDriverManager().install())

    @staticmethod
    def __get_browser_options():
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('--enable-javascript')
        options.add_argument('--disk-cache-dir=/dev/null')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        return options
