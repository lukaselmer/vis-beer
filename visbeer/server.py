#!/usr/bin/env python

import logging
from flask import Flask, request, abort
from functools import wraps
from visbeer.services.beer_service import BeerService


# TODO: move this to a config file
API_KEY = 'llxPd3Krm2y4dLMa5YGCkLumvx0Mb1DZaZiPH'

app = Flask(__name__)
app.config.from_object(__name__)

# set as config, so we can use dependency injection for the tests
app.config['BeerService'] = BeerService


def get_api_key():
    return API_KEY


def require_api_key(view_function):
    # the new, post-decoration function. Note *args and **kwargs here.
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == get_api_key():
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@app.route('/')
def index():
    return 'api online'


@app.route('/validate_key')
@require_api_key
def validate_key():
    return 'API key is valid'


@app.route('/beer/status/<rfid>')
@require_api_key
def beer_rfid(rfid):
    try:
        ret = str(app.config.get('BeerService')(str(rfid)).status())
        logging.info('beer_rfid: Request with rfid ' + rfid + ' returns with ' + ret)
        return ret
    except Exception as e:
        logging.error('beer_rfid: An error has occurred with rfid ' + rfid)
        logging.exception(e)


@app.route('/beer/dispensed/<rfid>')
@require_api_key
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
