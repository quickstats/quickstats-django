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
        now = datetime.datetime.utcnow()
        URL = 'https://www.wanikani.com/api/user/{}/study-queue'.format(self.api_key)
        result = requests.get(URL)
        json = result.json()
        user = json['user_information']
        info = json['requested_information']
        yield now, 'wanikani.reviews', info['reviews_available']
        yield now, 'wanikani.lessons', info['lessons_available']
        yield now, 'wanikani.level', user['level']
