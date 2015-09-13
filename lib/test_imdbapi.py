from nose.tools import assert_equal, assert_is_instance
from lib.imdbapi import search, lookup_kws, lookup_movies, lookup_movie, Movie


def test_search():
    id, title = search('Kill Bill')

    assert_equal(id, 'tt0266697')
    assert_equal(title, 'Kill Bill - Volume 1')


def test_lookup_movies():
    pass


def test_lookup_movie():
    movie = lookup_movie('tt0266697')
    assert_is_instance(movie, Movie)
    assert_equal(movie.title, 'Kill Bill: Vol. 1')
    assert len(movie.casts) > 0
    assert len(movie.directors) > 0
    assert len(movie.keywords) > 0
    assert 7 < movie.rating < 9
