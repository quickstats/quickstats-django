import datetime
import logging
import os

import requests

from simplestats.numerous import Numerous

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

        Numerous.update_value(1518834333051481998, user['level'])
        Numerous.update_value(7591292017638108494, info['lessons_available'])
        Numerous.update_value(5850886773862194952, info['reviews_available'])
        if info['reviews_available'] == 0:
            Numerous.update_value(8834312823618892099, info['next_review_date'])

        yield now, 'wanikani.reviews', info['reviews_available']
        yield now, 'wanikani.lessons', info['lessons_available']
        yield now, 'wanikani.level', user['level']
