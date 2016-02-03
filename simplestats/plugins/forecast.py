import datetime
import logging
import os

import requests

logger = logging.getLogger(__name__)


class ForecastIO(object):
    def collect(self):
        now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
        url = 'https://api.forecast.io/forecast/{0}/{1},{2}?units=si'.format(
            os.environ.get('FORECAST_IO'),
            33.5818585,
            130.3462494
        )
        result = requests.get(url)
        json = result.json()
        yield now, 'weather.fukuoka.temperature', json['currently']['temperature']
        yield now, 'weather.fukuoka.humidity', json['currently']['humidity']
