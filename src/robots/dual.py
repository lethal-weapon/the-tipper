import re
import requests
from abc import ABC, abstractmethod

from src.robots.api import APIRobot, BASE_URL

URL_PARAMS = 'type={}&date={}&venue={}&raceno={}'

RESPONSE_PREFIX = '@@@;'
PAIR_SPLITOR = re.compile(r'=\d;')
ERROR_PATTERNS = [
    r'=---=',
]


class DualOddsRobot(APIRobot, ABC):

    def build_request_url(
        self,
        race_date: str,
        race_num: str,
        venue_code: str
    ) -> str:
        params = URL_PARAMS.format(
            self.get_url_odds_type(), race_date, venue_code, race_num
        )
        return f'{BASE_URL}{params}'

    @abstractmethod
    def get_url_odds_type(self) -> str:
        pass

    def do_fetch(self, url: str) -> dict:
        odds = {}
        res = requests.get(url).text.strip()
        # response sample (QIN):
        # {"OUT":"172437@@@;
        # 1-2=37=0;1-3=23=0;1-4=47=0;1-5=27=0;1-6=24=0;1-7=26=0;
        # 2-3=27=0;2-4=45=0;2-5=16=0;2-6=23=0;2-7=26=0;
        # 3-4=16=0;3-5=12=0;3-6=5.2=1;3-7=11=0;
        # 4-5=25=0;4-6=22=0;4-7=38=0;
        # 5-6=10=0;5-7=20=0;
        # 6-7=7.9=0"}

        # remove the prefix and suffix
        res = res[res.find(RESPONSE_PREFIX) + len(RESPONSE_PREFIX):]
        res = res[:res.rfind('=')]

        # check for any errors before proceeding
        for pattern in ERROR_PATTERNS:
            if re.search(pattern, res):
                return odds

        pairs = PAIR_SPLITOR.split(res)
        # pairs should look like:
        # ['1-2=37', '1-3=23', '1-4=47', '1-5=27', '1-6=24', '1-7=26', '2-3=27',
        # '2-4=45', '2-5=16', '2-6=23', '2-7=26', '3-4=16', '3-5=12', '3-6=5.2',
        # '3-7=11', '4-5=25', '4-6=22', '4-7=38', '5-6=10', '5-7=20', '6-7=7.9']

        for pair in pairs:
            # skip the withdrawn horse cases
            if 'SCR' in pair or pair.endswith('='):
                continue

            slices = pair.split('=')
            assert len(slices) == 2

            dual_nums, dual_odds = slices[0], float(slices[1])
            dual_nums = dual_nums.split('-')
            assert len(dual_nums) == 2

            horse_1_num, horse_2_num = dual_nums[0], dual_nums[1]
            if horse_1_num in odds:
                odds[horse_1_num][horse_2_num] = dual_odds
            else:
                odds[horse_1_num] = {horse_2_num: dual_odds}

        return odds
