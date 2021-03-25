from flask import Flask, render_template
import jsonlines
import os


app = Flask(__name__)


@app.route('/')
def speeds():
    with jsonlines.open(os.environ.get('SPEEDS', 'speeds.jsonl')) as reader:
        objects = [o for o in reader]

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
