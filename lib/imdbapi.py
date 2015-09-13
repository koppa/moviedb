import requests

from lxml.etree import fromstring
from bs4 import BeautifulSoup
from collections import namedtuple
from lib import config_directory

IMDB_SEARCH_API = "http://akas.imdb.com/xml/find"
IMDB_MOVIE_API = "http://akas.imdb.com/title/{}"
IMDB_KEYWORDS_API = 'http://akas.imdb.com/title/{}/keywords'


class Movie(object):
    fields = {'rating', 'keywords', 'casts', 'directors', 'id', 'title'}

    def __init__(self, **kwargs):
        if set(kwargs.keys()) != self.fields:
            raise Exception("Fields are: {}\nExpected fields: {}".format(kwargs.keys(), self.fields))
        print(kwargs)
        self.__dict__ = kwargs

    def get_poster(self):
        directory = config_directory / 'posters'
        if not directory.exists():
            directory.mkdir()

        file = directory / '{}.jpg'.format(self.id)

        if not file.exists():
            content = lookup_poster(self.id)
            with file.open('wb') as fh:
                fh.write(content)
        return file.open('rb')

    def __repr__(self):
        return repr(self.__dict__)


# TODO  integrate imdb file api ftp://ftp.fu-berlin.de/pub/misc/movies/database/


def search(title, year=None):
    """ Searches for a movie
    :param title:
    :param year:
    :return: movieid, title
    """
    query = ("{0} ({1})".format(title, year) if year else title)
    payload = {'xml': "1", 'nr': "1", 'tt': 'on', 'q': query}

    r = requests.get(IMDB_SEARCH_API, params=payload)
    document = fromstring(r.content)
    root = document.getroottree()

    # get first movie
    try:
        result = root.xpath('.//ImdbEntity')[0]
        return result.get('id'), result.text
    except IndexError:
        return None


def lookup_movie(id):
    """ Aggregate movie information via various sources

    :param id:
    :return:
    """
    r = requests.get(IMDB_MOVIE_API.format(id))
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.select('h1.header span.itemprop')[0].text.strip()

    if len(soup.select('div.rating-ineligible')):
        print(id, "not a real movie")
        print('Not released?')
        return

    try:
        rating = float(soup.select('div.titlePageSprite')[0].text.strip())
    except Exception as e:
        # Probably not enough ratings available
        rating = None

    keywords = lookup_kws(id)

    # only important roles in cast
    casts = [e.text for e in soup.select('table.cast_list span.itemprop')]
    directors = [e.text for e in soup.select('[itemprop="director"] a')]

    return Movie(id=id, title=title, rating=rating, keywords=keywords, casts=casts, directors=directors)


def lookup_kws(id):
    r = requests.get(IMDB_KEYWORDS_API.format(id))
    soup = BeautifulSoup(r.text, 'lxml')
    return [e.attrs['data-item-keyword'] for e in soup.select('#keywords_content .soda.sodavote')]


OMDB_API = 'http://www.omdbapi.com/'


def lookup_poster(id):
    payload = {"r": "json",
               "i": id}
    r = requests.get(OMDB_API, params=payload)
    doc = r.json()
    posterurl = doc['Poster']
    img = requests.get(posterurl)
    return img.content
