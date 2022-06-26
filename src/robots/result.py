from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.schema import *
from src.utils.constants import Race
from src.storage.storage import Storage
from src.robots.robot import Robot, RESPONSE_TIMEOUT

URL_RACE_RESULT_PREFIX = \
    'https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx'

URL_RESULT_DIVIDENDS = \
    URL_RACE_RESULT_PREFIX + '?RaceDate={}'

URL_RESULT_DETAIL = \
    URL_RACE_RESULT_PREFIX + '?RaceDate={}&Racecourse={}&RaceNo={}'

URL_RACE_VIDEO = \
    'https://racing.hkjc.com/racing/video/play.asp?type=replay-full' \
    '&date={}&no={}&lang=eng'

XPATH_RESULT_DIV = '//div[contains(@class, "localResults")]'
XPATH_DIVIDEND_TABLE_BODY = '//div[contains(@class, "dividend_tab")]/table/tbody'
XPATH_PERFORMANCE_TABLE = '//div[contains(@class, "performance")]/table'


class RaceResultRobot(Robot):

    def run(self, race_date: str):
        url = URL_RESULT_DIVIDENDS.format(race_date.replace('-', '/'))
        browser = None
        try:
            browser = self.get_browser()
            browser.get(url)
        except:
            pass
        finally:
            if browser:
                browser.quit()
