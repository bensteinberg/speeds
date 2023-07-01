from flask import Flask, render_template, g, abort
import jsonlines
import os
from datetime import datetime, timedelta


app = Flask(__name__)


def get_reader():
    if 'reader' not in g:
        g.reader = jsonlines.open(os.environ.get('SPEEDS', 'speeds.jsonl'))

    return g.reader


@app.teardown_appcontext
def teardown_reader(exception):
    reader = g.pop('reader', None)

    if reader is not None:
        reader.close()


@app.route('/all')
def all():
    reader = get_reader()
    objects = [o for o in reader]
    return graph(objects)


@app.route('/')
@app.route('/<int:months>')
def speeds(months=1):
    reader = get_reader()
    now = datetime.now()
    then = timedelta(months * 365 / 12)
    objects = [o for o in reader if
               now - ts_dt(o['timestamp']) < then]

    return graph(objects)


@app.route('/<int:start>-<int:end>')
def interval(start, end):
    reader = get_reader()
    try:
        s = datetime.strptime(str(start), '%Y%m%d')
        e = datetime.strptime(str(end), '%Y%m%d')
    except ValueError:
        abort(400, description='Dates in range must be formatted YYYYMMDD')
    if e < s:
        abort(400,
              description='Start of range must be less than or equal to end')
    objects = [o for o in reader if
               s <= ts_dt(o['timestamp']) and
               e >= ts_dt(o['timestamp'])]

    return graph(objects)


def graph(objects):
    """ Produce output """
    locations = set([o['source'] for o in objects])
    output = {}
    colors = {}
    # we need as many pairs as we have locations; some kind of
    # generator would be better.
    palette = [
        ('red', 'pink'),
        ('blue', 'lightblue'),
        ('black', 'gray'),
    ]
    assert len(locations) < len(palette), 'Not enough color pairs'
    for idx, loc in enumerate(locations):
        colors[loc] = {'download': palette[idx][0],
                       'upload': palette[idx][1]}
        output[loc] = [o for o in objects if o['source'] == loc]
    return render_template('index.html', objects=output, colors=colors)


def ts_dt(ts):
    return datetime.strptime(ts[:25], '%Y-%m-%dT%H:%M:%S.%f')
