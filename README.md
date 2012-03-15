MovieDb
=======

A great tool for browsing your Movies via a fuse filesystem.

It automatically recognizes your movies, and adds it to your database

Dependencies:
* python2
* imdbpy  http://imdbpy.sourceforge.net/
* guessit http://pypi.python.org/pypi/guessit

Usage
-----
for Starting the filesystem execute

    moviedb mount "mountpoint"

for indexing your movies

    moviedb index

It should guide you through the process, and automatically finds new movies


Configuration
-----------------

You have to create the directory "~/.config/moviedb/"

And save a configuration File in "~/.config/moviedb/config"

example configuration file(json fileformat)

    {
        "directories": [
            "/media/filme"
        ],
        "database": "~/.config/moviedb/database"
    }

The database file will be automatically created
