#!/usr/bin/env python

import argparse
from os.path import expanduser
from pathlib import Path

import guessit

from lib import load_config, imdbapi
from lib.helper_index import search_moviedir

"""
This script annotates all movie dirs with .imdb files
in this file the id of the movies is stored.
"""



def add_movie(directory, verbose=False):
    """ Recognizes a movie
    Returns the imdb id
    """

    # before trying to analyse the directory name, search for a file containing a imdb id
    imdb_id = search_moviedir(directory)
    if imdb_id is None:
        guess = guessit.guess_movie_info(directory.resolve(), info=['filename'])

        # print(guess.nice_string())
        # print("Correct (at least year and name)? (Y/n)")
        # if getch().lower() == 'n':
        #     pass
        if verbose:
            print("Directory:", directory)
            print("guess:", guess['title'], guess.get('year', ''))

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


def index(verbose=False, force=False):
    config = load_config()
    for movies_dir in config.directories:
        d = Path(expanduser(movies_dir))
        for subd in d.iterdir():
            if not is_annotated(subd) or force:
                add_movie(subd, verbose)


def main():
    parser = argparse.ArgumentParser(description='Indexer')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='')
    parser.add_argument('--force', action='store_true',
                        help='Force the reparsing of the movie folder')
    # parser.add_argument('directory', nargs='?')
    args = parser.parse_args()

    index(verbose=args.verbose, force=args.force)


if __name__ == '__main__':
    main()
