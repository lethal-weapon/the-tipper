import os
import json
from typing import Any

from src.settings import CACHE_DIR
from src.utils.general import get_now
from src.utils.constants import QueryFile, VENUE_MAPPER
from src.utils.database import Database
from src.utils.cypher_converter import CypherConverter

SEASONS = {
    '21/22': ('2021-09-05', '2022-07-16'),
    '22/23': ('2022-09-11', '2023-07-16'),
}


class Cache:
    data: dict = {}

    @classmethod
    def initialize(cls):
        cls.read()

    @classmethod
    def read(cls):
        for f in os.listdir(CACHE_DIR):
            path = f'{CACHE_DIR}/{f}'
            if not os.path.isfile(path):
                continue
            try:
                with open(path, 'r') as infile:
                    cls.data[f] = json.loads(infile.read())
            except Exception as ex:
                print(f'Error while reading data from {path}: {ex}')

    @classmethod
    def write(cls, filename: str, content: Any):
        path = f'{CACHE_DIR}/{filename}'
        try:
            with open(path, 'w') as outfile:
                outfile.write(json.dumps(content, ensure_ascii=False))
            print(f'{filename} saved @ {get_now()}')
        except Exception as ex:
            print(f'Error while writing data to {path}: {ex}')

    @classmethod
    def get_earnings_by_season(
        cls,
        clear_cache: bool,
        person_type: str,
        season: str
    ) -> [dict]:

        slices = QueryFile.EARNINGS.split('/')
        filename = slices[-1] \
            .replace('.', f'-{person_type}-{season.replace("/", "-")}.') \
            .replace('cypher', 'json')

        if clear_cache:
            del cls.data[filename]

        if filename in cls.data:
            return cls.data[filename]

        params = {
            '$startDate': CypherConverter.to_date(SEASONS[season][0]),
            '$endDate': CypherConverter.to_date(SEASONS[season][1]),
        }
        if person_type == 'trainer':
            params['RODE'] = 'TRAINED'

        records = Database.read_from_file(QueryFile.EARNINGS, params)
        earnings = [r.data() for r in records]

        cls.data[filename] = earnings
        cls.write(filename, earnings)
        return earnings

    @classmethod
    def get_performance_by_meeting(
        cls,
        clear_cache: bool,
        person_type: str
    ) -> [dict]:

        slices = QueryFile.MEETINGS.split('/')
        filename = slices[-1] \
            .replace('.', f'-{person_type}.') \
            .replace('cypher', 'json')

        if clear_cache:
            del cls.data[filename]

        if filename in cls.data:
            return cls.data[filename]

        params = None
        if person_type == 'trainer':
            params = {'RODE': 'TRAINED'}

        records = Database.read_from_file(QueryFile.MEETINGS, params)
        performance = [r.data() for r in records]
        for p in performance:
            p['venue'] = VENUE_MAPPER[p['venue']]

        cls.data[filename] = performance
        cls.write(filename, performance)
        return performance
