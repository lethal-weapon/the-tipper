import os
import pytz
from pydantic import BaseSettings
from collections import namedtuple

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
QUERY_DIR = f'{PROJECT_DIR}/src/queries'
CACHE_DIR = f'{PROJECT_DIR}/cache'
STORAGE_DIR = f'{PROJECT_DIR}/data'
SETTING_FILE = f'{PROJECT_DIR}/config/settings.env'
SETTING_FILE_ENCODING = 'UTF-8'


class AppSettings(BaseSettings):
    NAME: str = 'The Tipper'
    TIMEZONE: object = pytz.FixedOffset(480)

    class Config:
        env_prefix = ''
        env_file = SETTING_FILE
        env_file_encoding = SETTING_FILE_ENCODING


class Neo4jSettings(BaseSettings):
    URI: str = ''
    USERNAME: str = ''
    PASSWORD: str = ''
    DATABASE: str = ''

    class Config:
        env_prefix = 'NEO4J_'
        env_file = SETTING_FILE
        env_file_encoding = SETTING_FILE_ENCODING


SETTINGS = namedtuple('settings', ['APP', 'NEO4J'])(
    AppSettings(),
    Neo4jSettings(),
)
