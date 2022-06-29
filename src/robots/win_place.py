import re
import requests

from src.utils.constants import Pool
from src.robots.api import APIRobot, BASE_URL

URL_PARAMS = 'type=winplaodds&date={}&venue={}&start={}&end={}'

WIN_SPLITOR = '@@@WIN;'
PLACE_SPLITOR = '#PLA;'
HORSE_SPLITOR = re.compile(r'=\d;')


class WinPlaceOddsRobot(APIRobot):

    def get_storage_odds_type(self) -> str:
        return Pool.WIN_PLA

    def build_request_url(
        self,
        race_date: str,
        race_num: str,
        venue_code: str
    ) -> str:
        params = URL_PARAMS.format(race_date, venue_code, race_num, race_num)
        return f'{BASE_URL}{params}'

    def do_fetch(self, url: str) -> dict:
        odds = {}
        res = requests.get(url).text.strip()
        # response sample:
        # {"OUT":"165736@@@WIN;1=7.6=0;2=11=0;3=7.2=0;4=12=0;5=5.9=1;
        # 6=16=0;7=26=0;8=6.6=0;9=27=0;10=6.3=0;11=39=0;12=7.4=0
        # #PLA;1=3.3=0;2=3.8=0;3=2.3=0;4=3.4=0;5=2.0=1;6=4.2=0;
        # 7=5.9=0;8=3.4=0;9=6.5=0;10=2.0=0;11=7.4=0;12=2.6=0"}

        # remove the prefix and suffix
        res = res[res.find(WIN_SPLITOR) + len(WIN_SPLITOR):]
        res = res[:res.rfind('"')]

        # split into WIN and PLACE groups
        groups = res.split(PLACE_SPLITOR)
        assert len(groups) == 2

        wins, places = groups[0], groups[1]
        wins, places = \
            wins[:wins.rfind('=')], places[:places.rfind('=')]
        wins, places = \
            HORSE_SPLITOR.split(wins), HORSE_SPLITOR.split(places)
        assert len(wins) == len(places)

        # wins and places should look like:
        # ['1=7.6', '2=11', '3=7.2', '4=12', '5=5.9', '6=16', '7=26']
        # ['1=3.3', '2=3.8', '3=2.3', '4=3.4', '5=2.0', '6=4.2', '7=5.9']

        # construct the payload
        for i in range(len(wins)):
            win_pair, place_pair = \
                wins[i].split('='), places[i].split('=')
            assert len(win_pair) == len(place_pair) == 2

            win_horse_num, win_odds, place_horse_num, place_odds = \
                win_pair[0], win_pair[1], place_pair[0], place_pair[1]
            assert win_horse_num == place_horse_num

            # withdrawn horses don't have odds, excluded
            if 'SCR' in win_odds:
                continue

            odds[win_horse_num] = [float(win_odds), float(place_odds)]

        return odds
