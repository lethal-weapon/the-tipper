from datetime import time, timedelta

from src.settings import QUERY_DIR


class Widget:
    WINDOW_WIDTH = 1360
    WINDOW_HEIGHT = 880

    INITIAL_X = 1
    INITIAL_Y = 0

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


class QueryFile:
    EARNINGS = f'{QUERY_DIR}/earnings.cypher'
    MEETINGS = f'{QUERY_DIR}/meetings.cypher'


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

VENUE_MAPPER = {
    '沙田': 'ST',
    '跑馬地': 'HV',
}

IGNORED_PEOPLE = [
    'D. Ferraris',
    'D. Moor',
    'C. Schofield',
    'T. Piccone',
    'Y. Kawada',
    'D. Lane',
    'R. Moore',
    'T. Marquand',
]

JOCKEY_RANKINGS = [
    'Z. Purton',
    'J. Moreira',
    'K. Teetan',
    'S. DeSousa',
    'A. Badel',
    'V. Ho',
    'M. Chadwick',
    'M. Poon',
    'D. Leung',
    'R. Maia',
    'L. Ferraris',
    'L. Hewitson',
    'L. Currie',
    'H. Bentley',
    'A. Hamelin',
    'V. Borges',
    'J. Chau',
    'A. Chung',
    'K. Yeung',
    'D. Mo',
    'V. Wong',
    'J. Wong',
    'A. Chan',
    'A. Lai',
]

TRAINER_RANKINGS = [
    'F. Lor',
    'J. Size',
    'T. Cruz',
    'D. Whyte',
    'R. Yiu',
    'F. Lui',
    'C. Fownes',
    'D. Shum',
    'D. Hall',
    'D. Hayes',
    'B. Yung',
    'C. So',
    'M. Man',
    'J. Ting',
    'D. Yip',
    'P. Ng',
    'J. Richards',
    'R. Gibson',
    'T. Millard',
    'M. Chang',
    'M. Tsui',
    'P. Ho',
]
