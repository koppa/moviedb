import pickle
import requests
from lxml.etree import fromstring
from bs4 import BeautifulSoup
from collections import namedtuple

IMDB_SEARCH_API = "http://akas.imdb.com/xml/find"
IMDB_MOVIE_API = "http://akas.imdb.com/title/{}"
IMDB_KEYWORDS_API = 'http://akas.imdb.com/title/{}/keywords'

Movie = namedtuple("Movie", ['rating', 'keywords', 'casts', 'directors', 'id', 'title'])

# TODO  integrate imdb file api ftp://ftp.fu-berlin.de/pub/misc/movies/database/


def search(title, year=""):
    """ Searches for a movie
    :param title:
    :param year:
    :return: movieid, title
    """
    payload = {'xml': "1", 'nr': "1", 'tt': 'on', 'q':title + " " + str(year)}

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
    rating = float(soup.select('div.titlePageSprite')[0].text.strip())
    keywords = lookup_kws(id)

    # only important roles in cast
    casts = [e.text for e in soup.select('table.cast_list span.itemprop')]
    directors = [e.text for e in soup.select('[itemprop="director"] a')]

    return Movie(id=id, title=title, rating=rating, keywords=keywords, casts=casts, directors=directors)


def lookup_kws(id):
    r = requests.get(IMDB_KEYWORDS_API.format(id))
    soup = BeautifulSoup(r.text, 'lxml')
    return [e.attrs['data-item-keyword'] for e in soup.select('#keywords_content .soda.sodavote')]


def lookup_movies(movies):
    fh = open(TARGET + '/store.pickle', 'rb')
    db = pickle.load(fh)
    for cat, val in db.items():
        db[cat] = {k: set(v) & set(movies) for k, v in val.items() if set(v) & set(movies)}
    import pdb; pdb.set_trace()
    return db
