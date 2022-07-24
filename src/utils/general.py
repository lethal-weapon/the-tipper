import threading
from datetime import datetime, date, time

from src.settings import SETTINGS


def get_thread_name() -> str:
    return threading.current_thread().name


def get_now() -> datetime:
    return datetime.now(tz=SETTINGS.BASE.TIMEZONE)


def get_current_date() -> date:
    return datetime.date(get_now())


def get_current_date_and_time() -> (date, time):
    now = get_now()
    return datetime.date(now), datetime.time(now)
