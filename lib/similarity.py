import numpy as np

def similarity_lists(list1, list2):
    """ Calculate similarity of 2 lists """
    set1, set2 = set(list1), set(list2)
    return len(set1.intersection(set2)) / len(set1.union(list2))


def calc_similarity(m1, m2):
    """

    :param m1:
    :param m2:
    :return:
    """
    score = [
        similarity_lists(m1.directors, m2.directors),
        similarity_lists(m1.casts, m2.casts),
        similarity_lists(m1.keywords, m2.keywords),
        # 1 if m1.genre == m2.genre else 0,
        # min(1 - abs(m1.year - m2.year) / 10, 0)
    ]

    return np.average(score)


def find_similar(movie, movies, N=5):
    """ finds the most similar movies

    Uses a simliarity score based on:
    * director
    * actors
    * keywords
    * year
    * genre

    Returns:
        [(movie, similarity)]
    """
    scores = [(m, calc_similarity(movie, m)) for m in movies if m != movie]
    scores = sorted(scores, key=lambda x: x[1])
    return scores[:-N:-1]
