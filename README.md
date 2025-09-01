speeds
======

This is a Flask application for serving a graph of cable modem
speeds. The data source is [JSON Lines](https://jsonlines.org/),
obtained by periodically running something like

    ./speedtest-go --json | tail -n 1 | awk '{$1=$1};1' | jq -c -M '. + {"source":"myhouse"}' >> speeds.jsonl

(A previous version of this system used [librespeed-cli](https://github.com/librespeed/speedtest-cli) and specified the server; this lets `speedtest-go` figure out which server to use.)

You can concatenate such files from multiple sources into a single
file, then specify its location in `.env` along with `FLASK_APP`:

    FLASK_APP='speeds/speeds.py'
    SPEEDS='/path/to/my/speeds.jsonl'

Once you've installed [Poetry](https://python-poetry.org/) and run

    poetry install
     
you should be able to run

    poetry run flask run
    
and see the graph at http://127.0.0.1:5000/

It defaults to showing one month of data, but you can use `all` or
an integer in the URL to see a different number of months, or a range
of dates in the form `YYYYMMDD-YYYYMMDD`.

Tools
-----

https://github.com/showwin/speedtest-go

https://stedolan.github.io/jq/
