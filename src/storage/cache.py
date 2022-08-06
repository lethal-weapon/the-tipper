import os
import json
from typing import Any

from src.settings import CACHE_DIR
from src.utils.general import get_now
from src.utils.constants import QueryFile
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
                outfile.write(json.dumps(content))
            print(f'{filename} saved @ {get_now()}')
        except Exception as ex:
            print(f'Error while writing data to {path}: {ex}')

    @classmethod
    def get_jockey_earnings_by_season(cls, season: str) -> [dict]:
        slices = QueryFile.JOCKEY_EARNING.split('/')
        filename = slices[-1] \
            .replace('.', f'-{season.replace("/", "-")}.') \
            .replace('cypher', 'json')

        if filename in cls.data:
            return cls.data[filename]

        params = {
            '$startDate': CypherConverter.to_date(SEASONS[season][0]),
            '$endDate': CypherConverter.to_date(SEASONS[season][1]),
        }
        records = Database.read_from_file(
            QueryFile.JOCKEY_EARNING,
            params
        )
        earnings = [r.data() for r in records]

        cls.data[filename] = earnings
        cls.write(filename, earnings)
        return earnings
