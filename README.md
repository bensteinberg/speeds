speeds
======

This is a Flask application for serving a graph of cable modem
speeds. The data source is JSON Lines, obtained by periodically
running something like

    ./librespeed-cli --json --telemetry-level disabled' | tail -n 1 | awk '{$1=$1};1' | jq -c -M '. + {"source":"myhouse"}' >> speeds.jsonl

You can concatenate such files from multiple sources into a single
file, then specify its location in `.env` along with `FLASK_APP`:

    FLASK_APP='speeds/speeds.py'
    SPEEDS='/path/to/my/speeds.jsonl'

Once you've installed [Poetry](https://python-poetry.org/) and run

    poetry install
     
you should be able to run

    poetry run flask run
    
and see the graph at http://127.0.0.1:5000/

Tools
-----

https://github.com/librespeed/speedtest-cli

https://stedolan.github.io/jq/
