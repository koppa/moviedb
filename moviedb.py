#!/usr/bin/env python

import argparse
import pickle
import os

from pathlib import Path
from requests.exceptions import ConnectionError

from lib import load_config, db_file, imdbapi
import webservice


def mount(movies, destination):
    import fuse
    from lib import filesystem

    # raise NotImplementedError('Not implemented generating file structure')
    structure = {}
    kwds = {}
    for m in movies:
        for k in m.keywords:
            if k in kwds:
                kwds[k][m.title] = {}
            else:
                kwds[k] = {m.title: {}}
    structure['keywords'] = kwds

    if not os.path.exists(destination):
        raise Exception("Destination not existing:", destination)

    server = fuse.FUSE(filesystem.Filesystem(structure),
                       mountpoint=destination,
                       foreground=True)


def find_movies(lookup=True):
    """

    :param lookup: do lookup of movies via imdb
    :return:
    """
    config = load_config()

    # find imdb ids
    for movies_dir in config.directories:
        imdbs = [(f, f.open().read()) for f in
                 Path(movies_dir).glob('**/.imdb')]

    try:
        with db_file.open('rb') as fh:
            db = pickle.load(fh)
    except FileNotFoundError:
        db = {}

    # remove values from db which are None
    isnone = [k for k, v in db.items() if v is None]
    for k in isnone:
        db.pop(k)

    movies = {}
    # lookup data
    for f, i in imdbs:
        if i not in db:
            if not lookup:
                continue

            try:
                movie = imdbapi.lookup_movie(i)
                if movie is None:
                    continue
                db[i] = movie
            except ConnectionError:
                print("No internet connection?\nCancelling lookup.")
                break
            except Exception as e:
                print('Lookup failed for movie id:', i)

                # before quitting store database
                with db_file.open('wb') as fh:
                    pickle.dump(db, fh)

                raise e

        else:
            movie = db[i]
        movies[f.parent] = movie

    with db_file.open('wb') as fh:
        pickle.dump(db, fh)

    return movies


def main():
    parser = argparse.ArgumentParser(description='A filesystem layer for browsing your movies')
    parser.add_argument('--mount', '-m', action='store_true')
    parser.add_argument('destination', action='store', nargs='?')
    parser.add_argument('--web', '-w', action='store_true')
    parser.add_argument('--offline', '-o', action='store_true')
    args = parser.parse_args()

    movies = find_movies(lookup=not args.offline)

    if args.mount:
        mount(movies, args.destination)
    elif args.web:
        webservice.start(movies)
    else:
        print("Specifiy mount or web")


if __name__ == '__main__':
    main()
