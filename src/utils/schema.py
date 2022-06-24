from src.utils.checkers import *
from src.utils.converters import *
from src.utils.constants import Race

# crawler side
RACE_INFO_SCHEMA = {
    Race.RACE_DATE: to_str,
    Race.RACE_NUM: to_int,
    Race.TIME: to_str,
    Race.NAME: to_str,
    Race.VENUE: to_str,
    Race.CLASS: to_str,
    Race.DISTANCE: to_int,
    Race.TRACK: to_str,
    Race.COURSE: to_str,
    Race.PRIZE: to_int,
}

RACE_INFO_VALIDATION_SCHEMA = {
    Race.RACE_DATE: check_race_date,
    Race.RACE_NUM: check_race_num,
    Race.TIME: check_datetime_str,
    Race.NAME: check_str,
    Race.VENUE: check_str,
    Race.CLASS: check_str,
    Race.DISTANCE: check_positive_int,
    Race.TRACK: check_str,
    Race.PRIZE: check_positive_int,
}
