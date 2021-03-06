import os
import json
from typing import Optional

from src.settings import STORAGE_DIR
from src.utils.constants import Race, Tip
from src.utils.general import get_now


class Storage:
    data: list = []

    @classmethod
    def initialize(cls):
        cls.read()

    @classmethod
    def print(cls):
        print(json.dumps(cls.data, sort_keys=False, indent=4))

    @classmethod
    def read(cls):
        for f in os.listdir(STORAGE_DIR):
            path = f'{STORAGE_DIR}/{f}'
            if not os.path.isfile(path):
                continue
            try:
                with open(path, 'r') as infile:
                    cls.data.extend(json.loads(infile.read()))
            except Exception as ex:
                print(f'Error while reading data from {path}: {ex}')

    @classmethod
    def write(cls, race_date: str):
        path = f'{STORAGE_DIR}/{race_date}.json'
        matches = list(filter(
            lambda d: d[Race.RACE_DATE] == race_date, cls.data
        ))

        try:
            with open(path, 'w') as outfile:
                outfile.write(json.dumps(matches))
            print(f'Meeting {race_date} saved @ {get_now()}')
        except Exception as ex:
            print(f'Error while writing data to {path}: {ex}')

    @classmethod
    def save_race(cls, new_race: dict):
        new_date, new_num = new_race[Race.RACE_DATE], new_race[Race.RACE_NUM]
        stored = cls.get_race(new_date, new_num)

        if stored:
            for extra_field in [Race.TIPS, Race.ODDS, Race.POOLS, Race.DIVIDENDS]:
                new_race[extra_field] = stored[extra_field]
            cls.data.remove(stored)
        else:
            new_race[Race.TIPS] = []
            new_race[Race.ODDS] = {}
            new_race[Race.POOLS] = {}
            new_race[Race.DIVIDENDS] = {}

        cls.data.append(new_race)
        print(f'Racecard <{new_date}, {new_num}> saved')

    @classmethod
    def save_dividends(
        cls,
        race_date: str,
        race_num: int,
        dividends: dict
    ):
        stored = cls.get_race(race_date, race_num)
        if stored:
            stored[Race.DIVIDENDS] = dividends
            print(f'Dividend <{race_date}, {race_num}> saved')
        else:
            print(f'Racecard <{race_date}, {race_num}> does not exist')

    @classmethod
    def save_odds(
        cls,
        race_date: str,
        race_num: int,
        odds_type: str,
        odds_value: dict
    ):
        stored = cls.get_race(race_date, race_num)
        if stored:
            stored[Race.ODDS][odds_type] = odds_value
            # print(f'{odds_type} <{race_date}, {race_num}> saved')
        else:
            print(f'Racecard <{race_date}, {race_num}> does not exist')

    @classmethod
    def save_pools(
        cls,
        race_date: str,
        race_num: int,
        pools: dict
    ):
        stored = cls.get_race(race_date, race_num)
        if stored:
            stored[Race.POOLS] = pools
            print(f'Pool <{race_date}, {race_num}> saved')
        else:
            print(f'Racecard <{race_date}, {race_num}> does not exist')

    @classmethod
    def is_empty(cls) -> bool:
        return len(cls.data) == 0

    @classmethod
    def get_most_recent_race_date(cls) -> str:
        return cls.get_race_dates()[0]

    @classmethod
    def get_race_dates(cls) -> [str]:
        dates = []
        for d in cls.data:
            if d[Race.RACE_DATE] not in dates:
                dates.append(d[Race.RACE_DATE])

        dates.sort(reverse=True)
        return dates

    @classmethod
    def get_race_tuples(cls) -> [(str, int)]:
        return [
            (d[Race.RACE_DATE], d[Race.RACE_NUM]) for d in cls.data
        ]

    @classmethod
    def get_race(
        cls,
        race_date: str,
        race_num: int
    ) -> dict:
        matches = list(filter(
            lambda d: d[Race.RACE_DATE] == race_date and d[Race.RACE_NUM] == race_num,
            cls.data
        ))
        if len(matches) == 1:
            return matches[0]

    @classmethod
    def get_race_date_and_num_count(cls, n: Optional[int] = 3) -> dict:
        """
        Return up to the most recent n race days
        and the total races for each one of them.
        """
        races = {d: 0 for d in cls.get_race_dates()[:n]}

        for (race_date, race_num) in cls.get_race_tuples():
            if race_date in races and race_num > races[race_date]:
                races[race_date] = race_num

        return races

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
        cls.write(race_date)
