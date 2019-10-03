#!/bin/sh

set -e

if [ "${1:0:1}" = '-' ]; then
	set -- quickstats "$@"
fi

case "$1" in
worker)
  # Shortcut to start a celery worker
  set -- celery "-A" quickstats.standalone "$@"
  ;;
beat)
  # Shortcut to start a celery beat
  set -- celery "-A" quickstats.standalone "$@"
  ;;
web)
  # Shortcut for launching a gunicorn worker
  shift
  set -- gunicorn "quickstats.standalone.wsgi:application" -b 0.0.0.0 "$@"
  ;;
esac

# Finally exec our command
exec "$@"
