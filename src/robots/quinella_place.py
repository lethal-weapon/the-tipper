from src.utils.constants import Pool
from src.robots.dual import DualOddsRobot


class QuinellaPlaceOddsRobot(DualOddsRobot):

    def get_storage_odds_type(self) -> str:
        return Pool.QPL

    def get_url_odds_type(self) -> str:
        return 'qpl'
