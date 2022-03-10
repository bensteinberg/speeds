from flask import Flask, render_template
import jsonlines
import os
from datetime import datetime, timedelta


app = Flask(__name__)


@app.route('/')
@app.route('/<months>')
def speeds(months='1'):
    with jsonlines.open(os.environ.get('SPEEDS', 'speeds.jsonl')) as reader:
        if months == 'all':
            objects = [o for o in reader]
        else:
            now = datetime.now()
            try:
                then = timedelta(int(months) * 365 / 12)
            except ValueError:
                return 'Bad parameter, use "all" or an integer', 400
            objects = [o for o in reader if
                       now - datetime.strptime(o['timestamp'][:26],
                                               '%Y-%m-%dT%H:%M:%S.%f')
                       < then]

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
