from subprocess import call
from collections import Counter

from flask import Flask, render_template, send_file, request
from lib.similarity import find_similar

app = Flask(__name__)


def find_movie(id):
    return [m for m in movies.values() if m.id == id][0]


@app.route('/kw')
def kw():
    kws = [w for m in movies.values() for w in m.keywords]
    count = Counter(kws)
    count = [(k, i) for k, i in count.items() if i > 1]
    count = sorted(count, key=lambda x: x[1])[::-1][:200]
    return render_template('kw_overview.html', kws=count)


@app.route('/')
@app.route('/filter/<key>=<value>')
def filter_movies(sort='title', key=None, value=None):
    ms = movies.values()
    # for k, v in request.args.items():
    if key in ['keywords']:
        ms = [m for m in ms if value in m.__dict__[key]]
    elif key is not None:
        ms = [m for m in ms if m.__dict__[key] == value]

    # sort
    ms = sorted(ms, key=lambda x: x.__dict__[sort])
    return render_template('gallery.html', movies=ms)


@app.route('/poster/<id>.jpg')
def poster(id):
    m = find_movie(id)
    content = m.get_poster()
    return send_file(content, mimetype='image/gif')


@app.route('/open/<id>')
def open_directory(id):
    for f, m in movies.items():
        if m.id == id:
            break
    call(['dolphin', str(f)])


@app.route('/movie/<id>/rename', methods=['POST'])
def rename():
    raise Exception("Not implemented!")


@app.route('/movie/<id>')
def movie(id):
    m = find_movie(id)
    return render_template("movie.html", movie=m,
                           similar=find_similar(m, movies.values()))


def start(_movies):
    global movies
    movies = _movies
    app.run(debug=True)
