import datetime
import logging
import os

import requests

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.wanikani')
logger = logging.getLogger(__name__)


class WaniKani(object):
    @property
    def api_key(self):
        if os.path.exists(CONFIG_PATH):
            logger.debug('Loading config from %s', CONFIG_PATH)
            with open(CONFIG_PATH) as f:
                return f.read().strip()
        return ''

    def collect(self):
        URL = 'https://www.wanikani.com/api/user/{}/study-queue'.format(self.api_key)
        result = requests.get(URL)
        data = result.json()['requested_information']
        yield datetime.datetime.utcnow(), 'wanikani.reviews', data['reviews_available']
        yield datetime.datetime.utcnow(), 'wanikani.lessons', data['lessons_available']
