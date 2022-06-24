import re
from datetime import datetime, date


def check_str(text: str):
    return text and len(text) > 0


def check_positive_int(num: int):
    return num and num > 0


def check_bool(value: bool):
    return value is not None


def check_list(lst: list):
    return lst and len(lst) > 0


def check_horse_num(horse_num: int):
    return horse_num and horse_num > 0


def check_race_num(race_num: int):
    return 1 <= race_num <= 11


def check_race_date(race_date: str):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    match = re.search(pattern, race_date)
    if match:
        try:
            tokens = [int(token) for token in race_date.split('-')]
            year, month, day = tokens[0], tokens[1], tokens[2]
            if year >= 1900 and date(year, month, day):
                return True
        except:
            return False

    return False


def check_datetime_str(dt: str):
    # e.g. '2022-03-29T10:10:12+08:00'
    # e.g. '2022-03-29T10:10:12.069706+08:00'
    try:
        datetime.fromisoformat(dt)
        return True
    except:
        return False


def are_all_fields_exist_and_valid(data: dict,
                                   validation_schema: dict):
    for field, validator in validation_schema.items():
        if not (field in data and validator(data[field])):
            return False

    return True
