import logging
import os

import requests

logger = logging.getLogger(__name__)

class Numerous(object):
    @classmethod
    def update_value(cls, chart, value):
        try:
            return requests.post(
                'https://api.numerousapp.com/v2/metrics/{}/events'.format(chart),
                auth=(os.environ.get('NUMEROUS_KEY'), ''),
                json={'value': value}
            )
        except IOError as e:
            logger.warning('Error posting to Numerous: %s', e)
            return None

    @classmethod
    def update_chart(cls, chart, properties):
        try:
            return requests.put(
                'https://api.numerousapp.com/v2/metrics/{}'.format(chart),
                auth=(os.environ.get('NUMEROUS_KEY'), ''),
                json=properties,
            )
        except IOError as e:
            logger.warning('Error posting to Numerous: %s', e)
            return None
