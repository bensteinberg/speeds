speeds
======

This is a Flask application for serving a graph of cable modem
speeds. The data source is [JSON Lines](https://jsonlines.org/),
obtained by periodically running something like

    ./librespeed-cli --json --telemetry-level disabled' | tail -n 1 | awk '{$1=$1};1' | jq -c -M '. + {"source":"myhouse"}' >> speeds.jsonl

(You may want to specify what server `librespeed-cli` should use with
`--server <x>` where the ID comes from `./librespeed-cli --list`, so
you're not measuring apples and oranges. Note that setting the server
in a cron job is fragile, should the list of servers change.)

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
an integer in the URL to see a different range.

Tools
-----

https://github.com/librespeed/speedtest-cli

https://stedolan.github.io/jq/
