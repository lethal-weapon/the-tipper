from src.utils.constants import Pool
from src.robots.dual import DualOddsRobot


class QuinellaOddsRobot(DualOddsRobot):

    def get_storage_odds_type(self) -> str:
        return Pool.QIN

    def get_url_odds_type(self) -> str:
        return 'qin'
