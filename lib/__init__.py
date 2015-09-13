import json
from os.path import expanduser
from pathlib import Path

config_directory = Path(expanduser('~/.config/moviedb/'))
db_file = config_directory / 'movies.db'
config_file = config_directory / 'config'

from lib.imdbapi import lookup_poster

class toobject(object):
    def __init__(self, d):
        self.__dict__ = d


def load_config():
    with config_file.open() as f:
        data = f.read()
        config = json.loads(data)
    return toobject(config)
