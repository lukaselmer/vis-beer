#!/usr/bin/env python

from flask import Flask
from visbeer.services.beer_service import BeerService

app = Flask(__name__)
app.config.from_object(__name__)

# set as config, so we can use dependency injection for the tests
app.config['BeerService'] = BeerService

@app.route('/')
def index():
    return 'api online'


@app.route('/beer/status/<rfid>')
def beer_rfid(rfid):
    return app.config.get('BeerService')(rfid).status()


@app.route('/beer/dispensed/<rfid>')
def beer_dispensed(rfid):
    return app.config.get('BeerService')(rfid).dispensed()


if __name__ == '__main__':
    app.run(debug=True)
