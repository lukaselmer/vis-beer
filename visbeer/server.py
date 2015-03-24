#!/usr/bin/env python

import logging
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
    try:
        ret = str(app.config.get('BeerService')(str(rfid)).status())
        logging.info('beer_rfid: Request with rfid ' + rfid + ' returns with ' + ret)
        return ret
    except Exception as e:
        logging.error('beer_rfid: An error has occurred with rfid ' + rfid)
        logging.exception(e)


@app.route('/beer/dispensed/<rfid>')
def beer_dispensed(rfid):
    try:
        ret = str(app.config.get('BeerService')(str(rfid)).dispensed())
        logging.info('beer_dispensed: Request with rfid ' + rfid + ' returns with ' + ret)
        return ret
    except Exception as e:
        logging.error('beer_dispensed: An error has occurred with rfid ' + rfid)
        logging.exception(e)


if __name__ == '__main__':
    app.run(debug=True)
