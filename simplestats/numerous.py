import os
import requests

class Numerous(object):
    @classmethod
    def update_value(cls, chart, value):
        return requests.post(
            'https://api.numerousapp.com/v2/metrics/{}/events'.format(chart),
            auth=(os.environ.get('NUMEROUS_KEY'), ''),
            json={'value': value}
        )

    @classmethod
    def update_chart(cls, chart, properties):
        return requests.put(
            'https://api.numerousapp.com/v2/metrics/{}'.format(chart),
            auth=(os.environ.get('NUMEROUS_KEY'), ''),
            json=properties,
        )
