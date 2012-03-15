#!/usr/bin/python

import argparse
from pathlib import Path
import sys
import pickle
import fuse
import os

import imdbapi
from lib import filesystem, load_config, DB_FILE


def flatten(data):
    out = {}
    for d in data:
        for k, v in d.__dict__.items():
            out[k]


def mount(movies, destination):
    
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


def find_movies():
    config = load_config()

    # find imdb ids
    for movies_dir in config.directories:
        dirs = list(Path(movies_dir).glob('**/.imdb'))
        imdbs = [f.open().read() for f in dirs]

    try:
        with DB_FILE.open('rb') as fh:
            data = pickle.load(fh)
    except FileNotFoundError:
        data = {}

    movies = []
    # lookup data
    for i in imdbs:
        if i not in data:
            try:
                d = imdbapi.lookup_movie(i)
                data[i] = d
                movies.append(d)
            except Exception as e:
                print('Lookup failed for movie id:', i)
                print(e)

        else:
            movies.append(data[i])

    with DB_FILE.open('wb') as fh:
        pickle.dump(data, fh)

    return movies


def main():
    parser = argparse.ArgumentParser(description='A filesystem layer for browsing your movies')
    parser.add_argument('destination', action='store', nargs='?')
    args = parser.parse_args()

    movies = find_movies()
    mount(movies, args.destination)


if __name__ == '__main__':
    main()
