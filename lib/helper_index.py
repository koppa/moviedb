import re

# maximum filesize to be searched for imdb ids (100kByte)
MAXSIZE = 100e3
SEARCH_ID = re.compile('imdb[\t \w\./]*(tt[0-9]+)')


def find_match(d):
    # only files and smaller 100kB
    for f in d.iterdir():
        if f.is_dir():
            yield from find_match(f)
        elif f.stat().st_size < MAXSIZE:
            yield f


def search_moviedir(directory):
    """
    Seearches a given directory for a imdb
    :param directory:
    :return:
    """
    if not directory.is_dir():
        return

    interest = find_match(directory)
    ids = []
    for f in interest:
        fh = f.open('r', errors='ignore')
        matches = [SEARCH_ID.search(l) for l in fh]
        ids.extend(m.groups()[0] for m in matches if m)

    ids = set(ids)

    if len(ids) > 1 and any([x != y for x in ids for y in ids]):
        raise Exception('Multiple different ids found', directory, ids)
        # TODO handle multiple ids

    for i in ids:
        return i