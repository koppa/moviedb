import argparse
import guessit
import imdbapi
import re

from os.path import expanduser
from pathlib import Path
from lib import load_config

"""
This script annotates all movie dirs with .imdb files
in this file the id of the movies is stored.
"""

# maximum filesize to be searched for imdb ids
MAXSIZE = 100000
SEARCH_ID = re.compile('imdb[\t \w\./]*(tt[0-9]+)')


def search_moviedir(directory):
    if not directory.is_dir():
        return

    def find_match(d):
        # only files and smaller 100kB
        for f in d.iterdir():
            if f.is_dir():
                yield from find_match(f)
            elif f.stat().st_size < MAXSIZE:
                yield f

    interest = find_match(directory)
    ids = []
    for f in interest:
        fh = f.open('r', errors='ignore')
        matches = [SEARCH_ID.search(l) for l in fh]
        ids.extend(m.groups()[0] for m in matches if m)

    ids = set(ids)

    if len(ids) > 1:
        # raise Exception('Multiple ids found', directory, ids)
        # TODO handle multiple ids
        print('Multiple ids found', directory, "ignoring")

    for i in ids:
        return i


def add_movie(directory):
    """ Recognizes a movie
    Returns the imdb id
    """

    # before trying to analyse the directory name, search for a file containing a imdb id
    imdb_id = search_moviedir(directory)
    if imdb_id is not None:
        guess = guessit.guess_movie_info(directory.resolve(), info=['filename'])

        # print(guess.nice_string())
        # print("Correct (at least year and name)? (Y/n)")
        # if getch().lower() == 'n':
        #     pass

        try:
            imdb_id, _ = imdbapi.search(guess['title'], guess.get('year', ''))
        except TypeError:
            # None not iterable
            pass

        # if (len(search) == 0):
        #     search = ia.search_movie(guess['title'])

        # print("Results:")
        # for item in search:
        #     print(item['long imdb canonical title'])

        # print("Choosing first")
        # result = ia.get_movie(search[0].movieID)
        # ia.update(result, 'keywords')

    if imdb_id:
        fh = (directory / '.imdb').open('w')
        fh.write(imdb_id)
        print("Stored", directory)
    else:
        print("Error for:", directory)


def is_annotated(directory):
    return len(list(directory.glob('**/.imdb'))) > 0


def index():
    config = load_config()
    for movies_dir in config.directories:
        d = Path(expanduser(movies_dir))
        for subd in d.iterdir():
            if not is_annotated(subd):
                add_movie(subd)


def main():
    parser = argparse.ArgumentParser(description='Indexer')
    parser.add_argument('--force', action='store_true',
                        help='Force the reparsing of the movie folder')
    parser.add_argument('directory', nargs='?')
    args = parser.parse_args()

    # TODO implement force

    if args.directory:
        raise NotImplementedError()
    else:
        index()


if __name__ == '__main__':
    main()
