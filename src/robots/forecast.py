from src.utils.constants import Pool
from src.robots.dual import DualOddsRobot


class ForecastOddsRobot(DualOddsRobot):

    def get_storage_odds_type(self) -> str:
        return Pool.FCT

    def get_url_odds_type(self) -> str:
        return 'fct'
