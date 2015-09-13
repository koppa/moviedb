from nose.tools import assert_equal, assert_is_instance
from lib.imdbapi import search, lookup_kws, lookup_movie, Movie, lookup_poster


def test_search():
    id, title = search('Kill Bill')

    assert_equal(id, 'tt0266697')
    assert_equal(title, 'Kill Bill - Volume 1')


def test_lookup_poster():
    id = 'tt0266697'
    poster = lookup_poster(id)


def test_lookup_movie():
    movie = lookup_movie('tt0266697')
    assert_is_instance(movie, Movie)
    assert_equal(movie.title, 'Kill Bill: Vol. 1')
    assert len(movie.casts) > 0
    assert len(movie.directors) > 0
    assert len(movie.keywords) > 0
    assert 7 < movie.rating < 9

    # movie with not enough ratings
    movie = lookup_movie('tt0978611')
    assert movie.rating is None

    movie = lookup_movie('tt3467726')
    assert movie.rating is None
