'''
Wrapper around Python requests

Simple wrapper around the Python requests library to collect all
of our custom headers and caching in a single place
'''

from __future__ import absolute_import

import requests

from simplestats import __version__

USER_AGENT = 'simplestats/%s https://github.com/kfdm/django-simplestats' % __version__

def get(url, *args, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['user-agent'] = USER_AGENT
    response = requests.get(url, *args, **kwargs)
    return response
