import logging

from pkg_resources import working_set

logger = logging.getLogger(__name__)

for entry in working_set.iter_entry_points('simplestats.signals'):
    try:
        module = entry.load()
        logger.debug('Loaded %s', module)
    except ImportError:
        logger.warning('Error loading %s', entry)
