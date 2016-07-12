'''
Wrapper around Python requests

Simple wrapper around the Python requests library to collect all
of our custom headers and caching in a single place
'''

from __future__ import absolute_import

from functools import wraps

import requests

from simplestats import __version__

USER_AGENT = 'simplestats/%s https://github.com/kfdm/django-simplestats' % __version__


def add_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            kwargs['headers']['user-agent'] = USER_AGENT
        except KeyError:
            kwargs['headers'] = {'user-agent': USER_AGENT}
        return func(*args, **kwargs)
    return wrapper

get = add_args(requests.get)
post = add_args(requests.post)
put = add_args(requests.put)
