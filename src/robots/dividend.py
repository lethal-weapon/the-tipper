from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.storage.storage import Storage
from src.robots.robot import Robot, RESPONSE_TIMEOUT
from src.utils.schema import *
from src.utils.constants import \
    Race, POOL_MAPPER, SINGLE_HORSE_POOLS, MULTIPLE_HORSE_POOLS

URL_DIVIDENDS = \
    'https://racing.hkjc.com/racing/information/english/Racing/ResultsAll.aspx' \
    '?RaceDate={}'

XPATH_RESULT_DIV = '//div[contains(@class, "race_result")]'


class DividendRobot(Robot):

    def run(self, race_date: str):
        url = URL_DIVIDENDS.format(race_date.replace('-', '/'))
        browser = None
        try:
            browser = self.get_browser()
            browser.get(url)
            WebDriverWait(browser, RESPONSE_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, XPATH_RESULT_DIV)))

            xpath_races = f'{XPATH_RESULT_DIV}/div'
            races = len(browser.find_elements(By.XPATH, xpath_races))

            for i in range(1, races + 1):
                xpath_result_wrapper = f'{xpath_races}[{str(i)}]'
                result_text = browser.find_element(By.XPATH, xpath_result_wrapper).text

                if 'will be' in result_text:
                    break

                xpath_dividend_table_body = \
                    f'{xpath_result_wrapper}/div[4]/div[2]/table/tbody'
                dividends = \
                    self.clean_one(self.scratch_one(browser, xpath_dividend_table_body))

                Storage.save_dividends(race_date, i, dividends)
        except:
            pass
        finally:
            if browser:
                browser.quit()
            if check_race_date(race_date):
                Storage.write(race_date)

    @staticmethod
    def scratch_one(browser, xpath_table_body: str) -> dict:
        dividends = {}
        xpath_rows = f'{xpath_table_body}/tr'
        rows = len(browser.find_elements(By.XPATH, xpath_rows))

        for i in range(1, rows + 1):
            xpath_cells = f'{xpath_rows}[{str(i)}]/td'
            pool = browser.find_element(By.XPATH, f'{xpath_cells}[1]').text
            dividend = None

            if pool in SINGLE_HORSE_POOLS:
                dividend = {}

                # 1st dividend for this pool
                horse_num = browser.find_element(By.XPATH, f'{xpath_cells}[2]').text
                horse_dividend = browser.find_element(By.XPATH, f'{xpath_cells}[3]').text
                dividend[horse_num] = horse_dividend

                # 2nd and up to 4th dividend
                for j in range(i + 1, i + 4):
                    xpath_nested_cells = f'{xpath_rows}[{str(j)}]/td'
                    nested_cells = len(browser.find_elements(By.XPATH, xpath_nested_cells))
                    if nested_cells != 2:
                        break

                    horse_num = browser.find_element(By.XPATH, f'{xpath_nested_cells}[1]').text
                    horse_dividend = browser.find_element(By.XPATH, f'{xpath_nested_cells}[2]').text
                    dividend[horse_num] = horse_dividend

            elif pool in MULTIPLE_HORSE_POOLS:
                dividend = []

                # 1st combination
                combination = browser.find_element(By.XPATH, f'{xpath_cells}[2]').text
                comb_dividend = browser.find_element(By.XPATH, f'{xpath_cells}[3]').text

                # special case: 2022-05-22 #1
                if 'REFUND' in comb_dividend:
                    continue

                dividend.append({
                    Race.COMBINATION: combination.split(','),
                    Race.DIVIDEND: comb_dividend
                })

                # 2nd and up to 6th combination for this pool
                for k in range(i + 1, i + 6):
                    xpath_nested_cells = f'{xpath_rows}[{str(k)}]/td'
                    nested_cells = len(browser.find_elements(By.XPATH, xpath_nested_cells))
                    if nested_cells != 2:
                        break

                    combination = browser.find_element(By.XPATH, f'{xpath_nested_cells}[1]').text
                    comb_dividend = browser.find_element(By.XPATH, f'{xpath_nested_cells}[2]').text
                    dividend.append({
                        Race.COMBINATION: combination.split(','),
                        Race.DIVIDEND: comb_dividend
                    })

            # finally add one pool dividend into all pools'
            if dividend:
                dividends[pool] = dividend

        return dividends

    @staticmethod
    def clean_one(raw: dict) -> dict:
        clean = {}

        for pool, pool_abbr in POOL_MAPPER.items():
            if pool not in raw:
                clean[pool_abbr] = None
                continue

            nested_dividend = raw[pool]

            if pool in SINGLE_HORSE_POOLS:
                clean[pool_abbr] = {}
                for horse_num, raw_dividend in nested_dividend.items():
                    clean[pool_abbr][horse_num] = to_odds(raw_dividend)

            elif pool in MULTIPLE_HORSE_POOLS:
                clean[pool_abbr] = []
                for comb in nested_dividend:
                    clean[pool_abbr].append({
                        Race.COMBINATION:
                            [to_int(horse_num) for horse_num in comb[Race.COMBINATION]],
                        Race.ODDS: to_odds(comb[Race.DIVIDEND])
                    })

        return clean
