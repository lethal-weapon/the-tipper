from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.schema import *
from src.utils.constants import Race
from src.storage.storage import Storage
from src.robots.robot import Robot, RESPONSE_TIMEOUT
from src.robots.result import URL_RESULT_DETAIL, URL_RACE_VIDEO

URL_RACE_CARD = 'https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx'

XPATH_RACE_NUM_ROW = '//div[contains(@class, "racingNum")]/table/tbody/tr[1]'
XPATH_GEAR_DETAIL_DIV = '//div[contains(@class, "Gear")]'
XPATH_RACE_INFO_DIV = '//div[contains(@class, "margin_top10")]/div[contains(@class, "f_fs13")]'


class RaceRobot(Robot):

    def run(self):
        browser, race_date = None, ''
        try:
            browser = self.get_browser()
            race_urls = self.get_race_urls(browser)

            # scratch, clean and save race card according to each race url
            # one race failure shouldn't affect the others
            for url in race_urls:
                try:
                    card = self.clean_one(self.scratch_one(browser, url))
                    if not are_all_fields_exist_and_valid(card, RACE_INFO_VALIDATION_SCHEMA):
                        raise RuntimeError(f'Invalid racecard: {card}')

                    race_date = card[Race.RACE_DATE]
                    Storage.save_race(card)
                except:
                    pass
        except:
            pass
        finally:
            if browser:
                browser.quit()
            if check_race_date(race_date):
                Storage.write(race_date)

    @staticmethod
    def get_race_urls(browser) -> [str]:
        race_urls = []

        # go to the latest race card page of the latest race day, this page
        # always shows the immediate race which could be race #1 ~ #11
        browser.get(URL_RACE_CARD)
        WebDriverWait(browser, RESPONSE_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, XPATH_RACE_NUM_ROW)))

        # first cell of this row contains race venue/racecourse
        # rest cells contain respective race's race card url
        xpath_cells = f'{XPATH_RACE_NUM_ROW}/td'
        cells = len(browser.find_elements(By.XPATH, xpath_cells))
        missing_nums = []

        # currently displayed race doesn't have the anchor element inside
        # for simulcast race day, there will be some empty cells in the middle
        for i in range(2, cells + 1):
            xpath_anchor = f'{xpath_cells}[{str(i)}]/a'
            try:
                anchor = browser.find_element(By.XPATH, xpath_anchor)
                race_urls.append(anchor.get_attribute('href'))
            except:
                missing_nums.append(i - 1)
                missing_nums.append(i - 2)

        # create currently displayed race's url to make sure it's
        # uniform with the rest, rather than using the current url
        # also, put it at the head of the list, since it's more important
        # e.g. {URL_RACE_CARD}?RaceDate=2022/04/27&Racecourse=HV&RaceNo=9
        for missing_num in missing_nums:
            if missing_num < 1 or missing_num > 11:
                continue
            existing: str = race_urls[0]
            prefix = existing[:existing.rfind('=') + 1]
            missing_url = f'{prefix}{missing_num}'

            if missing_url not in race_urls:
                race_urls.insert(0, missing_url)

        return race_urls

    def scratch_one(self, browser, url: str) -> dict:
        """ A wrapper method for scratch_info. """
        race_date, race_num, venue_code = to_race_date_num_venue(url)
        raw_card = {
            Race.RACE_DATE: race_date,
            Race.RACE_NUM: race_num,
            Race.VENUE: venue_code,
            Race.VIDEO_URL: URL_RACE_VIDEO.format(
                race_date.replace('-', ''),
                f'0{race_num}' if int(race_num) < 10 else race_num
            ),
            Race.RESULT_URL: URL_RESULT_DETAIL.format(
                race_date.replace('-', '/'),
                venue_code,
                race_num
            ),
        }

        try:
            browser.get(url)
            WebDriverWait(browser, RESPONSE_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, XPATH_GEAR_DETAIL_DIV)))

            self.scratch_info(browser, raw_card, race_date)
        except Exception as ex:
            print(f'Error while scratching: {url}: {str(ex)}')
            raise ex

        return raw_card

    @staticmethod
    def scratch_info(browser, raw: dict, race_date: str):
        race_text = browser.find_element(By.XPATH, XPATH_RACE_INFO_DIV).text
        race_name = browser.find_element(By.XPATH, f'{XPATH_RACE_INFO_DIV}/span').text
        # race_text contains race_name (first line below), it looks like:

        # Race 1 - CHAI WAN ROAD HANDICAP
        # Saturday, June 25, 2022, Sha Tin, 13:00
        # Turf, "B" Course, 1200M, Good
        # Prize Money: $780,000, Rating: 40-0, Class 5

        info_lines = race_text.replace(race_name, '').strip().split('\n')
        assert len(info_lines) == 3
        line_1, line_2, line_3 = \
            info_lines[0].split(','), info_lines[1].split(','), info_lines[2].split(',')

        raw[Race.NAME] = race_name.split('-')[1]
        raw[Race.TIME] = to_race_time(race_date, line_1[len(line_1) - 1].strip())

        raw[Race.TRACK] = line_2[0]
        if 'Course' in line_2[1]:
            raw[Race.COURSE] = line_2[1].replace('"', '').replace('Course', '')
        if 'M' in line_2[1]:
            raw[Race.DISTANCE] = line_2[1].replace('M', '')
        if len(line_2) > 2 and 'M' in line_2[2]:
            raw[Race.DISTANCE] = line_2[2].replace('M', '')

        raw[Race.CLASS] = line_3[len(line_3) - 1]
        sub = info_lines[2][:info_lines[2].rfind(',') - 1]
        raw[Race.PRIZE] = sub[:sub.rfind(',')] \
            .replace('Prize Money:', '').replace('$', '').replace(',', '')

    @staticmethod
    def clean_one(raw: dict) -> dict:
        clean = {}

        try:
            for field, janitor in RACE_INFO_SCHEMA.items():
                if field in raw:
                    clean[field] = janitor(raw[field].strip())
                else:
                    clean[field] = None

        except Exception as ex:
            print(f'Error while cleaning:\n{raw}\n: {str(ex)}')
            raise ex

        return clean
