import logging

from pkg_resources import working_set

logger = logging.getLogger()

for entry in working_set.iter_entry_points('simplestats.signals'):
    try:
        module = entry.load()
        logging.debug('Loaded %s', module)
    except ImportError:
        logging.warning('Error loading %s', entry)
