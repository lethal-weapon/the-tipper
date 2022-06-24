import re
from datetime import date, time, datetime

from src.settings import SETTINGS


def to_str(string: str):
    return string if len(string) > 0 else None


def to_int(int_str: str):
    if len(int_str) == 0 or int_str == '-':
        return None
    return int(int_str)


def to_bool(value: bool) -> bool:
    return value


def to_date(date_str: str) -> date:
    # e.g. '2021-12-09'
    tokens = [int(token) for token in date_str.split('-')]
    year, month, day = tokens[0], tokens[1], tokens[2]
    return date(year, month, day)


def to_race_time(race_date: str, race_time: str) -> str:
    # e.g. race_date: '2021-12-09', race_time: '12:30'
    time_slices = [int(token) for token in race_time.split(':')]
    the_date = to_date(race_date)
    the_time = time(time_slices[0], time_slices[1], 0)
    return datetime(
        the_date.year,
        the_date.month,
        the_date.day,
        the_time.hour,
        the_time.minute,
        the_time.second,
        tzinfo=SETTINGS.BASE.TIMEZONE,
    ).isoformat()


def to_race_date_num_venue(url: str) -> (str, str, str):
    # e.g. 'https://~hkjc.com~?RaceDate=2022/04/27&Racecourse=HV&RaceNo=9'
    return (
        re.search(r'\d{4}/\d{2}/\d{2}', url).group().replace('/', '-'),
        url[url.rfind('=') + 1:],
        re.search(r'=(ST|HV)', url).group().replace('=', '')
    )