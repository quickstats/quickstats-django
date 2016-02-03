'''
Get currency data for JPY from forecast.io

https://docs.openexchangerates.org/docs/latest-json
'''

import datetime
import logging
import os

import requests

logger = logging.getLogger(__name__)


class Currency(object):
    def collect(self):
        now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
        url = 'https://openexchangerates.org/api/latest.json'
        result = requests.get(url, params={
            'app_id': os.environ.get('OPEN_EXCHANGE_RATES')
        })
        json = result.json()
        yield now, 'currency.USD.JPY', json['rates']['JPY']
