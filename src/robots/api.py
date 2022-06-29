from abc import ABC, abstractmethod

from src.storage.storage import Storage

BASE_URL = 'https://bet.hkjc.com/racing/getJSON.aspx?'


class APIRobot(ABC):

    def run(
        self,
        race_date: str,
        race_num: str,
        venue_code: str
    ):
        robot_prefix = self.get_robot_prefix()
        url = self.build_request_url(race_date, race_num, venue_code)

        try:
            if 'Odds' in robot_prefix:
                Storage.save_odds(
                    race_date,
                    int(race_num),
                    self.get_storage_odds_type(),
                    self.fetch(url)
                )
            else:
                Storage.save_pools(
                    race_date,
                    int(race_num),
                    self.fetch(url)
                )
        except:
            pass

    def get_robot_prefix(self) -> str:
        return self.__class__.__name__.replace('Robot', '')

    @abstractmethod
    def get_storage_odds_type(self) -> str:
        pass

    @abstractmethod
    def build_request_url(
        self,
        race_date: str,
        race_num: str,
        venue_code: str
    ) -> str:
        pass

    def fetch(self, url: str) -> dict:
        """ A wrapper method for do_fetch. """
        try:
            return self.do_fetch(url)
        except Exception as ex:
            print(f'Error while fetching {self.get_robot_prefix()} '
                  f'with url `{url}`: {str(ex)}')
            raise ex

    @abstractmethod
    def do_fetch(self, url: str) -> dict:
        """ Implement the essential odds/pools processing logics. """
        pass
