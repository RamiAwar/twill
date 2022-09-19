import os
from pathlib import Path

DEFAULT_ENV = 'dev'
DEFAULT_DATA_PATH = './data'


def get_env():
    return os.environ.get('ENV', DEFAULT_ENV)

def get_data_path():
    path = os.environ.get('DATA_PATH', DEFAULT_DATA_PATH)
    return Path(path)