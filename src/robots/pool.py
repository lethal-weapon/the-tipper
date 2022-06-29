import requests

from src.utils.constants import Race
from src.robots.api import APIRobot, BASE_URL

URL_PARAMS = 'type=pooltot&date={}&venue={}&raceno={}'


class PoolRobot(APIRobot):

    def get_storage_odds_type(self) -> str:
        return Race.POOLS

    def build_request_url(
        self,
        race_date: str,
        race_num: str,
        venue_code: str
    ) -> str:
        params = URL_PARAMS.format(race_date, venue_code, race_num)
        return f'{BASE_URL}{params}'

    def do_fetch(self, url: str) -> dict:
        pools = {}
        try:
            res = requests.get(url).json()
        except:
            raise RuntimeError('HKJC response is not in JSON')

        # response sample:
        # {"inv":[
        # {"pool":"WIN","value":"526054"},{"pool":"PLA","value":"404441"},
        # {"pool":"QIN","value":"440711"},{"pool":"QPL","value":"596966"},
        # {"pool":"TCE","value":"41466"},
        # {"pool":"FCT","value":"90655","pid":"90462"},
        # {"pool":"TRI","value":"90655","pid":"90462"},
        # {"pool":"F-F","value":"66127","pid":"90461"},
        # {"pool":"QTT","value":"66127","pid":"90461"},
        # {"pool":"DBL","value":"80520"}
        # ], "totalInv":"10172995","updateTime":"153427"}

        for inv in res['inv']:
            pools[inv['pool']] = int(inv['value'])

        return pools
