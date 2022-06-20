import os
import pytz
from pydantic import BaseSettings
from collections import namedtuple

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
SETTING_FILE = f'{PROJECT_DIR}/config/settings.env'
SETTING_FILE_ENCODING = 'UTF-8'


class Settings(BaseSettings):
    APP: str = 'The Tipper'
    TIMEZONE: object = pytz.FixedOffset(480)

    class Config:
        env_prefix = ''
        env_file = SETTING_FILE
        env_file_encoding = SETTING_FILE_ENCODING


class MongoSettings(BaseSettings):
    URI: str = ''
    USERNAME: str = ''
    PASSWORD: str = ''
    DATABASE: str = ''

    class Config:
        env_prefix = 'MONGO_'
        env_file = SETTING_FILE
        env_file_encoding = SETTING_FILE_ENCODING


SETTINGS = namedtuple('settings', ['BASE', 'MONGO'])(
    Settings(),
    MongoSettings(),
)
