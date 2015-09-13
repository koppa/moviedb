from similarity import find_simlar, similarity_lists

def test_similarity_lists():
    a = 'abc'
    b = 'bcd'
    c = "efg"

    assert similarity_lists(a, a) == 1
    assert .5 < similarity_lists(a, b) < 1
    assert similarity_lists(a, c) == 0

def test_find_similar():
    # TODO construct movies library
    pass
