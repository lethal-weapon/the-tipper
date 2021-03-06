from datetime import time, timedelta


class Widget:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700

    INITIAL_X = 200
    INITIAL_Y = 100

    TAB_WIDTH = 200
    TAB_HEIGHT = 50


class Style:
    FILL = 'fill'
    TEXT = 'text'
    FG = 'fg'


class State:
    NORMAL = 'normal'
    DISABLE = 'disable'


class Color:
    NONE = ''
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    BLACK = 'black'
    WHITE = 'white'
    GOLD = 'gold'
    SILVER = 'silver'
    BROWN = 'brown'
    ORANGE = 'orange'


class MessageLevel:
    INFO = 'info'
    ERROR = 'error'
    SUCCESS = 'success'


class Misc:
    NULL = 'NULL'
    ORDINALS = {
        1: '1st',
        2: '2nd',
        3: '3rd',
        4: '4th',
        5: '5th',
    }


class Time:
    ONE_DAY = timedelta(days=1)
    ONE_HOUR = timedelta(hours=1)
    TWO_HOURS = timedelta(hours=2)
    SIX_AM = time(hour=6)
    ONE_PM = time(hour=13)
    ODDS_FREQUENCY_SEC = 7
    REFRESH_FREQUENCY_MS = 10000


class Race:
    RACE_DATE = 'race_date'
    RACE_NUM = 'race_num'
    TIME = 'time'
    NAME = 'name'
    VENUE = 'venue'
    CLASS = 'class'
    DISTANCE = 'distance'
    TRACK = 'track'
    COURSE = 'course'
    PRIZE = 'prize'
    VIDEO_URL = 'video_url'
    RESULT_URL = 'result_url'

    TIPS = 'tips'
    ODDS = 'odds'
    POOLS = 'pools'
    DIVIDEND = 'dividend'
    DIVIDENDS = 'dividends'
    COMBINATION = 'combination'


class Tip:
    SOURCE = 'source'
    TIPSTER = 'tipster'
    TIP = 'tip'
    CONFIDENT = 'confident'


class Pool:
    WIN = 'WIN'
    PLA = 'PLA'
    QIN = 'QIN'
    QPL = 'QPL'
    FCT = 'FCT'
    TRI = 'TRI'
    TCE = 'TCE'
    F_F = 'F-F'
    QTT = 'QTT'
    DBL = 'DBL'

    WIN_PLA = 'WIN_PLA'


POOL_MAPPER = {
    'WIN': Pool.WIN,
    'PLACE': Pool.PLA,
    'QUINELLA': Pool.QIN,
    'QUINELLA PLACE': Pool.QPL,
    'FORECAST': Pool.FCT,
    'TRIO': Pool.TRI,
    'TIERCE': Pool.TCE,
    'FIRST 4': Pool.F_F,
    'QUARTET': Pool.QTT,
}

SINGLE_HORSE_POOLS = [
    'WIN',
    'PLACE',
]

MULTIPLE_HORSE_POOLS = [
    'QUINELLA',
    'QUINELLA PLACE',
    'FORECAST',
    'TRIO',
    'TIERCE',
    'FIRST 4',
    'QUARTET',
]
