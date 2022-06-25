class Widget:
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = WINDOW_WIDTH * 5 // 8

    INITIAL_X = 400
    INITIAL_Y = 250

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
    DIVIDENDS = 'dividends'


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
    QIN_QPL = 'QIN_QPL '
    FCT_TRI = 'FCT_TRI'
    QTT_F_F = 'QTT_F-F'
