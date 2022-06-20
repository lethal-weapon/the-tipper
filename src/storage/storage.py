import json

from src.storage.dummy import DUMMY
from src.utils.constants import Race, Tip


class Storage:
    data: list = []

    @classmethod
    def initialize(cls):
        cls.data = DUMMY
        # cls.print()

    @classmethod
    def print(cls):
        print(json.dumps(cls.data, sort_keys=False, indent=4))

    @classmethod
    def load_from_database(cls):
        # TODO:
        pass

    @classmethod
    def save_to_database(cls):
        # TODO:
        pass

    @classmethod
    def get_race_dates(cls) -> [str]:
        dates = [d[Race.RACE_DATE] for d in cls.data]
        dates.sort(reverse=True)
        return dates

    @classmethod
    def get_race_tuples(cls) -> [(str, int)]:
        return [
            (d[Race.RACE_DATE], d[Race.RACE_NUM]) for d in cls.data
        ]

    @classmethod
    def get_race(cls, race_date: str, race_num: int) -> dict:
        matches = list(filter(
            lambda d: d[Race.RACE_DATE] == race_date and d[Race.RACE_NUM] == race_num,
            cls.data
        ))
        if len(matches) == 1:
            return matches[0]

    @classmethod
    def get_tip(
        cls,
        race_date: str,
        race_num: int,
        source: str,
        tipster: str
    ) -> dict:
        race = cls.get_race(race_date, race_num)
        matches = list(filter(
            lambda t: t[Tip.SOURCE] == source and t[Tip.TIPSTER] == tipster,
            race[Race.TIPS]
        ))

        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise RuntimeError(f'{tipster} tips got duplicates.')

    @classmethod
    def save_tip(
        cls,
        race_date: str,
        race_num: int,
        new_tip: dict
    ):
        race = cls.get_race(race_date, race_num)
        stored = cls.get_tip(
            race_date, race_num, new_tip[Tip.SOURCE], new_tip[Tip.TIPSTER]
        )
        if stored:
            race[Race.TIPS].remove(stored)

        race[Race.TIPS].append(new_tip)
        cls.print()
