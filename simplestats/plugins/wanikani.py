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

    def numerousapp(self, metric_id, value):
        if 'NUMEROUS_KEY' in os.environ:
            response = requests.post(
                'https://api.numerousapp.com/v2/metrics/%s/events' % metric_id,
                auth=(os.getenv('NUMEROUS_KEY'), ''),
                json={'value': value}
            )
            logger.info('%s', response)

    def collect(self):
        now = datetime.datetime.utcnow()
        URL = 'https://www.wanikani.com/api/user/{}/study-queue'.format(self.api_key)
        result = requests.get(URL)
        json = result.json()
        user = json['user_information']
        info = json['requested_information']

        self.numerousapp('1518834333051481998', user['level'])
        self.numerousapp('7591292017638108494', info['lessons_available'])
        self.numerousapp('5850886773862194952', info['reviews_available'])
        if info['reviews_available'] == 0:
            self.numerousapp('8834312823618892099', info['next_review_date'])

        yield now, 'wanikani.reviews', info['reviews_available']
        yield now, 'wanikani.lessons', info['lessons_available']
        yield now, 'wanikani.level', user['level']
