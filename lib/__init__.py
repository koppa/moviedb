import json
from os.path import expanduser
from pathlib import Path

DB_FILE = Path(expanduser('~/.config/moviedb/movies.db'))
CONFIG_FILE = Path(expanduser('~/.config/moviedb/config'))


class toobject(object):
    def __init__(self, d):
        self.__dict__ = d


def load_config():
    with CONFIG_FILE.open() as f:
        data = f.read()
        config = json.loads(data)
    return toobject(config)
