MovieDb
=======

A great tool for browsing your Movies via a fuse filesystem.

It automatically recognizes your movies, and adds it to your database

Dependencies:
* python
* imdbpy  http://imdbpy.sourceforge.net/
* guessit http://pypi.python.org/pypi/guessit

Usage
-----

First create a config:

###Configuration

You have to create the directory "~/.config/moviedb/"

And save a configuration File in "~/.config/moviedb/config"

example configuration file(json fileformat)

    {
        "directories": [
            "/media/filme"
        ]
    }

The database file will be automatically created


Automatically index your movies.
It tries to heuristically determine the correct movie.
Then the imdb-id is stored in the file '.imdb' for each movie.

    moviedb_index

for Starting the filesystem execute

    moviedb -m "mountpoint"

Or use the web interface

    moviedb -w


TODO
----
* Add person to the database
* create a good ui design
* backend 
    * improve guessit performance by using the full path to the video file
    * More stable parser for videos
        * Support directories with multiple movies
            * Needed extension of .imdb format  
          multiple movies per film, or marks for movie groups
    * integrate themoviedb <https://www.themoviedb.org/> <http://docs.themoviedb.apiary.io/#>
      use stolen api key from github
* frontend
    * Integrate a way to correct wrong movie classifications
    * Remove or update fuse filesystem